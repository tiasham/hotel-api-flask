#!/usr/bin/env python3
"""
Simple Voice Agent - Hotel Booking Assistant
Works without LiveKit dependencies for immediate testing
"""
import requests
import json
import logging
from datetime import datetime
from typing import Dict, List
import re
import random

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

class HindiDialogueManager:
    """Manages conversation flow in Hindi/Hinglish"""
    
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.current_context: Dict = {}
        self.hotel_api = HotelAPI()
        self.user_name = None
        self.ticket_number = random.choice(["SR3017861", "SR3117862", "SR3217863"])
        
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
        
        # Available locations and amenities
        self.locations = self.hotel_api.get_locations()
        self.amenities = self.hotel_api.get_amenities()
        
        print(f"✅ Available locations: {self.locations}")
        print(f"✅ Available amenities: {self.amenities}")
    
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
                print(f"📍 Location detected: {location}")
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
                print(f"📅 Dates detected: {self.booking_info['check_in_date']} to {self.booking_info['check_out_date']}")
                break
        
        # Extract number of adults
        adults_match = re.search(r'(\d+)\s*(adult|adults|person|people|लोग)', user_input.lower())
        if adults_match:
            self.booking_info["adults"] = int(adults_match.group(1))
            print(f"👥 Adults detected: {self.booking_info['adults']}")
        
        # Extract number of children
        children_match = re.search(r'(\d+)\s*(child|children|kid|kids|बच्चे)', user_input.lower())
        if children_match:
            self.booking_info["children"] = int(children_match.group(1))
            print(f"👶 Children detected: {self.booking_info['children']}")
        
        # Extract number of rooms
        rooms_match = re.search(r'(\d+)\s*(room|rooms|कमरे)', user_input.lower())
        if rooms_match:
            self.booking_info["rooms"] = int(rooms_match.group(1))
            print(f"🏠 Rooms detected: {self.booking_info['rooms']}")
        
        # Extract amenities
        found_amenities = []
        for amenity in self.amenities:
            if amenity.lower() in user_input.lower():
                found_amenities.append(amenity)
        if found_amenities:
            self.booking_info["amenities"] = ",".join(found_amenities)
            print(f"🏊 Amenities detected: {self.booking_info['amenities']}")
        
        # Extract price range
        price_match = re.search(r'(\d+)\s*(to|-)\s*(\d+)\s*(rs|rupees|price|रुपये)', user_input.lower())
        if price_match:
            self.booking_info["min_price"] = int(price_match.group(1))
            self.booking_info["max_price"] = int(price_match.group(3))
            print(f"💰 Price range detected: {self.booking_info['min_price']} to {self.booking_info['max_price']}")
        
        # Extract star rating
        stars_match = re.search(r'(\d+)\s*star', user_input.lower())
        if stars_match:
            self.booking_info["min_stars"] = int(stars_match.group(1))
            print(f"⭐ Star rating detected: {self.booking_info['min_stars']}")
        
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
                print(f"👤 Name detected: {self.user_name}")
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
        
        print(f"🔍 Searching hotels with parameters: {self.booking_info}")
        
        # Search for hotels
        result = self.hotel_api.search_hotels(self.booking_info)
        
        if result.get("success") and result.get("result", {}).get("hotels"):
            hotels = result["result"]["hotels"]
            
            if not hotels:
                return f"Sorry {self.user_name}, {self.booking_info['location']} में आपके criteria के according कोई hotels नहीं मिले। क्या आप different dates या budget try करना चाहेंगे?"
            
            # Format response with top 2-3 hotels
            response = f"Perfect {self.user_name}! मैंने आपके लिए {len(hotels)} hotels ढूंढे हैं {self.booking_info['location']} में। "
            
            for i, hotel in enumerate(hotels[:3], 1):
                response += f"एक शानदार option है {hotel['name']}, ये एक {hotel['stars']}-star property है, guest rating है {hotel['guest_rating']}/5, और price around {hotel['price_per_night']} rupees per night है। "
            
            response += f"मैंने {hotels[0]['name']} को आपके cart में डाल दिया है — आप आराम से review कर सकते हैं। जब आप ready हों, बस बता दीजिए — मैं तुरंत booking confirm कर दूँगा।"
            
            return response
        else:
            return f"Sorry {self.user_name}, कुछ technical issue आ रहा है। क्या आप थोड़ी देर बाद try कर सकते हैं?"
    
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

def main():
    """Main function to run the voice agent simulation"""
    print("🏨 Hindi/Hinglish Hotel Booking Voice Agent")
    print("=" * 50)
    print("This is a simulation of the voice agent.")
    print("Type 'quit' to exit.")
    print()
    
    # Initialize dialogue manager
    dm = HindiDialogueManager()
    
    # Start conversation
    print("🤖 Agent: Hey, welcome to Cleartrip Hotel Support! मैं राज बोल रहा हूँ — super excited हूँ आपकी hotel booking में help करने के लिए! बताइए, कहाँ जाना है आपको?")
    print()
    
    while True:
        # Get user input
        user_input = input("👤 You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("🤖 Agent: Thank you for using Cleartrip! Have a great day! 👋")
            break
        
        if not user_input:
            continue
        
        # Generate response
        response = dm.generate_response(user_input)
        
        print(f"🤖 Agent: {response}")
        print()

if __name__ == "__main__":
    main() 