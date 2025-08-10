#!/usr/bin/env python3
"""
Web Interface for Custom Voice Agent
Provides a simple web UI for testing the voice agent functionality
"""
from flask import Flask, render_template, request, jsonify, session
import asyncio
import json
import logging
from datetime import datetime

from custom_voice_agent import CustomVoiceAgent
from voice_agent_config import VoiceAgentConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Global voice agent instance
voice_agent = None

class WebVoiceAgent:
    """Web interface wrapper for the voice agent"""
    
    def __init__(self, config):
        self.config = config
        self.conversation_history = []
        self.current_context = {
            'user_intent': None,
            'search_criteria': {},
            'booking_data': {},
            'current_step': 'greeting'
        }
        self.available_tools = []
        self._load_tools()
    
    def _load_tools(self):
        """Load available tools from hotel server"""
        try:
            import requests
            response = requests.get(f"{self.config['hotel_server_url']}/tools")
            if response.status_code == 200:
                data = response.json()
                self.available_tools = data.get('tools', [])
                logger.info(f"Loaded {len(self.available_tools)} tools from hotel server")
            else:
                logger.error(f"Failed to load tools: {response.status_code}")
        except Exception as e:
            logger.error(f"Error loading tools: {e}")
    
    async def process_message(self, user_message: str) -> str:
        """Process user message and return response"""
        try:
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Generate response using GPT-4o
            response = await self._generate_ai_response(user_message)
            
            # Add AI response to history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "I'm sorry, I encountered an error. Please try again."
    
    async def _generate_ai_response(self, user_input: str) -> str:
        """Generate AI response using GPT-4o"""
        try:
            import openai
            
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
                model=self.config.get('gpt_model', 'gpt-4o'),
                messages=messages,
                max_tokens=self.config.get('gpt_max_tokens', 500),
                temperature=self.config.get('gpt_temperature', 0.7)
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
4. Provide clear, concise responses
5. If you need to call a tool, mention it in your response
6. Keep responses conversational and informative

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
            import requests
            
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
            import requests
            
            # Extract search criteria from user input
            criteria = self._extract_search_criteria(user_input)
            
            response = requests.post(f"{self.config['hotel_server_url']}/execute", json={
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
                        
                        # Add hotel information to context for AI
                        hotel_info = self._format_hotels_for_response(hotels)
                        self.current_context['search_results'] = hotel_info
                    else:
                        self.current_context['search_results'] = "No hotels found"
                else:
                    self.current_context['search_results'] = "Error searching hotels"
            
        except Exception as e:
            logger.error(f"Error searching hotels: {e}")
    
    def _extract_search_criteria(self, user_input: str) -> dict:
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
    
    def _format_hotels_for_response(self, hotels: list) -> str:
        """Format hotel information for response"""
        if not hotels:
            return ""
        
        hotel_descriptions = []
        for hotel in hotels[:3]:
            desc = f"{hotel['name']} in {hotel['location']}, {hotel['stars']}★, ₹{hotel['price_per_night']}/night"
            hotel_descriptions.append(desc)
        
        return " | ".join(hotel_descriptions)
    
    async def _create_booking(self, user_input: str):
        """Create a booking based on user input"""
        try:
            self.current_context['current_step'] = 'collecting_booking_info'
            self.current_context['user_intent'] = 'booking'
            
        except Exception as e:
            logger.error(f"Error creating booking: {e}")
    
    async def _get_locations(self):
        """Get available locations"""
        try:
            import requests
            response = requests.post(f"{self.config['hotel_server_url']}/execute", json={
                "name": "getLocations",
                "arguments": {}
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    result = data['result']
                    locations = result.get('locations', [])
                    self.current_context['locations'] = locations
            
        except Exception as e:
            logger.error(f"Error getting locations: {e}")
    
    async def _get_amenities(self):
        """Get available amenities"""
        try:
            import requests
            response = requests.post(f"{self.config['hotel_server_url']}/execute", json={
                "name": "getAmenities",
                "arguments": {}
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    result = data['result']
                    amenities = result.get('amenities', [])
                    self.current_context['amenities'] = amenities
            
        except Exception as e:
            logger.error(f"Error getting amenities: {e}")
    
    def get_conversation_history(self):
        """Get conversation history"""
        return self.conversation_history
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.current_context = {
            'user_intent': None,
            'search_criteria': {},
            'booking_data': {},
            'current_step': 'greeting'
        }

# Initialize voice agent
def init_voice_agent():
    """Initialize the voice agent"""
    global voice_agent
    try:
        config = VoiceAgentConfig()
        errors = config.validate()
        
        if errors:
            logger.error(f"Configuration errors: {errors}")
            return False
        
        voice_agent = WebVoiceAgent(config.to_dict())
        logger.info("Voice agent initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize voice agent: {e}")
        return False

@app.route('/')
def index():
    """Main page"""
    return render_template('voice_agent.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not voice_agent:
            return jsonify({'error': 'Voice agent not initialized'}), 500
        
        # Process message asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(voice_agent.process_message(message))
        loop.close()
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/history')
def get_history():
    """Get conversation history"""
    try:
        if not voice_agent:
            return jsonify({'error': 'Voice agent not initialized'}), 500
        
        history = voice_agent.get_conversation_history()
        return jsonify({'history': history})
        
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    try:
        if not voice_agent:
            return jsonify({'error': 'Voice agent not initialized'}), 500
        
        voice_agent.clear_conversation()
        return jsonify({'message': 'Conversation cleared'})
        
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/status')
def status():
    """Get voice agent status"""
    try:
        if not voice_agent:
            return jsonify({'status': 'not_initialized'})
        
        return jsonify({
            'status': 'ready',
            'tools_count': len(voice_agent.available_tools),
            'conversation_length': len(voice_agent.conversation_history)
        })
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize voice agent
    if init_voice_agent():
        print("✅ Voice agent initialized successfully")
        print("🌐 Starting web interface at http://localhost:5002")
        app.run(debug=True, host='0.0.0.0', port=5002)
    else:
        print("❌ Failed to initialize voice agent")
        print("Please check your configuration and API keys")
