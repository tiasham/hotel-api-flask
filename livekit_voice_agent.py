#!/usr/bin/env python3
"""
Hotel Booking Voice Agent using LiveKit Agents Framework
"""
import logging
import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from dotenv import load_dotenv
_ = load_dotenv(override=True)

logger = logging.getLogger("hotel-agent")
logger.setLevel(logging.INFO)

from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, jupyter
from livekit.plugins import (
    openai,
    elevenlabs,
    silero,
)

class HotelBookingAssistant(Agent):
    def __init__(self) -> None:
        # Initialize AI components
        llm = openai.LLM(model="gpt-4o")
        stt = openai.STT()
        tts = elevenlabs.TTS()
        silero_vad = silero.VAD.load()

        # Hotel server configuration
        self.hotel_server_url = os.getenv('HOTEL_SERVER_URL', 'http://localhost:5001')
        self.available_tools = []
        self.conversation_context = {
            'user_intent': None,
            'search_criteria': {},
            'booking_data': {},
            'current_step': 'greeting'
        }
        
        # Load hotel tools
        self._load_hotel_tools()

        super().__init__(
            instructions=self._build_instructions(),
            stt=stt,
            llm=llm,
            tts=tts,
            vad=silero_vad,
        )
    
    def _load_hotel_tools(self):
        """Load available tools from hotel server"""
        try:
            response = requests.get(f"{self.hotel_server_url}/tools")
            if response.status_code == 200:
                data = response.json()
                self.available_tools = data.get('tools', [])
                logger.info(f"Loaded {len(self.available_tools)} hotel booking tools")
            else:
                logger.error(f"Failed to load hotel tools: {response.status_code}")
        except Exception as e:
            logger.error(f"Error loading hotel tools: {e}")
    
    def _build_instructions(self) -> str:
        """Build comprehensive instructions for the hotel booking assistant"""
        tools_info = "\n".join([
            f"- {tool['name']}: {tool['description']}" 
            for tool in self.available_tools
        ])
        
        return f"""
You are a helpful hotel booking assistant. You can help users search for hotels, get details, and make bookings.

AVAILABLE TOOLS:
{tools_info}

HOTEL INFORMATION:
- Available locations: Mumbai, Delhi, Bangalore
- Available amenities: Gym, Pool, Restaurant, Spa, WiFi, Parking, Concierge, Bar
- Room types: Deluxe, Suite, Presidential
- Price range: ₹11,000 - ₹25,000 per night
- All hotels are 5-star luxury properties

CONVERSATION GUIDELINES:
1. Be conversational, friendly, and helpful
2. Ask for missing information when needed (dates, number of guests, preferences)
3. Confirm details before making bookings
4. Provide clear, concise responses suitable for voice interaction
5. When users want to search for hotels, extract their criteria and call the searchHotels tool
6. When users want to book, guide them through the booking process step by step
7. Keep responses under 2-3 sentences for voice
8. Use natural language to describe hotel features and amenities

BOOKING PROCESS:
1. Collect guest information (name, email, phone)
2. Get travel dates (check-in, check-out)
3. Determine number of guests (adults, children)
4. Select hotel and room type
5. Confirm all details before creating booking
6. Provide booking confirmation with details

SEARCH CAPABILITIES:
- Search by location (Mumbai, Delhi, Bangalore)
- Filter by amenities (Pool, Spa, Gym, Restaurant, WiFi)
- Filter by price range
- Filter by number of guests
- Check availability for specific dates

EXAMPLE CONVERSATIONS:
User: "Find hotels in Mumbai"
Assistant: "I'll search for hotels in Mumbai for you. How many guests will be staying and what are your preferred dates?"

User: "I want a hotel with a pool"
Assistant: "I can help you find hotels with pools. Which city would you prefer - Mumbai, Delhi, or Bangalore?"

User: "Book a room for 2 adults and 1 child"
Assistant: "I'd be happy to help you book a room. I'll need some details: your name, email, preferred dates, and which city you'd like to stay in."

User: "What amenities do you have?"
Assistant: "Our hotels offer Gym, Pool, Restaurant, Spa, WiFi, Parking, Concierge, and Bar facilities. Is there a specific amenity you're looking for?"

Remember to be helpful, conversational, and guide users through the booking process naturally.
"""
    
    async def on_message(self, message: str) -> str:
        """Handle incoming messages and generate responses"""
        try:
            logger.info(f"Received message: {message}")
            
            # Check if we need to call hotel tools
            if self._should_call_hotel_tools(message):
                await self._handle_hotel_tool_calls(message)
            
            # Let the LLM generate a response
            return await super().on_message(message)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "I'm sorry, I encountered an error. Please try again."
    
    def _should_call_hotel_tools(self, message: str) -> bool:
        """Determine if we should call hotel tools based on user input"""
        hotel_keywords = ['search', 'find', 'hotel', 'book', 'reservation', 'location', 'amenity', 'price']
        return any(keyword in message.lower() for keyword in hotel_keywords)
    
    async def _handle_hotel_tool_calls(self, user_input: str):
        """Handle hotel tool calls based on user input"""
        try:
            # Determine which tool to call
            if 'search' in user_input.lower() or 'find' in user_input.lower():
                await self._search_hotels(user_input)
            elif 'book' in user_input.lower() or 'reservation' in user_input.lower():
                await self._handle_booking_request(user_input)
            elif 'location' in user_input.lower():
                await self._get_locations()
            elif 'amenity' in user_input.lower():
                await self._get_amenities()
            elif 'room type' in user_input.lower() or 'room types' in user_input.lower():
                await self._get_room_types()
            
        except Exception as e:
            logger.error(f"Error handling hotel tool calls: {e}")
    
    async def _search_hotels(self, user_input: str):
        """Search hotels based on user input"""
        try:
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
                        self.conversation_context['search_criteria'] = criteria
                        self.conversation_context['user_intent'] = 'searching_hotels'
                        self.conversation_context['search_results'] = hotels
                        
                        logger.info(f"Found {len(hotels)} hotels matching criteria")
                    else:
                        self.conversation_context['search_results'] = []
                        logger.info("No hotels found matching criteria")
                else:
                    logger.error(f"Hotel search failed: {data.get('error')}")
            
        except Exception as e:
            logger.error(f"Error searching hotels: {e}")
    
    def _extract_search_criteria(self, user_input: str) -> Dict:
        """Extract search criteria from user input"""
        criteria = {}
        
        # Extract location
        locations = ['mumbai', 'delhi', 'bangalore']
        for location in locations:
            if location in user_input.lower():
                criteria['location'] = location.title()
                break
        
        # Extract number of guests
        if 'adult' in user_input.lower():
            import re
            numbers = re.findall(r'\d+', user_input)
            if numbers:
                criteria['adults'] = int(numbers[0])
        
        if 'child' in user_input.lower():
            import re
            numbers = re.findall(r'\d+', user_input)
            if len(numbers) > 1:
                criteria['children'] = int(numbers[1])
            elif 'child' in user_input.lower():
                criteria['children'] = 1
        
        # Extract amenities
        amenities = ['pool', 'spa', 'gym', 'restaurant', 'wifi', 'parking', 'concierge', 'bar']
        found_amenities = []
        for amenity in amenities:
            if amenity in user_input.lower():
                found_amenities.append(amenity.title())
        
        if found_amenities:
            criteria['amenities'] = ','.join(found_amenities)
        
        # Extract price information
        if 'cheap' in user_input.lower() or 'budget' in user_input.lower():
            criteria['max_price'] = 15000
        elif 'luxury' in user_input.lower() or 'expensive' in user_input.lower():
            criteria['min_price'] = 20000
        
        return criteria
    
    async def _handle_booking_request(self, user_input: str):
        """Handle booking requests"""
        try:
            self.conversation_context['current_step'] = 'collecting_booking_info'
            self.conversation_context['user_intent'] = 'booking'
            
            # Extract any booking information from the input
            booking_info = self._extract_booking_info(user_input)
            self.conversation_context['booking_data'].update(booking_info)
            
            logger.info(f"Booking request initiated: {booking_info}")
            
        except Exception as e:
            logger.error(f"Error handling booking request: {e}")
    
    def _extract_booking_info(self, user_input: str) -> Dict:
        """Extract booking information from user input"""
        info = {}
        
        # Extract number of guests
        if 'adult' in user_input.lower():
            import re
            numbers = re.findall(r'\d+', user_input)
            if numbers:
                info['adults'] = int(numbers[0])
        
        if 'child' in user_input.lower():
            import re
            numbers = re.findall(r'\d+', user_input)
            if len(numbers) > 1:
                info['children'] = int(numbers[1])
            elif 'child' in user_input.lower():
                info['children'] = 1
        
        # Extract room type
        room_types = ['deluxe', 'suite', 'presidential']
        for room_type in room_types:
            if room_type in user_input.lower():
                info['room_type'] = room_type.title()
                break
        
        return info
    
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
                    self.conversation_context['locations'] = locations
                    logger.info(f"Available locations: {locations}")
            
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
                    self.conversation_context['amenities'] = amenities
                    logger.info(f"Available amenities: {amenities}")
            
        except Exception as e:
            logger.error(f"Error getting amenities: {e}")
    
    async def _get_room_types(self):
        """Get available room types"""
        try:
            response = requests.post(f"{self.hotel_server_url}/execute", json={
                "name": "getRoomTypes",
                "arguments": {}
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    result = data['result']
                    room_types = result.get('room_types', [])
                    self.conversation_context['room_types'] = room_types
                    logger.info(f"Available room types: {room_types}")
            
        except Exception as e:
            logger.error(f"Error getting room types: {e}")

async def entrypoint(ctx: JobContext):
    """Entry point for the voice agent job"""
    await ctx.connect()
    
    session = AgentSession()
    
    await session.start(
        room=ctx.room,
        agent=HotelBookingAssistant()
    )

if __name__ == "__main__":
    # For local development and testing
    import asyncio
    
    async def main():
        # Create a mock context for testing
        class MockContext:
            async def connect(self):
                logger.info("Mock connection established")
            
            @property
            def room(self):
                return "test-room"
        
        ctx = MockContext()
        await entrypoint(ctx)
    
    asyncio.run(main()) 