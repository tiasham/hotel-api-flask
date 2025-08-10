#!/usr/bin/env python3
"""
Voice Agent Trigger API
Triggers the hotel booking voice agent with Hindi/Hinglish personality
"""
import logging
import os
import json
import asyncio
import random
from datetime import datetime
from typing import Dict, Optional

from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests

load_dotenv(override=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class VoiceAgentTrigger:
    def __init__(self):
        self.hotel_server_url = os.getenv('HOTEL_SERVER_URL', 'http://localhost:5001')
        self.livekit_url = os.getenv('LIVEKIT_URL')
        self.livekit_api_key = os.getenv('LIVEKIT_API_KEY')
        self.livekit_api_secret = os.getenv('LIVEKIT_API_SECRET')
        
        # Available ticket numbers
        self.ticket_numbers = ["SR3017861", "SR3117862", "SR3217863"]
        
        # Conversation states
        self.active_conversations = {}
    
    def generate_ticket_number(self) -> str:
        """Generate a random ticket number"""
        return random.choice(self.ticket_numbers)
    
    def create_conversation_state(self, user_id: str) -> Dict:
        """Create a new conversation state"""
        return {
            'user_id': user_id,
            'ticket_number': self.generate_ticket_number(),
            'conversation_started': datetime.now().isoformat(),
            'current_step': 'greeting',
            'user_name': None,
            'booking_info': {
                'location': None,
                'check_in_date': None,
                'check_out_date': None,
                'adults': None,
                'children': None,
                'rooms': None,
                'guests_per_room': None,
                'amenities': None,
                'min_price': None,
                'max_price': None,
                'min_stars': None,
                'max_stars': None,
                'min_rating': None,
                'max_rating': None
            },
            'conversation_history': []
        }
    
    def get_greeting_message(self, ticket_number: str) -> str:
        """Get the initial greeting message"""
        return f"Hey, welcome to Cleartrip Hotel Support! मैं राज बोल रहा हूँ — super excited हूँ आपकी hotel booking में help करने के लिए! बताइए, कहाँ जाना है आपको? (Ticket: {ticket_number})"
    
    def get_next_question(self, conversation_state: Dict) -> str:
        """Get the next question based on missing information"""
        booking_info = conversation_state['booking_info']
        user_name = conversation_state['user_name']
        
        if not booking_info['location']:
            return "सबसे पहले बताइए — आपको किस शहर या एरिया में होटल चाहिए?"
        
        if not booking_info['check_in_date']:
            return f"Great! {booking_info['location']} में होटल ढूंढेंगे। Check-in और check-out की dates क्या होंगी?"
        
        if not booking_info['adults']:
            return "Adult और बच्चे — कितने लोग जा रहे हैं?"
        
        if not booking_info['rooms']:
            return "आपको कितने rooms की ज़रूरत होगी?"
        
        if not booking_info['guests_per_room']:
            return "हर room में लगभग कितने guests रुकेंगे?"
        
        if not booking_info['amenities']:
            return "कोई specific amenities चाहिए? जैसे wifi, pool, AC, breakfast वगैरह?"
        
        if not booking_info['min_price'] or not booking_info['max_price']:
            return "आपका budget क्या है — minimum और maximum per night price बताइए।"
        
        if not booking_info['min_stars']:
            return "कोई specific star rating चाहिए? जैसे three star, four star, five star?"
        
        if not booking_info['min_rating']:
            return "Guest reviews matter करते हैं क्या? Minimum four-plus rating दिखाऊँ?"
        
        if not user_name:
            return "Perfect! Booking शुरू करने से पहले — अपना नाम बता दीजिए।"
        
        return None
    
    def extract_booking_info(self, user_input: str, conversation_state: Dict) -> Dict:
        """Extract booking information from user input"""
        import re
        
        booking_info = conversation_state['booking_info']
        
        # Extract location
        locations = ['mumbai', 'delhi', 'bangalore', 'pune', 'hyderabad', 'chennai']
        for location in locations:
            if location in user_input.lower():
                booking_info['location'] = location.title()
                break
        
        # Extract dates
        date_patterns = [
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # DD/MM/YYYY
            r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # YYYY/MM/DD
        ]
        
        for pattern in date_patterns:
            dates = re.findall(pattern, user_input)
            if len(dates) >= 2:
                # Assume first date is check-in, second is check-out
                booking_info['check_in_date'] = f"{dates[0][0]}-{dates[0][1]}-{dates[0][2]}"
                booking_info['check_out_date'] = f"{dates[1][0]}-{dates[1][1]}-{dates[1][2]}"
                break
        
        # Extract number of adults
        adults_match = re.search(r'(\d+)\s*(adult|adults|person|people|लोग)', user_input.lower())
        if adults_match:
            booking_info['adults'] = int(adults_match.group(1))
        
        # Extract number of children
        children_match = re.search(r'(\d+)\s*(child|children|kid|kids|बच्चे)', user_input.lower())
        if children_match:
            booking_info['children'] = int(children_match.group(1))
        
        # Extract number of rooms
        rooms_match = re.search(r'(\d+)\s*(room|rooms|कमरे)', user_input.lower())
        if rooms_match:
            booking_info['rooms'] = int(rooms_match.group(1))
        
        # Extract guests per room
        guests_per_room_match = re.search(r'(\d+)\s*(guest|guests|per room|room में)', user_input.lower())
        if guests_per_room_match:
            booking_info['guests_per_room'] = int(guests_per_room_match.group(1))
        
        # Extract amenities
        amenities = ['wifi', 'pool', 'ac', 'breakfast', 'gym', 'spa', 'restaurant', 'parking']
        found_amenities = []
        for amenity in amenities:
            if amenity in user_input.lower():
                found_amenities.append(amenity.title())
        
        if found_amenities:
            booking_info['amenities'] = ','.join(found_amenities)
        
        # Extract price range
        price_match = re.search(r'(\d+)\s*(to|-)\s*(\d+)\s*(rs|rupees|price|रुपये)', user_input.lower())
        if price_match:
            booking_info['min_price'] = int(price_match.group(1))
            booking_info['max_price'] = int(price_match.group(3))
        
        # Extract star rating
        stars_match = re.search(r'(\d+)\s*star', user_input.lower())
        if stars_match:
            booking_info['min_stars'] = int(stars_match.group(1))
        
        # Extract user name
        name_patterns = [
            r'my name is (\w+)',
            r'i am (\w+)',
            r'मेरा नाम (\w+) है',
            r'मैं (\w+) हूँ'
        ]
        
        for pattern in name_patterns:
            name_match = re.search(pattern, user_input.lower())
            if name_match:
                conversation_state['user_name'] = name_match.group(1).title()
                break
        
        return booking_info
    
    def is_booking_complete(self, conversation_state: Dict) -> bool:
        """Check if all required booking information is collected"""
        booking_info = conversation_state['booking_info']
        required_fields = ['location', 'adults']
        return all(booking_info.get(field) for field in required_fields)
    
    def search_hotels(self, conversation_state: Dict) -> Dict:
        """Search hotels using the hotel server"""
        try:
            booking_info = conversation_state['booking_info']
            
            # Prepare search parameters
            search_params = {
                'location': booking_info.get('location'),
                'adults': booking_info.get('adults'),
                'children': booking_info.get('children', 0),
                'amenities': booking_info.get('amenities'),
                'min_price': booking_info.get('min_price'),
                'max_price': booking_info.get('max_price'),
                'min_stars': booking_info.get('min_stars'),
                'min_rating': booking_info.get('min_rating')
            }
            
            # Remove None values
            search_params = {k: v for k, v in search_params.items() if v is not None}
            
            response = requests.post(f"{self.hotel_server_url}/execute", json={
                "name": "searchHotels",
                "arguments": search_params
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data['result']
                else:
                    return {'error': data.get('error', 'Search failed')}
            else:
                return {'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Error searching hotels: {e}")
            return {'error': str(e)}
    
    def format_hotel_suggestions(self, hotels: list, user_name: str) -> str:
        """Format hotel suggestions in Hinglish"""
        if not hotels:
            return f"Sorry {user_name}, आपके criteria के according कोई hotels नहीं मिले। क्या आप different dates या budget try करना चाहेंगे?"
        
        response = f"Perfect {user_name}! मैंने आपके लिए {len(hotels)} hotels ढूंढे हैं। "
        
        for i, hotel in enumerate(hotels[:3], 1):
            response += f"एक शानदार option है {hotel['name']}, ये एक {hotel['stars']}-star property है, guest rating है {hotel['guest_rating']}/5, और price around {hotel['price_per_night']} rupees per night है। "
        
        response += f"मैंने {hotels[0]['name']} को आपके cart में डाल दिया है — आप आराम से review कर सकते हैं। जब आप ready हों, बस बता दीजिए — मैं तुरंत booking confirm कर दूँगा।"
        
        return response
    
    def process_user_input(self, user_id: str, user_input: str) -> str:
        """Process user input and generate response"""
        try:
            # Get or create conversation state
            if user_id not in self.active_conversations:
                self.active_conversations[user_id] = self.create_conversation_state(user_id)
            
            conversation_state = self.active_conversations[user_id]
            
            # Add user input to history
            conversation_state['conversation_history'].append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now().isoformat()
            })
            
            # Extract booking information
            self.extract_booking_info(user_input, conversation_state)
            
            # Check if booking is complete
            if self.is_booking_complete(conversation_state):
                # Search for hotels
                search_result = self.search_hotels(conversation_state)
                
                if 'error' not in search_result and search_result.get('hotels'):
                    hotels = search_result['hotels']
                    response = self.format_hotel_suggestions(hotels, conversation_state['user_name'] or 'Sir')
                else:
                    response = f"Sorry, कुछ technical issue आ रहा है। क्या आप थोड़ी देर बाद try कर सकते हैं?"
            else:
                # Get next question
                next_question = self.get_next_question(conversation_state)
                if next_question:
                    response = next_question
                else:
                    response = "Perfect! अब मैं आपके लिए hotels search करता हूँ।"
            
            # Add response to history
            conversation_state['conversation_history'].append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing user input: {e}")
            return "I'm sorry, I encountered an error. Please try again."

# Initialize the trigger
trigger = VoiceAgentTrigger()

@app.route('/trigger', methods=['POST'])
def trigger_voice_agent():
    """Trigger the voice agent with a new conversation"""
    try:
        data = request.json
        user_id = data.get('user_id', f"user_{datetime.now().timestamp()}")
        
        # Create new conversation
        conversation_state = trigger.create_conversation_state(user_id)
        trigger.active_conversations[user_id] = conversation_state
        
        # Get greeting message
        greeting = trigger.get_greeting_message(conversation_state['ticket_number'])
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'ticket_number': conversation_state['ticket_number'],
            'message': greeting,
            'conversation_started': conversation_state['conversation_started']
        })
        
    except Exception as e:
        logger.error(f"Error triggering voice agent: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Process chat message"""
    try:
        data = request.json
        user_id = data.get('user_id')
        message = data.get('message', '').strip()
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'user_id is required'
            }), 400
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'message is required'
            }), 400
        
        # Process the message
        response = trigger.process_user_input(user_id, message)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/conversation/<user_id>', methods=['GET'])
def get_conversation(user_id):
    """Get conversation history"""
    try:
        if user_id not in trigger.active_conversations:
            return jsonify({
                'success': False,
                'error': 'Conversation not found'
            }), 404
        
        conversation_state = trigger.active_conversations[user_id]
        
        return jsonify({
            'success': True,
            'conversation': conversation_state
        })
        
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/conversation/<user_id>', methods=['DELETE'])
def end_conversation(user_id):
    """End a conversation"""
    try:
        if user_id in trigger.active_conversations:
            del trigger.active_conversations[user_id]
        
        return jsonify({
            'success': True,
            'message': 'Conversation ended'
        })
        
    except Exception as e:
        logger.error(f"Error ending conversation: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'active_conversations': len(trigger.active_conversations),
        'hotel_server_url': trigger.hotel_server_url
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(debug=True, host='0.0.0.0', port=port)
