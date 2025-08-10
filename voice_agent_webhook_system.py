#!/usr/bin/env python3
"""
Voice Agent Webhook System
Triggers LiveKit voice agent with Hindi/Hinglish personality for hotel booking
"""
import logging
import os
import json
import asyncio
import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import requests
import pandas as pd

from dotenv import load_dotenv
from flask import Flask, request, jsonify
import subprocess
import threading
import time

load_dotenv(override=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class VoiceAgentWebhookSystem:
    def __init__(self):
        self.hotel_server_url = os.getenv('HOTEL_SERVER_URL', 'http://localhost:5001')
        self.livekit_url = os.getenv('LIVEKIT_URL')
        self.livekit_api_key = os.getenv('LIVEKIT_API_KEY')
        self.livekit_api_secret = os.getenv('LIVEKIT_API_SECRET')
        self.hotel_dataset_path = 'Hotel_Dataset.csv'
        
        # Available ticket numbers
        self.ticket_numbers = ["SR3017861", "SR3117862", "SR3217863"]
        
        # Active voice sessions
        self.active_sessions = {}
        
        # Conversation states
        self.conversation_states = {}
        
        # Load hotel dataset
        self.load_hotel_dataset()
    
    def load_hotel_dataset(self):
        """Load hotel dataset from CSV"""
        try:
            if os.path.exists(self.hotel_dataset_path):
                self.hotel_df = pd.read_csv(self.hotel_dataset_path)
                logger.info(f"Loaded {len(self.hotel_df)} hotels from dataset")
            else:
                logger.warning(f"Hotel dataset not found: {self.hotel_dataset_path}")
                self.hotel_df = pd.DataFrame()
        except Exception as e:
            logger.error(f"Error loading hotel dataset: {e}")
            self.hotel_df = pd.DataFrame()
    
    def generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"session_{uuid.uuid4().hex[:8]}"
    
    def generate_ticket_number(self) -> str:
        """Generate a random ticket number"""
        return random.choice(self.ticket_numbers)
    
    def create_conversation_state(self, session_id: str, user_id: str) -> Dict:
        """Create a new conversation state"""
        return {
            'session_id': session_id,
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
            'conversation_history': [],
            'voice_session_active': False,
            'livekit_room_name': None,
            'livekit_token': None
        }
    
    def get_greeting_message(self, ticket_number: str) -> str:
        """Get the initial greeting message"""
        return f"Hey, welcome to Cleartrip Hotel Support! मैं राज बोल रहा हूँ — super excited हूँ आपकी hotel booking में help करने के लिए! बताइए, कहाँ जाना है आपको? (Ticket: {ticket_number})"
    
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
    
    def is_booking_complete(self, conversation_state: Dict) -> bool:
        """Check if all required booking information is collected"""
        booking_info = conversation_state['booking_info']
        required_fields = ['location', 'adults']
        return all(booking_info.get(field) for field in required_fields)
    
    def search_hotels_from_dataset(self, conversation_state: Dict) -> List[Dict]:
        """Search hotels from the CSV dataset with comprehensive filtering"""
        try:
            if self.hotel_df.empty:
                logger.warning("Hotel dataset is empty")
                return []
            
            booking_info = conversation_state['booking_info']
            df = self.hotel_df.copy()
            
            logger.info(f"Starting hotel search with filters: {booking_info}")
            initial_count = len(df)
            
            # Location filter (case-insensitive partial match)
            if booking_info.get('location'):
                location_filter = booking_info['location'].strip().lower()
                df = df[df['location'].str.lower().str.contains(location_filter, na=False)]
                logger.info(f"After location filter '{location_filter}': {len(df)} hotels")
            
            # Capacity filters - using correct column names from CSV
            if booking_info.get('adults'):
                adults_needed = int(booking_info['adults'])
                df = df[df['guests_adults'] >= adults_needed]
                logger.info(f"After adults filter (>= {adults_needed}): {len(df)} hotels")
            
            if booking_info.get('children'):
                children_needed = int(booking_info['children'])
                df = df[df['guests_children'] >= children_needed]
                logger.info(f"After children filter (>= {children_needed}): {len(df)} hotels")
            
            # Room capacity filter (if rooms and guests_per_room specified)
            if booking_info.get('rooms') and booking_info.get('guests_per_room'):
                rooms_needed = int(booking_info['rooms'])
                guests_per_room = int(booking_info['guests_per_room'])
                total_guests = rooms_needed * guests_per_room
                
                # Check if hotel can accommodate total guests
                df = df[df['guests_adults'] + df['guests_children'] >= total_guests]
                logger.info(f"After room capacity filter (>= {total_guests} total guests): {len(df)} hotels")
            
            # Amenities filter (case-insensitive partial match)
            if booking_info.get('amenities'):
                amenities_list = [amenity.strip().lower() for amenity in booking_info['amenities'].split(',')]
                for amenity in amenities_list:
                    if amenity:  # Skip empty strings
                        df = df[df['amenities'].str.lower().str.contains(amenity, na=False)]
                        logger.info(f"After amenity filter '{amenity}': {len(df)} hotels")
            
            # Price filters
            if booking_info.get('min_price'):
                min_price = float(booking_info['min_price'])
                df = df[df['price_per_night'] >= min_price]
                logger.info(f"After min price filter (>= {min_price}): {len(df)} hotels")
            
            if booking_info.get('max_price'):
                max_price = float(booking_info['max_price'])
                df = df[df['price_per_night'] <= max_price]
                logger.info(f"After max price filter (<= {max_price}): {len(df)} hotels")
            
            # Star rating filters
            if booking_info.get('min_stars'):
                min_stars = int(booking_info['min_stars'])
                df = df[df['stars'] >= min_stars]
                logger.info(f"After min stars filter (>= {min_stars}): {len(df)} hotels")
            
            if booking_info.get('max_stars'):
                max_stars = int(booking_info['max_stars'])
                df = df[df['stars'] <= max_stars]
                logger.info(f"After max stars filter (<= {max_stars}): {len(df)} hotels")
            
            # Guest rating filter
            if booking_info.get('min_rating'):
                min_rating = float(booking_info['min_rating'])
                df = df[df['guest_rating'] >= min_rating]
                logger.info(f"After min rating filter (>= {min_rating}): {len(df)} hotels")
            
            if booking_info.get('max_rating'):
                max_rating = float(booking_info['max_rating'])
                df = df[df['guest_rating'] <= max_rating]
                logger.info(f"After max rating filter (<= {max_rating}): {len(df)} hotels")
            
            # Date availability filter (if check-in and check-out dates are specified)
            if booking_info.get('check_in_date') and booking_info.get('check_out_date'):
                try:
                    check_in = datetime.strptime(booking_info['check_in_date'], '%Y-%m-%d')
                    check_out = datetime.strptime(booking_info['check_out_date'], '%Y-%m-%d')
                    
                    # Filter hotels that have availability for the requested dates
                    # This is a simplified check - in a real system you'd check actual availability
                    df = df[
                        (df['check_in'] <= check_in.strftime('%d-%b-%Y')) &
                        (df['check_out'] >= check_out.strftime('%d-%b-%Y'))
                    ]
                    logger.info(f"After date availability filter: {len(df)} hotels")
                except ValueError as e:
                    logger.warning(f"Date parsing error: {e}, skipping date filter")
            
            # Sort by multiple criteria: rating first, then price (ascending for better deals)
            if not df.empty:
                df = df.sort_values(['guest_rating', 'price_per_night'], ascending=[False, True])
                
                # Limit results to top 10 for better performance
                df = df.head(10)
                
                logger.info(f"Final results: {len(df)} hotels found (from {initial_count} total)")
                
                # Convert to list of dictionaries and add some computed fields
                results = []
                for _, hotel in df.iterrows():
                    hotel_dict = hotel.to_dict()
                    
                    # Add computed fields
                    hotel_dict['total_price'] = hotel_dict['price_per_night']
                    hotel_dict['amenities_list'] = eval(hotel_dict['amenities']) if isinstance(hotel_dict['amenities'], str) else []
                    hotel_dict['rating_category'] = self._get_rating_category(hotel_dict['guest_rating'])
                    hotel_dict['price_category'] = self._get_price_category(hotel_dict['price_per_night'])
                    
                    results.append(hotel_dict)
                
                return results
            else:
                logger.info("No hotels found matching the criteria")
                return []
            
        except Exception as e:
            logger.error(f"Error searching hotels from dataset: {e}")
            return []
    
    def _get_rating_category(self, rating: float) -> str:
        """Get rating category based on guest rating"""
        if rating >= 4.5:
            return "Excellent"
        elif rating >= 4.0:
            return "Very Good"
        elif rating >= 3.5:
            return "Good"
        elif rating >= 3.0:
            return "Average"
        else:
            return "Below Average"
    
    def _get_price_category(self, price: float) -> str:
        """Get price category based on price per night"""
        if price <= 3000:
            return "Budget"
        elif price <= 6000:
            return "Mid-Range"
        elif price <= 10000:
            return "Premium"
        else:
            return "Luxury"
    
    def get_available_locations(self) -> List[str]:
        """Get list of available locations from dataset"""
        try:
            if self.hotel_df.empty:
                return []
            return sorted(self.hotel_df['location'].unique().tolist())
        except Exception as e:
            logger.error(f"Error getting available locations: {e}")
            return []
    
    def get_available_amenities(self) -> List[str]:
        """Get list of available amenities from dataset"""
        try:
            if self.hotel_df.empty:
                return []
            
            all_amenities = set()
            for amenities_str in self.hotel_df['amenities']:
                try:
                    if isinstance(amenities_str, str):
                        amenities_list = eval(amenities_str)
                        if isinstance(amenities_list, list):
                            all_amenities.update(amenities_list)
                except:
                    continue
            
            return sorted(list(all_amenities))
        except Exception as e:
            logger.error(f"Error getting available amenities: {e}")
            return []
    
    def get_price_range(self) -> Dict[str, float]:
        """Get price range from dataset"""
        try:
            if self.hotel_df.empty:
                return {'min': 0, 'max': 0}
            
            min_price = self.hotel_df['price_per_night'].min()
            max_price = self.hotel_df['price_per_night'].max()
            
            return {'min': float(min_price), 'max': float(max_price)}
        except Exception as e:
            logger.error(f"Error getting price range: {e}")
            return {'min': 0, 'max': 0}
    
    def format_hotel_suggestions(self, hotels: List[Dict], user_name: str) -> str:
        """Format hotel suggestions in Hinglish with enhanced details"""
        if not hotels:
            return f"Sorry {user_name}, आपके criteria के according कोई hotels नहीं मिले। क्या आप different dates या budget try करना चाहेंगे?"
        
        response = f"Perfect {user_name}! मैंने आपके लिए {len(hotels)} hotels ढूंढे हैं। "
        
        # Format top 3 hotels with enhanced details
        for i, hotel in enumerate(hotels[:3], 1):
            hotel_name = hotel.get('name', 'Hotel')
            stars = hotel.get('stars', 0)
            rating = hotel.get('guest_rating', 0)
            price = hotel.get('price_per_night', 0)
            location = hotel.get('location', '')
            rating_category = hotel.get('rating_category', '')
            price_category = hotel.get('price_category', '')
            
            # Format amenities (take first 3)
            amenities_list = hotel.get('amenities_list', [])
            amenities_display = ', '.join(amenities_list[:3]) if amenities_list else 'basic amenities'
            
            response += f"एक {rating_category} option है {hotel_name}, ये एक {stars}-star {price_category} property है, guest rating है {rating}/5, और price around {price:,} rupees per night है। Location भी बढ़िया है — {location} में। Available amenities include {amenities_display}. "
        
        # Add recommendation for the best option
        best_hotel = hotels[0]
        best_hotel_name = best_hotel.get('name', 'Hotel')
        best_hotel_price = best_hotel.get('price_per_night', 0)
        
        response += f"मैंने {best_hotel_name} को आपके cart में डाल दिया है — ये best value for money है at {best_hotel_price:,} rupees per night। आप आराम से review कर सकते हैं। जब आप ready हों, बस बता दीजिए — मैं तुरंत booking confirm कर दूँगा।"
        
        return response
    
    def process_user_input(self, session_id: str, user_input: str) -> str:
        """Process user input and generate response"""
        try:
            if session_id not in self.conversation_states:
                return "Session not found. Please start a new conversation."
            
            conversation_state = self.conversation_states[session_id]
            
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
                # Search for hotels from dataset
                hotels = self.search_hotels_from_dataset(conversation_state)
                
                if hotels:
                    response = self.format_hotel_suggestions(hotels, conversation_state['user_name'] or 'Sir')
                else:
                    response = f"Sorry, आपके criteria के according कोई hotels नहीं मिले। क्या आप different dates या budget try करना चाहेंगे?"
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
    
    def start_livekit_voice_session(self, session_id: str) -> Dict:
        """Start LiveKit voice session"""
        try:
            if not all([self.livekit_url, self.livekit_api_key, self.livekit_api_secret]):
                return {
                    'success': False,
                    'error': 'LiveKit configuration missing'
                }
            
            # Generate room name
            room_name = f"hotel_booking_{session_id}"
            
            # Start LiveKit agent in background
            def run_livekit_agent():
                try:
                    # Create a temporary script to run the LiveKit agent
                    agent_script = f"""
import asyncio
import os
from livekit_voice_agent import HotelBookingAssistant
from livekit.agents import AgentSession, JobContext

async def run_agent():
    # Set environment variables
    os.environ['LIVEKIT_URL'] = '{self.livekit_url}'
    os.environ['LIVEKIT_API_KEY'] = '{self.livekit_api_key}'
    os.environ['LIVEKIT_API_SECRET'] = '{self.livekit_api_secret}'
    
    # Create mock context
    class MockContext:
        def __init__(self):
            self.room = type('Room', (), {{'name': '{room_name}'}})()
        
        async def connect(self):
            pass
    
    ctx = MockContext()
    await ctx.connect()
    
    session = AgentSession()
    agent = HotelBookingAssistant()
    
    await session.start(room=ctx.room, agent=agent)

if __name__ == "__main__":
    asyncio.run(run_agent())
"""
                    
                    # Write script to file
                    script_path = f"temp_agent_{session_id}.py"
                    with open(script_path, 'w') as f:
                        f.write(agent_script)
                    
                    # Run the agent
                    subprocess.run(['python', script_path], check=True)
                    
                    # Clean up
                    os.remove(script_path)
                    
                except Exception as e:
                    logger.error(f"Error running LiveKit agent: {e}")
            
            # Start agent in background thread
            thread = threading.Thread(target=run_livekit_agent)
            thread.daemon = True
            thread.start()
            
            # Update conversation state
            if session_id in self.conversation_states:
                self.conversation_states[session_id]['voice_session_active'] = True
                self.conversation_states[session_id]['livekit_room_name'] = room_name
            
            return {
                'success': True,
                'room_name': room_name,
                'message': 'Voice session started successfully'
            }
            
        except Exception as e:
            logger.error(f"Error starting LiveKit voice session: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Initialize the system
webhook_system = VoiceAgentWebhookSystem()

@app.route('/webhook/trigger', methods=['POST'])
def trigger_voice_agent():
    """Webhook to trigger voice agent"""
    try:
        data = request.json
        user_id = data.get('user_id', f"user_{datetime.now().timestamp()}")
        start_voice = data.get('start_voice', False)
        
        # Generate session ID
        session_id = webhook_system.generate_session_id()
        
        # Create conversation state
        conversation_state = webhook_system.create_conversation_state(session_id, user_id)
        webhook_system.conversation_states[session_id] = conversation_state
        
        # Get greeting message
        greeting = webhook_system.get_greeting_message(conversation_state['ticket_number'])
        
        response_data = {
            'success': True,
            'session_id': session_id,
            'user_id': user_id,
            'ticket_number': conversation_state['ticket_number'],
            'message': greeting,
            'conversation_started': conversation_state['conversation_started'],
            'voice_session_active': False
        }
        
        # Start voice session if requested
        if start_voice:
            voice_result = webhook_system.start_livekit_voice_session(session_id)
            if voice_result['success']:
                response_data['voice_session_active'] = True
                response_data['room_name'] = voice_result['room_name']
                response_data['voice_message'] = voice_result['message']
            else:
                response_data['voice_error'] = voice_result['error']
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error triggering voice agent: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/webhook/chat', methods=['POST'])
def chat():
    """Process chat message"""
    try:
        data = request.json
        session_id = data.get('session_id')
        message = data.get('message', '').strip()
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'session_id is required'
            }), 400
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'message is required'
            }), 400
        
        # Process the message
        response = webhook_system.process_user_input(session_id, message)
        
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

@app.route('/webhook/start-voice', methods=['POST'])
def start_voice_session():
    """Start voice session for existing conversation"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'session_id is required'
            }), 400
        
        if session_id not in webhook_system.conversation_states:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        # Start voice session
        voice_result = webhook_system.start_livekit_voice_session(session_id)
        
        return jsonify(voice_result)
        
    except Exception as e:
        logger.error(f"Error starting voice session: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/webhook/conversation/<session_id>', methods=['GET'])
def get_conversation(session_id):
    """Get conversation history"""
    try:
        if session_id not in webhook_system.conversation_states:
            return jsonify({
                'success': False,
                'error': 'Conversation not found'
            }), 404
        
        conversation_state = webhook_system.conversation_states[session_id]
        
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

@app.route('/webhook/conversation/<session_id>', methods=['DELETE'])
def end_conversation(session_id):
    """End a conversation"""
    try:
        if session_id in webhook_system.conversation_states:
            del webhook_system.conversation_states[session_id]
        
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

@app.route('/webhook/hotels/search', methods=['POST'])
def search_hotels():
    """Search hotels from dataset"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if not session_id or session_id not in webhook_system.conversation_states:
            return jsonify({
                'success': False,
                'error': 'Valid session_id is required'
            }), 400
        
        conversation_state = webhook_system.conversation_states[session_id]
        hotels = webhook_system.search_hotels_from_dataset(conversation_state)
        
        return jsonify({
            'success': True,
            'hotels': hotels,
            'count': len(hotels)
        })
        
    except Exception as e:
        logger.error(f"Error searching hotels: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/webhook/hotels/locations', methods=['GET'])
def get_available_locations():
    """Get available locations from dataset"""
    try:
        locations = webhook_system.get_available_locations()
        return jsonify({
            'success': True,
            'locations': locations,
            'count': len(locations)
        })
    except Exception as e:
        logger.error(f"Error getting locations: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/webhook/hotels/amenities', methods=['GET'])
def get_available_amenities():
    """Get available amenities from dataset"""
    try:
        amenities = webhook_system.get_available_amenities()
        return jsonify({
            'success': True,
            'amenities': amenities,
            'count': len(amenities)
        })
    except Exception as e:
        logger.error(f"Error getting amenities: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/webhook/hotels/price-range', methods=['GET'])
def get_price_range():
    """Get price range from dataset"""
    try:
        price_range = webhook_system.get_price_range()
        return jsonify({
            'success': True,
            'price_range': price_range
        })
    except Exception as e:
        logger.error(f"Error getting price range: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/webhook/hotels/search/advanced', methods=['POST'])
def advanced_hotel_search():
    """Advanced hotel search with direct parameters"""
    try:
        data = request.json
        
        # Create a temporary conversation state for this search
        temp_state = {
            'booking_info': {
                'location': data.get('location'),
                'check_in_date': data.get('check_in_date'),
                'check_out_date': data.get('check_out_date'),
                'adults': data.get('adults'),
                'children': data.get('children'),
                'rooms': data.get('rooms'),
                'guests_per_room': data.get('guests_per_room'),
                'amenities': data.get('amenities'),
                'min_price': data.get('min_price'),
                'max_price': data.get('max_price'),
                'min_stars': data.get('min_stars'),
                'max_stars': data.get('max_stars'),
                'min_rating': data.get('min_rating'),
                'max_rating': data.get('max_rating')
            }
        }
        
        hotels = webhook_system.search_hotels_from_dataset(temp_state)
        
        return jsonify({
            'success': True,
            'hotels': hotels,
            'count': len(hotels),
            'filters_applied': temp_state['booking_info']
        })
        
    except Exception as e:
        logger.error(f"Error in advanced hotel search: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/webhook/hotels/stats', methods=['GET'])
def get_hotel_stats():
    """Get hotel dataset statistics"""
    try:
        if webhook_system.hotel_df.empty:
            return jsonify({
                'success': False,
                'error': 'Hotel dataset not loaded'
            }), 404
        
        df = webhook_system.hotel_df
        
        stats = {
            'total_hotels': len(df),
            'locations': df['location'].nunique(),
            'star_ratings': df['stars'].value_counts().to_dict(),
            'price_stats': {
                'min': float(df['price_per_night'].min()),
                'max': float(df['price_per_night'].max()),
                'mean': float(df['price_per_night'].mean()),
                'median': float(df['price_per_night'].median())
            },
            'rating_stats': {
                'min': float(df['guest_rating'].min()),
                'max': float(df['guest_rating'].max()),
                'mean': float(df['guest_rating'].mean()),
                'median': float(df['guest_rating'].median())
            },
            'capacity_stats': {
                'max_adults': int(df['guests_adults'].max()),
                'max_children': int(df['guests_children'].max())
            }
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Error getting hotel stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/webhook/health', methods=['GET'])
def health():
    """Health check with enhanced hotel dataset information"""
    try:
        hotel_stats = {}
        if not webhook_system.hotel_df.empty:
            df = webhook_system.hotel_df
            hotel_stats = {
                'total_hotels': len(df),
                'locations': df['location'].nunique(),
                'price_range': {
                    'min': float(df['price_per_night'].min()),
                    'max': float(df['price_per_night'].max())
                },
                'star_ratings': df['stars'].value_counts().to_dict(),
                'avg_rating': float(df['guest_rating'].mean())
            }
        
        return jsonify({
            'status': 'healthy',
            'active_conversations': len(webhook_system.conversation_states),
            'hotel_dataset_loaded': not webhook_system.hotel_df.empty,
            'hotel_stats': hotel_stats,
            'livekit_configured': all([
                webhook_system.livekit_url,
                webhook_system.livekit_api_key,
                webhook_system.livekit_api_secret
            ]),
            'endpoints': {
                'hotel_search': '/webhook/hotels/search',
                'advanced_search': '/webhook/hotels/search/advanced',
                'locations': '/webhook/hotels/locations',
                'amenities': '/webhook/hotels/amenities',
                'price_range': '/webhook/hotels/price-range',
                'stats': '/webhook/hotels/stats'
            }
        })
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5004))
    app.run(debug=True, host='0.0.0.0', port=port)
