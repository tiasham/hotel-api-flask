#!/usr/bin/env python3
"""
Voice Agent with LiveKit Framework
- STT (Speech-to-Text)
- LLM (Language Model)
- TTS (Text-to-Speech)
- VAD (Voice Activity Detection)
- Dialogue Manager
- Hotel API Integration
"""
import asyncio
import json
import logging
import os
from typing import Dict, List, Optional
import requests
from datetime import datetime

# LiveKit imports
from livekit import rtc
from livekit.agents import (
    JobContext,
    WorkerOptions,
    agent,
    run_app,
)
from livekit.agents.llm import (
    LLM,
    LLMStream,
    Message,
    MessageRole,
    StreamState,
)
from livekit.agents.stt import (
    STT,
    STTEvent,
    STTEventType,
    STTStream,
)
from livekit.agents.tts import (
    TTS,
    TTSStream,
    SynthesisEvent,
    SynthesisEventType,
)
from livekit.agents.vad import (
    VAD,
    VADEvent,
    VADEventType,
    VADStream,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HotelAPI:
    """Hotel API integration"""
    
    def __init__(self, base_url: str = "https://hotel-api-flask-production.up.railway.app"):
        self.base_url = base_url
    
    def search_hotels(self, parameters: Dict) -> Dict:
        """Search hotels using the API"""
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json={
                    "name": "searchHotels",
                    "arguments": parameters
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Hotel API error: {e}")
            return {"error": str(e), "hotels": []}
    
    def get_locations(self) -> List[str]:
        """Get available locations"""
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json={
                    "name": "getLocations",
                    "arguments": {}
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result.get("result", {}).get("locations", [])
        except Exception as e:
            logger.error(f"Locations API error: {e}")
            return []
    
    def get_amenities(self) -> List[str]:
        """Get available amenities"""
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json={
                    "name": "getAmenities",
                    "arguments": {}
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result.get("result", {}).get("amenities", [])
        except Exception as e:
            logger.error(f"Amenities API error: {e}")
            return []

class DialogueManager:
    """Manages conversation flow and context"""
    
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.current_context: Dict = {}
        self.hotel_api = HotelAPI()
        
        # Available locations and amenities
        self.locations = self.hotel_api.get_locations()
        self.amenities = self.hotel_api.get_amenities()
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def extract_search_parameters(self, user_input: str) -> Dict:
        """Extract hotel search parameters from user input"""
        params = {}
        
        # Extract location
        for location in self.locations:
            if location.lower() in user_input.lower():
                params["location"] = location
                break
        
        # Extract number of adults
        import re
        adults_match = re.search(r'(\d+)\s*(adult|adults|person|people)', user_input.lower())
        if adults_match:
            params["adults"] = int(adults_match.group(1))
        
        # Extract number of children
        children_match = re.search(r'(\d+)\s*(child|children|kid|kids)', user_input.lower())
        if children_match:
            params["children"] = int(children_match.group(1))
        
        # Extract amenities
        found_amenities = []
        for amenity in self.amenities:
            if amenity.lower() in user_input.lower():
                found_amenities.append(amenity)
        if found_amenities:
            params["amenities"] = ",".join(found_amenities)
        
        # Extract price range
        price_match = re.search(r'(\d+)\s*(to|-)\s*(\d+)\s*(rs|rupees|price)', user_input.lower())
        if price_match:
            params["min_price"] = int(price_match.group(1))
            params["max_price"] = int(price_match.group(3))
        
        # Extract star rating
        stars_match = re.search(r'(\d+)\s*star', user_input.lower())
        if stars_match:
            params["min_stars"] = int(stars_match.group(1))
        
        return params
    
    def generate_response(self, user_input: str) -> str:
        """Generate appropriate response based on user input"""
        self.add_message("user", user_input)
        
        # Check if user wants to search for hotels
        search_keywords = ["hotel", "book", "search", "find", "stay", "accommodation"]
        is_search_request = any(keyword in user_input.lower() for keyword in search_keywords)
        
        if is_search_request:
            # Extract search parameters
            params = self.extract_search_parameters(user_input)
            
            if not params.get("location"):
                return "I'd be happy to help you find a hotel! Which city or location would you like to stay in?"
            
            if not params.get("adults"):
                return f"Great! I can help you find hotels in {params['location']}. How many adults will be traveling?"
            
            # Search for hotels
            result = self.hotel_api.search_hotels(params)
            
            if result.get("success") and result.get("result", {}).get("hotels"):
                hotels = result["result"]["hotels"]
                response = f"I found {len(hotels)} hotels in {params['location']} that match your criteria:\n\n"
                
                for i, hotel in enumerate(hotels[:3], 1):  # Show top 3
                    response += f"{i}. {hotel['name']} - {hotel['stars']} stars, Rating: {hotel['guest_rating']}/5\n"
                    response += f"   Price: ₹{hotel['price_per_night']}/night, Amenities: {hotel['amenities']}\n\n"
                
                response += "Would you like me to provide more details about any of these hotels?"
            else:
                response = f"I couldn't find hotels matching your criteria in {params['location']}. Would you like to try different search parameters?"
        else:
            # General conversation
            response = "Hello! I'm your hotel booking assistant. I can help you find and book hotels. What would you like to do?"
        
        self.add_message("assistant", response)
        return response

@agent()
class HotelVoiceAgent:
    """Voice agent for hotel booking"""
    
    def __init__(self, ctx: JobContext):
        self.ctx = ctx
        self.dialogue_manager = DialogueManager()
        
        # Initialize components
        self.stt = STT.create()
        self.tts = TTS.create()
        self.llm = LLM.create()
        self.vad = VAD.create()
        
        # Streams
        self.stt_stream: Optional[STTStream] = None
        self.tts_stream: Optional[TTSStream] = None
        self.llm_stream: Optional[LLMStream] = None
        self.vad_stream: Optional[VADStream] = None
        
        # Audio tracks
        self.audio_track: Optional[rtc.Track] = None
        self.mic_track: Optional[rtc.Track] = None
        
        # State
        self.is_speaking = False
        self.is_listening = False
    
    async def start(self):
        """Start the voice agent"""
        logger.info("Starting Hotel Voice Agent...")
        
        # Get audio tracks
        self.audio_track = self.ctx.room.local_tracks.get(rtc.TrackSource.AUDIO)
        self.mic_track = self.ctx.room.local_tracks.get(rtc.TrackSource.MICROPHONE)
        
        if not self.audio_track or not self.mic_track:
            logger.error("Audio tracks not found")
            return
        
        # Start VAD
        await self.start_vad()
        
        # Start listening
        await self.start_listening()
    
    async def start_vad(self):
        """Start Voice Activity Detection"""
        self.vad_stream = self.vad.stream()
        
        async def on_vad_event(event: VADEvent):
            if event.type == VADEventType.SPEECH_START:
                logger.info("Speech detected")
                self.is_listening = True
            elif event.type == VADEventType.SPEECH_END:
                logger.info("Speech ended")
                self.is_listening = False
                await self.process_speech()
        
        self.vad_stream.on("vad_event", on_vad_event)
        await self.vad_stream.start(self.mic_track)
    
    async def start_listening(self):
        """Start listening for speech"""
        self.stt_stream = self.stt.stream()
        
        async def on_stt_event(event: STTEvent):
            if event.type == STTEventType.FINAL_TRANSCRIPT:
                logger.info(f"Final transcript: {event.alternatives[0].text}")
                await self.handle_user_input(event.alternatives[0].text)
        
        self.stt_stream.on("stt_event", on_stt_event)
        await self.stt_stream.start(self.mic_track)
    
    async def handle_user_input(self, text: str):
        """Handle user input and generate response"""
        if self.is_speaking:
            return
        
        # Generate response using dialogue manager
        response = self.dialogue_manager.generate_response(text)
        
        # Speak the response
        await self.speak(response)
    
    async def speak(self, text: str):
        """Convert text to speech and play it"""
        if self.is_speaking:
            return
        
        self.is_speaking = True
        logger.info(f"Speaking: {text}")
        
        try:
            self.tts_stream = self.tts.stream()
            
            async def on_synthesis_event(event: SynthesisEvent):
                if event.type == SynthesisEventType.STARTED:
                    logger.info("TTS started")
                elif event.type == SynthesisEventType.FINISHED:
                    logger.info("TTS finished")
                    self.is_speaking = False
            
            self.tts_stream.on("synthesis_event", on_synthesis_event)
            
            # Send text to TTS
            await self.tts_stream.synthesize(text)
            
            # Play audio
            await self.tts_stream.start(self.audio_track)
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            self.is_speaking = False
    
    async def process_speech(self):
        """Process speech after VAD detects end"""
        if self.stt_stream:
            await self.stt_stream.flush()

async def main():
    """Main function to run the voice agent"""
    # Configure worker options
    options = WorkerOptions(
        url=os.getenv("LIVEKIT_URL", "ws://localhost:7880"),
        api_key=os.getenv("LIVEKIT_API_KEY", ""),
        api_secret=os.getenv("LIVEKIT_API_SECRET", ""),
    )
    
    # Run the agent
    await run_app(HotelVoiceAgent, options)

if __name__ == "__main__":
    asyncio.run(main()) 