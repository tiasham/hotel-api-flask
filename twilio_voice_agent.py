#!/usr/bin/env python3
"""
Twilio Voice Agent - Hotel Booking Assistant
Handles phone calls with Hindi/Hinglish conversation
"""
from flask import Flask, request, jsonify
import requests
import json
import logging
from datetime import datetime
from typing import Dict, List
import re
import random
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class TwilioDialogueManager:
    """Twilio dialogue manager for phone calls"""
    
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.user_name = None
        self.ticket_number = random.choice(["SR3017861", "SR3117862", "SR3217863"])
        self.call_sid = None
        
        # Booking information
        self.booking_info = {
            "location": None,
            "check_in_date": None,
            "check_out_date": None,
            "adults": None,
            "children": None,
            "rooms": None,
            "amenities": None,
            "min_price": None,
            "max_price": None,
            "min_stars": None,
            "min_rating": None
        }
        
        # Local data - no API calls needed
        self.locations = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata", "Jaipur", "Goa", "Udaipur"]
        self.amenities = ["WiFi", "Pool", "Gym", "Restaurant", "Spa", "AC", "Parking", "Room Service", "Breakfast", "Business Center"]
        
        # Sample hotels for each location
        self.sample_hotels = {
            "Mumbai": [
                {"name": "Taj Mahal Palace", "stars": 5, "rating": 4.8, "price": 15000, "amenities": "WiFi,Pool,Gym,Restaurant"},
                {"name": "Oberoi Mumbai", "stars": 5, "rating": 4.7, "price": 12000, "amenities": "WiFi,Pool,Spa,Restaurant"},
                {"name": "ITC Maratha", "stars": 5, "rating": 4.6, "price": 10000, "amenities": "WiFi,Gym,Restaurant,AC"}
            ],
            "Delhi": [
                {"name": "The Leela Palace", "stars": 5, "rating": 4.9, "price": 18000, "amenities": "WiFi,Pool,Gym,Spa"},
                {"name": "Taj Palace Delhi", "stars": 5, "rating": 4.8, "price": 16000, "amenities": "WiFi,Pool,Restaurant,AC"},
                {"name": "The Imperial", "stars": 5, "rating": 4.7, "price": 14000, "amenities": "WiFi,Gym,Restaurant,Parking"}
            ],
            "Bangalore": [
                {"name": "The Oberoi Bangalore", "stars": 5, "rating": 4.8, "price": 11000, "amenities": "WiFi,Pool,Gym,Restaurant"},
                {"name": "Taj West End", "stars": 5, "rating": 4.7, "price": 9500, "amenities": "WiFi,Pool,Spa,AC"},
                {"name": "The Leela Palace Bangalore", "stars": 5, "rating": 4.6, "price": 13000, "amenities": "WiFi,Gym,Restaurant,Parking"}
            ]
        }
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def extract_booking_info(self, user_input: str) -> Dict:
        """Extract booking information from user input"""
        import re
        
        # Extract location
        for location in self.locations:
            if location.lower() in user_input.lower():
                self.booking_info["location"] = location
                logger.info(f"Location detected: {location}")
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
                self.booking_info["check_in_date"] = f"{dates[0][0]}-{dates[0][1]}-{dates[0][2]}"
                self.booking_info["check_out_date"] = f"{dates[1][0]}-{dates[1][1]}-{dates[1][2]}"
                logger.info(f"Dates detected: {self.booking_info['check_in_date']} to {self.booking_info['check_out_date']}")
                break
        
        # Extract number of adults
        adults_match = re.search(r'(\d+)\s*(adult|adults|person|people|लोग)', user_input.lower())
        if adults_match:
            self.booking_info["adults"] = int(adults_match.group(1))
            logger.info(f"Adults detected: {self.booking_info['adults']}")
        
        # Extract number of children
        children_match = re.search(r'(\d+)\s*(child|children|kid|kids|बच्चे)', user_input.lower())
        if children_match:
            self.booking_info["children"] = int(children_match.group(1))
            logger.info(f"Children detected: {self.booking_info['children']}")
        
        # Extract number of rooms
        rooms_match = re.search(r'(\d+)\s*(room|rooms|कमरे)', user_input.lower())
        if rooms_match:
            self.booking_info["rooms"] = int(rooms_match.group(1))
            logger.info(f"Rooms detected: {self.booking_info['rooms']}")
        
        # Extract amenities
        found_amenities = []
        for amenity in self.amenities:
            if amenity.lower() in user_input.lower():
                found_amenities.append(amenity)
        if found_amenities:
            self.booking_info["amenities"] = ",".join(found_amenities)
            logger.info(f"Amenities detected: {self.booking_info['amenities']}")
        
        # Extract price range
        price_match = re.search(r'(\d+)\s*(to|-)\s*(\d+)\s*(rs|rupees|price|रुपये)', user_input.lower())
        if price_match:
            self.booking_info["min_price"] = int(price_match.group(1))
            self.booking_info["max_price"] = int(price_match.group(3))
            logger.info(f"Price range detected: {self.booking_info['min_price']} to {self.booking_info['max_price']}")
        
        # Extract star rating
        stars_match = re.search(r'(\d+)\s*star', user_input.lower())
        if stars_match:
            self.booking_info["min_stars"] = int(stars_match.group(1))
            logger.info(f"Star rating detected: {self.booking_info['min_stars']}")
        
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
                self.user_name = name_match.group(1).title()
                logger.info(f"Name detected: {self.user_name}")
                break
        
        return self.booking_info
    
    def is_booking_complete(self) -> bool:
        """Check if all required booking information is collected"""
        required_fields = ["location", "adults"]
        return all(self.booking_info.get(field) for field in required_fields)
    
    def get_next_question(self) -> str:
        """Get the next question based on missing information"""
        if not self.booking_info["location"]:
            return "सबसे पहले बताइए — आपको किस शहर या एरिया में होटल चाहिए?"
        
        if not self.booking_info["check_in_date"]:
            return f"Great! {self.booking_info['location']} में होटल ढूंढेंगे। Check-in और check-out की dates क्या होंगी?"
        
        if not self.booking_info["adults"]:
            return "Adult और बच्चे — कितने लोग जा रहे हैं?"
        
        if not self.booking_info["rooms"]:
            return "आपको कितने rooms की ज़रूरत होगी?"
        
        if not self.user_name:
            return "Perfect! Booking शुरू करने से पहले — अपना नाम बता दीजिए।"
        
        return None
    
    def search_hotels_and_format_response(self) -> str:
        """Search hotels and format response in Hindi/Hinglish"""
        if not self.is_booking_complete():
            return self.get_next_question()
        
        location = self.booking_info["location"]
        
        # Get hotels for the location
        hotels = self.sample_hotels.get(location, [])
        
        if not hotels:
            # Fallback hotels for any location
            hotels = [
                {"name": f"Grand {location} Hotel", "stars": 4, "rating": 4.5, "price": 8000, "amenities": "WiFi,AC,Restaurant"},
                {"name": f"Comfort Inn {location}", "stars": 3, "rating": 4.2, "price": 5000, "amenities": "WiFi,AC,Parking"},
                {"name": f"Hotel {location} Plaza", "stars": 4, "rating": 4.3, "price": 7000, "amenities": "WiFi,Gym,Restaurant"}
            ]
        
        # Filter by price if specified
        if self.booking_info.get("min_price"):
            hotels = [h for h in hotels if h["price"] >= self.booking_info["min_price"]]
        if self.booking_info.get("max_price"):
            hotels = [h for h in hotels if h["price"] <= self.booking_info["max_price"]]
        
        # Filter by stars if specified
        if self.booking_info.get("min_stars"):
            hotels = [h for h in hotels if h["stars"] >= self.booking_info["min_stars"]]
        
        if not hotels:
            return f"Sorry {self.user_name}, {location} में आपके criteria के according कोई hotels नहीं मिले। क्या आप different dates या budget try करना चाहेंगे?"
        
        # Format response with top 2-3 hotels
        response = f"Perfect {self.user_name}! मैंने आपके लिए {len(hotels)} hotels ढूंढे हैं {location} में। "
        
        for i, hotel in enumerate(hotels[:3], 1):
            response += f"एक शानदार option है {hotel['name']}, ये एक {hotel['stars']}-star property है, guest rating है {hotel['rating']}/5, और price around {hotel['price']} rupees per night है। "
        
        response += f"मैंने {hotels[0]['name']} को आपके cart में डाल दिया है — आप आराम से review कर सकते हैं। जब आप ready हों, बस बता दीजिए — मैं तुरंत booking confirm कर दूँगा।"
        
        return response
    
    def generate_response(self, user_input: str) -> str:
        """Generate appropriate response based on user input"""
        self.add_message("user", user_input)
        
        # Extract booking information
        self.extract_booking_info(user_input)
        
        # Check if user wants to search for hotels
        search_keywords = ["hotel", "book", "search", "find", "stay", "accommodation", "होटल", "बुक", "ढूंढ"]
        is_search_request = any(keyword in user_input.lower() for keyword in search_keywords)
        
        if is_search_request or self.is_booking_complete():
            response = self.search_hotels_and_format_response()
        else:
            # Ask for missing information
            response = self.get_next_question()
        
        # If no specific response, use general conversation
        if not response:
            response = "Hey, welcome to Cleartrip Hotel Support! मैं राज बोल रहा हूँ — super excited हूँ आपकी hotel booking में help करने के लिए! बताइए, कहाँ जाना है आपको?"
        
        self.add_message("assistant", response)
        return response

# Global dialogue manager
dialogue_manager = TwilioDialogueManager()

def generate_twiml_response(speech_text: str, gather_input: bool = True) -> str:
    """Generate TwiML response for Twilio"""
    if gather_input:
        # Use Gather to collect speech input
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">{speech_text}</Say>
    <Gather input="speech" action="/handle_speech" method="POST" speechTimeout="auto" language="en-IN">
        <Say voice="alice" language="en-IN">Please speak after the beep.</Say>
    </Gather>
    <Say voice="alice" language="en-IN">We didn't receive any input. Goodbye!</Say>
</Response>"""
    else:
        # Just say something without gathering input
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">{speech_text}</Say>
</Response>"""
    
    return twiml

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Twilio Voice Agent for Hotel Booking',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'incoming_call': '/incoming_call',
            'handle_speech': '/handle_speech',
            'health': '/health'
        }
    })

@app.route('/incoming_call', methods=['POST'])
def incoming_call():
    """Handle incoming phone calls"""
    try:
        # Get call details from Twilio
        call_sid = request.form.get('CallSid')
        from_number = request.form.get('From')
        to_number = request.form.get('To')
        
        logger.info(f"Incoming call from {from_number} to {to_number}, CallSid: {call_sid}")
        
        # Store call SID in dialogue manager
        dialogue_manager.call_sid = call_sid
        
        # Initial greeting
        greeting = "Hey, welcome to Cleartrip Hotel Support! मैं राज बोल रहा हूँ — super excited हूँ आपकी hotel booking में help करने के लिए! बताइए, कहाँ जाना है आपको?"
        
        # Generate TwiML response
        twiml = generate_twiml_response(greeting, gather_input=True)
        
        return twiml, 200, {'Content-Type': 'text/xml'}
        
    except Exception as e:
        logger.error(f"Error handling incoming call: {e}")
        error_twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">Sorry, there was an error. Please try again later.</Say>
</Response>"""
        return error_twiml, 200, {'Content-Type': 'text/xml'}

@app.route('/handle_speech', methods=['POST'])
def handle_speech():
    """Handle speech input from user"""
    try:
        # Get speech input from Twilio
        speech_result = request.form.get('SpeechResult', '')
        confidence = request.form.get('Confidence', '0')
        call_sid = request.form.get('CallSid')
        
        logger.info(f"Speech received: '{speech_result}' (confidence: {confidence})")
        
        if not speech_result:
            # No speech detected, ask again
            response = "I didn't catch that. Could you please repeat?"
            twiml = generate_twiml_response(response, gather_input=True)
            return twiml, 200, {'Content-Type': 'text/xml'}
        
        # Generate response using dialogue manager
        agent_response = dialogue_manager.generate_response(speech_result)
        
        # Check if this is a booking confirmation
        if "booking confirm" in speech_result.lower() or "confirm" in speech_result.lower():
            # Final confirmation
            final_response = f"Perfect {dialogue_manager.user_name}! Your booking has been confirmed. You will receive a confirmation SMS shortly. Thank you for choosing Cleartrip!"
            twiml = generate_twiml_response(final_response, gather_input=False)
        else:
            # Continue conversation
            twiml = generate_twiml_response(agent_response, gather_input=True)
        
        return twiml, 200, {'Content-Type': 'text/xml'}
        
    except Exception as e:
        logger.error(f"Error handling speech: {e}")
        error_twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">Sorry, there was an error processing your request. Please try again.</Say>
    <Gather input="speech" action="/handle_speech" method="POST" speechTimeout="auto" language="en-IN">
        <Say voice="alice" language="en-IN">Please repeat your request.</Say>
    </Gather>
</Response>"""
        return error_twiml, 200, {'Content-Type': 'text/xml'}

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Twilio Voice Agent is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/test_conversation', methods=['POST'])
def test_conversation():
    """Test endpoint for conversation flow"""
    try:
        data = request.json
        user_input = data.get('message', '')
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        # Generate response using dialogue manager
        response = dialogue_manager.generate_response(user_input)
        
        return jsonify({
            'response': response,
            'booking_info': dialogue_manager.booking_info,
            'user_name': dialogue_manager.user_name
        })
        
    except Exception as e:
        logger.error(f"Test conversation error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port) 