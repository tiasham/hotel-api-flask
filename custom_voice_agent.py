#!/usr/bin/env python3
"""
Custom Voice Agent for Hotel Booking System
Integrates: LiveKit, Whisper STT, GPT-4o, ElevenLabs TTS
"""
import asyncio
import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp
import openai
import requests
from livekit import rtc
from livekit.rtc import AudioSource, Room, RoomEvent, TrackEvent
import whisper
from elevenlabs import generate, save, set_api_key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomVoiceAgent:
    def __init__(self, config: Dict):
        """
        Initialize the custom voice agent
        
        Args:
            config: Configuration dictionary with API keys and settings
        """
        self.config = config
        self.hotel_server_url = config.get('hotel_server_url', 'http://localhost:5001')
        
        # Initialize APIs
        self._setup_apis()
        
        # LiveKit room
        self.room: Optional[Room] = None
        self.audio_source: Optional[AudioSource] = None
        
        # Conversation state
        self.conversation_history = []
        self.current_context = {
            'user_intent': None,
            'search_criteria': {},
            'booking_data': {},
            'current_step': 'greeting'
        }
        
        # Available tools from hotel server
        self.available_tools = []
        self._load_tools()
    
    def _setup_apis(self):
        """Setup all API clients"""
        # OpenAI (GPT-4o)
        openai.api_key = self.config['openai_api_key']
        
        # ElevenLabs TTS
        set_api_key(self.config['elevenlabs_api_key'])
        
        # Whisper model
        self.whisper_model = whisper.load_model("base")
        
        # LiveKit
        self.livekit_url = self.config['livekit_url']
        self.livekit_api_key = self.config['livekit_api_key']
        self.livekit_api_secret = self.config['livekit_api_secret']
    
    def _load_tools(self):
        """Load available tools from hotel server"""
        try:
            response = requests.get(f"{self.hotel_server_url}/tools")
            if response.status_code == 200:
                data = response.json()
                self.available_tools = data.get('tools', [])
                logger.info(f"Loaded {len(self.available_tools)} tools from hotel server")
            else:
                logger.error(f"Failed to load tools: {response.status_code}")
        except Exception as e:
            logger.error(f"Error loading tools: {e}")
    
    async def start_voice_session(self, room_name: str, participant_name: str = "Hotel Agent"):
        """Start a voice session in LiveKit room"""
        try:
            # Create room connection
            self.room = Room()
            
            # Connect to room
            await self.room.connect(
                self.livekit_url,
                room_name,
                participant_name,
                api_key=self.livekit_api_key,
                api_secret=self.livekit_api_secret
            )
            
            logger.info(f"Connected to room: {room_name}")
            
            # Create audio source for TTS output
            self.audio_source = AudioSource()
            await self.room.local_participant.publish_track(self.audio_source)
            
            # Listen for audio from participants
            self.room.on(RoomEvent.TRACK_SUBSCRIBED, self._on_track_subscribed)
            
            # Start conversation
            await self._start_conversation()
            
        except Exception as e:
            logger.error(f"Failed to start voice session: {e}")
            raise
    
    def _on_track_subscribed(self, track, publication, participant):
        """Handle incoming audio tracks"""
        if track.kind == rtc.TrackKind.AUDIO:
            track.on(TrackEvent.DATA_RECEIVED, self._on_audio_data)
    
    async def _on_audio_data(self, data):
        """Process incoming audio data"""
        try:
            # Save audio data to temporary file
            audio_file = f"temp_audio_{int(time.time())}.wav"
            with open(audio_file, "wb") as f:
                f.write(data)
            
            # Convert speech to text using Whisper
            text = await self._speech_to_text(audio_file)
            
            if text and text.strip():
                logger.info(f"User said: {text}")
                await self._process_user_input(text)
            
            # Clean up temp file
            os.remove(audio_file)
            
        except Exception as e:
            logger.error(f"Error processing audio data: {e}")
    
    async def _speech_to_text(self, audio_file: str) -> str:
        """Convert speech to text using Whisper"""
        try:
            result = self.whisper_model.transcribe(audio_file)
            return result["text"].strip()
        except Exception as e:
            logger.error(f"Whisper STT error: {e}")
            return ""
    
    async def _text_to_speech(self, text: str) -> bytes:
        """Convert text to speech using ElevenLabs"""
        try:
            audio = generate(
                text=text,
                voice=self.config.get('elevenlabs_voice', 'Rachel'),
                model="eleven_monolingual_v1"
            )
            return audio
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            return b""
    
    async def _speak(self, text: str):
        """Speak text through LiveKit audio source"""
        try:
            audio_data = await self._text_to_speech(text)
            if audio_data and self.audio_source:
                # Convert audio data to proper format and send
                # This is a simplified version - you'd need proper audio format handling
                await self.audio_source.capture_frame(audio_data)
                logger.info(f"Spoke: {text}")
        except Exception as e:
            logger.error(f"Error speaking: {e}")
    
    async def _process_user_input(self, user_text: str):
        """Process user input and generate response"""
        try:
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_text})
            
            # Generate response using GPT-4o
            response = await self._generate_ai_response(user_text)
            
            # Add AI response to history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # Speak the response
            await self._speak(response)
            
        except Exception as e:
            logger.error(f"Error processing user input: {e}")
            await self._speak("I'm sorry, I encountered an error. Please try again.")
    
    async def _generate_ai_response(self, user_input: str) -> str:
        """Generate AI response using GPT-4o"""
        try:
            # Build system prompt with context
            system_prompt = self._build_system_prompt()
            
            # Create messages for GPT
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            
            # Add recent conversation history
            for msg in self.conversation_history[-6:]:  # Last 3 exchanges
                messages.append(msg)
            
            # Call GPT-4o
            response = await openai.ChatCompletion.acreate(
                model="gpt-4o",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Check if AI wants to call hotel server tools
            await self._handle_tool_calls(ai_response, user_input)
            
            return ai_response
            
        except Exception as e:
            logger.error(f"GPT-4o error: {e}")
            return "I'm sorry, I'm having trouble processing your request right now."
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with hotel booking context"""
        tools_info = "\n".join([
            f"- {tool['name']}: {tool['description']}" 
            for tool in self.available_tools
        ])
        
        return f"""
You are a helpful hotel booking assistant. You can help users search for hotels, get details, and make bookings.

Available tools:
{tools_info}

Current conversation context:
- User intent: {self.current_context['user_intent']}
- Current step: {self.current_context['current_step']}
- Search criteria: {self.current_context['search_criteria']}
- Booking data: {self.current_context['booking_data']}

Guidelines:
1. Be conversational and helpful
2. Ask for missing information when needed
3. Confirm details before making bookings
4. Provide clear, concise responses suitable for voice
5. If you need to call a tool, mention it in your response
6. Keep responses under 2-3 sentences for voice

Current available locations: Mumbai, Delhi, Bangalore
Available amenities: Gym, Pool, Restaurant, Spa, WiFi, Parking, Concierge, Bar
Room types: Deluxe, Suite, Presidential
"""
    
    async def _handle_tool_calls(self, ai_response: str, user_input: str):
        """Handle tool calls based on AI response and user input"""
        try:
            # Determine if we need to call hotel server tools
            if any(keyword in user_input.lower() for keyword in ['search', 'find', 'hotel', 'book', 'reservation']):
                await self._call_hotel_tools(user_input)
            
        except Exception as e:
            logger.error(f"Error handling tool calls: {e}")
    
    async def _call_hotel_tools(self, user_input: str):
        """Call appropriate hotel server tools based on user input"""
        try:
            # Determine which tool to call based on user input
            if 'search' in user_input.lower() or 'find' in user_input.lower():
                await self._search_hotels(user_input)
            elif 'book' in user_input.lower() or 'reservation' in user_input.lower():
                await self._create_booking(user_input)
            elif 'location' in user_input.lower():
                await self._get_locations()
            elif 'amenity' in user_input.lower():
                await self._get_amenities()
            
        except Exception as e:
            logger.error(f"Error calling hotel tools: {e}")
    
    async def _search_hotels(self, user_input: str):
        """Search hotels based on user input"""
        try:
            # Extract search criteria from user input
            criteria = self._extract_search_criteria(user_input)
            
            response = requests.post(f"{self.hotel_server_url}/execute", json={
                "name": "searchHotels",
                "arguments": criteria
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    result = data['result']
                    hotels = result.get('hotels', [])
                    
                    if hotels:
                        # Update context
                        self.current_context['search_criteria'] = criteria
                        self.current_context['user_intent'] = 'searching_hotels'
                        
                        # Generate response about found hotels
                        hotel_info = self._format_hotels_for_voice(hotels)
                        response_text = f"I found {len(hotels)} hotels matching your criteria. {hotel_info}"
                        await self._speak(response_text)
                    else:
                        await self._speak("I couldn't find any hotels matching your criteria. Would you like to try different search parameters?")
                else:
                    await self._speak("I'm sorry, there was an error searching for hotels. Please try again.")
            
        except Exception as e:
            logger.error(f"Error searching hotels: {e}")
            await self._speak("I encountered an error while searching for hotels.")
    
    def _extract_search_criteria(self, user_input: str) -> Dict:
        """Extract search criteria from user input"""
        criteria = {}
        
        # Extract location
        locations = ['mumbai', 'delhi', 'bangalore']
        for location in locations:
            if location in user_input.lower():
                criteria['location'] = location.title()
                break
        
        # Extract number of guests (simple extraction)
        if 'adult' in user_input.lower():
            # Simple number extraction - in production, use NLP
            import re
            numbers = re.findall(r'\d+', user_input)
            if numbers:
                criteria['adults'] = int(numbers[0])
        
        # Extract amenities
        amenities = ['pool', 'spa', 'gym', 'restaurant', 'wifi']
        found_amenities = []
        for amenity in amenities:
            if amenity in user_input.lower():
                found_amenities.append(amenity.title())
        
        if found_amenities:
            criteria['amenities'] = ','.join(found_amenities)
        
        return criteria
    
    def _format_hotels_for_voice(self, hotels: List[Dict]) -> str:
        """Format hotel information for voice output"""
        if not hotels:
            return ""
        
        # Format first 3 hotels
        hotel_descriptions = []
        for hotel in hotels[:3]:
            desc = f"{hotel['name']} in {hotel['location']}, rated {hotel['stars']} stars, costs ₹{hotel['price_per_night']} per night"
            hotel_descriptions.append(desc)
        
        return " ".join(hotel_descriptions)
    
    async def _create_booking(self, user_input: str):
        """Create a booking based on user input"""
        try:
            # This would extract booking details from user input
            # For now, we'll ask for more information
            await self._speak("I'd be happy to help you make a booking. I'll need some details like your name, email, preferred dates, and number of guests.")
            self.current_context['current_step'] = 'collecting_booking_info'
            
        except Exception as e:
            logger.error(f"Error creating booking: {e}")
            await self._speak("I encountered an error while processing your booking request.")
    
    async def _get_locations(self):
        """Get available locations"""
        try:
            response = requests.post(f"{self.hotel_server_url}/execute", json={
                "name": "getLocations",
                "arguments": {}
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    result = data['result']
                    locations = result.get('locations', [])
                    await self._speak(f"We have hotels in {', '.join(locations)}.")
            
        except Exception as e:
            logger.error(f"Error getting locations: {e}")
    
    async def _get_amenities(self):
        """Get available amenities"""
        try:
            response = requests.post(f"{self.hotel_server_url}/execute", json={
                "name": "getAmenities",
                "arguments": {}
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    result = data['result']
                    amenities = result.get('amenities', [])
                    await self._speak(f"Our hotels offer {', '.join(amenities[:5])} and more.")
            
        except Exception as e:
            logger.error(f"Error getting amenities: {e}")
    
    async def _start_conversation(self):
        """Start the conversation with a greeting"""
        greeting = "Hello! I'm your hotel booking assistant. I can help you search for hotels, get details, and make reservations. What would you like to do today?"
        await self._speak(greeting)
    
    async def stop_voice_session(self):
        """Stop the voice session"""
        try:
            if self.room:
                await self.room.disconnect()
                logger.info("Voice session stopped")
        except Exception as e:
            logger.error(f"Error stopping voice session: {e}")

# Configuration example
CONFIG = {
    'openai_api_key': 'your-openai-api-key',
    'elevenlabs_api_key': 'your-elevenlabs-api-key',
    'elevenlabs_voice': 'Rachel',
    'livekit_url': 'ws://localhost:7880',
    'livekit_api_key': 'your-livekit-api-key',
    'livekit_api_secret': 'your-livekit-api-secret',
    'hotel_server_url': 'http://localhost:5001'
}

async def main():
    """Main function to run the voice agent"""
    # Create voice agent
    agent = CustomVoiceAgent(CONFIG)
    
    try:
        # Start voice session
        await agent.start_voice_session("hotel-booking-room", "Hotel Agent")
        
        # Keep the session alive
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Stopping voice agent...")
        await agent.stop_voice_session()
    except Exception as e:
        logger.error(f"Error in main: {e}")
        await agent.stop_voice_session()

if __name__ == "__main__":
    asyncio.run(main())
