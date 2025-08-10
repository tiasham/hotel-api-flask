#!/usr/bin/env python3
"""
Retell-Specific MCP Server - Enhanced Hotel Booking System
"""
from flask import Flask, request, jsonify
import pandas as pd
import json
from datetime import datetime, timedelta
import os
import uuid
import re

app = Flask(__name__)

class RetellSpecificServer:
    def __init__(self):
        self.csv_file = 'Hotel_Dataset.csv'
        self.bookings_file = 'bookings.json'
        self.create_sample_data_if_needed()
        self.load_bookings()
    
    def create_sample_data_if_needed(self):
        """Create comprehensive sample hotel data if CSV doesn't exist"""
        if not os.path.exists(self.csv_file):
            hotels_data = {
                'hotel_id': [
                    'HOTEL001', 'HOTEL002', 'HOTEL003', 'HOTEL004', 'HOTEL005',
                    'HOTEL006', 'HOTEL007', 'HOTEL008', 'HOTEL009', 'HOTEL010',
                    'HOTEL011', 'HOTEL012', 'HOTEL013', 'HOTEL014', 'HOTEL015'
                ],
                'name': [
                    'Taj Palace Mumbai', 'Oberoi Delhi', 'ITC Gardenia Bangalore', 
                    'Leela Palace Mumbai', 'The Imperial Delhi', 'Taj West End Bangalore',
                    'Four Seasons Mumbai', 'The Leela Palace Delhi', 'Park Hyatt Bangalore',
                    'Raffles Mumbai', 'Aman New Delhi', 'The Oberoi Bangalore',
                    'Taj Lands End Mumbai', 'The Claridges Delhi', 'The Ritz-Carlton Bangalore'
                ],
                'location': [
                    'Mumbai', 'Delhi', 'Bangalore', 'Mumbai', 'Delhi',
                    'Bangalore', 'Mumbai', 'Delhi', 'Bangalore', 'Mumbai',
                    'Delhi', 'Bangalore', 'Mumbai', 'Delhi', 'Bangalore'
                ],
                'address': [
                    'Apollo Bunder, Mumbai', 'Dr. Zakir Hussain Marg, Delhi', 'Residency Road, Bangalore',
                    'Sahar, Mumbai', 'Janpath, Delhi', 'Race Course Road, Bangalore',
                    'Worli, Mumbai', 'Chanakyapuri, Delhi', 'Vittal Mallya Road, Bangalore',
                    'BKC, Mumbai', 'Lodhi Road, Delhi', 'MG Road, Bangalore',
                    'Bandra West, Mumbai', 'Aurangzeb Road, Delhi', 'MG Road, Bangalore'
                ],
                'stars': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                'guest_rating': [4.8, 4.9, 4.7, 4.8, 4.9, 4.6, 4.8, 4.9, 4.7, 4.8, 4.9, 4.7, 4.8, 4.9, 4.7],
                'amenities': [
                    'Gym,Pool,Restaurant,Spa,WiFi,Parking,Concierge',
                    'Spa,Gym,Restaurant,WiFi,Parking,Concierge,Bar',
                    'Pool,Restaurant,Gym,WiFi,Parking,Concierge,Spa',
                    'Gym,Restaurant,Spa,WiFi,Parking,Concierge,Pool',
                    'Spa,Pool,Gym,Restaurant,WiFi,Parking,Concierge',
                    'Gym,Pool,Restaurant,WiFi,Parking,Concierge,Spa',
                    'Spa,Gym,Restaurant,WiFi,Parking,Concierge,Pool',
                    'Pool,Restaurant,Gym,WiFi,Parking,Concierge,Spa',
                    'Gym,Restaurant,Spa,WiFi,Parking,Concierge,Pool',
                    'Spa,Pool,Gym,Restaurant,WiFi,Parking,Concierge',
                    'Gym,Pool,Restaurant,WiFi,Parking,Concierge,Spa',
                    'Spa,Gym,Restaurant,WiFi,Parking,Concierge,Pool',
                    'Pool,Restaurant,Gym,WiFi,Parking,Concierge,Spa',
                    'Gym,Restaurant,Spa,WiFi,Parking,Concierge,Pool',
                    'Spa,Pool,Gym,Restaurant,WiFi,Parking,Concierge'
                ],
                'price_per_night': [15000, 18000, 12000, 16000, 20000, 14000, 17000, 19000, 13000, 22000, 25000, 11000, 14500, 17500, 13500],
                'max_adults': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                'max_children': [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                'room_types': [
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential',
                    'Deluxe,Suite,Presidential'
                ],
                'description': [
                    'Luxury hotel with sea view in South Mumbai',
                    'Historic luxury hotel in the heart of Delhi',
                    'Garden-themed luxury hotel in Bangalore',
                    'Airport-adjacent luxury hotel in Mumbai',
                    'Heritage luxury hotel on Janpath',
                    'Colonial-style luxury hotel in Bangalore',
                    'Modern luxury hotel in Worli',
                    'Diplomatic enclave luxury hotel',
                    'Contemporary luxury hotel on Vittal Mallya Road',
                    'Ultra-luxury hotel in BKC',
                    'Exclusive luxury hotel on Lodhi Road',
                    'Downtown luxury hotel on MG Road',
                    'Seaside luxury hotel in Bandra',
                    'Heritage luxury hotel on Aurangzeb Road',
                    'Modern luxury hotel in Bangalore CBD'
                ]
            }
            df = pd.DataFrame(hotels_data)
            df.to_csv(self.csv_file, index=False)
    
    def load_bookings(self):
        """Load existing bookings from JSON file"""
        if os.path.exists(self.bookings_file):
            try:
                with open(self.bookings_file, 'r') as f:
                    self.bookings = json.load(f)
            except:
                self.bookings = []
        else:
            self.bookings = []
    
    def save_bookings(self):
        """Save bookings to JSON file"""
        with open(self.bookings_file, 'w') as f:
            json.dump(self.bookings, f, indent=2)
    
    def validate_date(self, date_str):
        """Validate date format and ensure it's in the future"""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            if date_obj.date() < datetime.now().date():
                return False, "Date must be in the future"
            return True, date_obj
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
    
    def validate_dates(self, check_in, check_out):
        """Validate check-in and check-out dates"""
        valid_in, in_date = self.validate_date(check_in)
        if not valid_in:
            return False, in_date
        
        valid_out, out_date = self.validate_date(check_out)
        if not valid_out:
            return False, out_date
        
        if in_date >= out_date:
            return False, "Check-out date must be after check-in date"
        
        return True, (in_date, out_date)
    
    def load_data(self):
        """Load hotel data from CSV"""
        try:
            return pd.read_csv(self.csv_file)
        except Exception as e:
            self.create_sample_data_if_needed()
            return pd.read_csv(self.csv_file)
    
    def search_hotels(self, parameters):
        """Enhanced search hotels based on parameters"""
        try:
            df = self.load_data()
            
            # Location filter
            if 'location' in parameters and parameters['location']:
                df = df[df['location'].str.contains(parameters['location'], case=False, na=False)]
            
            # Capacity filters
            if 'adults' in parameters and parameters['adults']:
                try:
                    adults = int(parameters['adults'])
                    df = df[df['max_adults'] >= adults]
                except:
                    pass
            
            if 'children' in parameters and parameters['children']:
                try:
                    children = int(parameters['children'])
                    df = df[df['max_children'] >= children]
                except:
                    pass
            
            # Amenities filter
            if 'amenities' in parameters and parameters['amenities']:
                amenities = parameters['amenities'].split(',')
                for amenity in amenities:
                    df = df[df['amenities'].str.contains(amenity.strip(), case=False, na=False)]
            
            # Price filters
            if 'min_price' in parameters and parameters['min_price']:
                try:
                    min_price = float(parameters['min_price'])
                    df = df[df['price_per_night'] >= min_price]
                except:
                    pass
            
            if 'max_price' in parameters and parameters['max_price']:
                try:
                    max_price = float(parameters['max_price'])
                    df = df[df['price_per_night'] <= max_price]
                except:
                    pass
            
            # Rating filters
            if 'min_stars' in parameters and parameters['min_stars']:
                try:
                    min_stars = int(parameters['min_stars'])
                    df = df[df['stars'] >= min_stars]
                except:
                    pass
            
            if 'min_rating' in parameters and parameters['min_rating']:
                try:
                    min_rating = float(parameters['min_rating'])
                    df = df[df['guest_rating'] >= min_rating]
                except:
                    pass
            
            # Date availability check
            if 'check_in' in parameters and 'check_out' in parameters:
                valid, dates = self.validate_dates(parameters['check_in'], parameters['check_out'])
                if valid:
                    # Check booking conflicts
                    available_hotels = []
                    for _, hotel in df.iterrows():
                        if self.is_hotel_available(hotel['hotel_id'], parameters['check_in'], parameters['check_out']):
                            available_hotels.append(hotel)
                    df = pd.DataFrame(available_hotels) if available_hotels else pd.DataFrame()
            
            # Sort by rating and limit results
            if not df.empty:
                df = df.sort_values('guest_rating', ascending=False).head(10)
            
            hotels = df.to_dict('records')
            
            return {
                'total_matches': len(df),
                'hotels': hotels,
                'search_criteria': parameters,
                'message': f"Found {len(hotels)} hotels matching your criteria"
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Error occurred while searching hotels'
            }
    
    def is_hotel_available(self, hotel_id, check_in, check_out):
        """Check if hotel is available for given dates"""
        for booking in self.bookings:
            if booking['hotel_id'] == hotel_id:
                # Check for date overlap
                booking_in = datetime.strptime(booking['check_in'], '%Y-%m-%d')
                booking_out = datetime.strptime(booking['check_out'], '%Y-%m-%d')
                requested_in = datetime.strptime(check_in, '%Y-%m-%d')
                requested_out = datetime.strptime(check_out, '%Y-%m-%d')
                
                if (requested_in < booking_out and requested_out > booking_in):
                    return False
        return True
    
    def get_hotel_details(self, hotel_id):
        """Get detailed information about a specific hotel"""
        try:
            df = self.load_data()
            hotel = df[df['hotel_id'] == hotel_id]
            
            if hotel.empty:
                return {
                    'error': 'Hotel not found',
                    'message': f'No hotel found with ID: {hotel_id}'
                }
            
            hotel_data = hotel.iloc[0].to_dict()
            
            # Add availability for next 30 days
            availability = []
            for i in range(30):
                date = datetime.now().date() + timedelta(days=i)
                date_str = date.strftime('%Y-%m-%d')
                available = self.is_hotel_available(hotel_id, date_str, (date + timedelta(days=1)).strftime('%Y-%m-%d'))
                availability.append({
                    'date': date_str,
                    'available': available
                })
            
            hotel_data['availability'] = availability
            
            return {
                'hotel': hotel_data,
                'message': 'Hotel details retrieved successfully'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Error occurred while retrieving hotel details'
            }
    
    def create_booking(self, booking_data):
        """Create a new hotel booking"""
        try:
            # Validate required fields
            required_fields = ['hotel_id', 'guest_name', 'guest_email', 'check_in', 'check_out', 'adults']
            for field in required_fields:
                if field not in booking_data or not booking_data[field]:
                    return {
                        'error': f'Missing required field: {field}',
                        'message': 'Please provide all required booking information'
                    }
            
            # Validate dates
            valid, dates = self.validate_dates(booking_data['check_in'], booking_data['check_out'])
            if not valid:
                return {
                    'error': 'Invalid dates',
                    'message': dates
                }
            
            # Check hotel availability
            if not self.is_hotel_available(booking_data['hotel_id'], booking_data['check_in'], booking_data['check_out']):
                return {
                    'error': 'Hotel not available',
                    'message': 'Hotel is not available for the selected dates'
                }
            
            # Validate email format
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, booking_data['guest_email']):
                return {
                    'error': 'Invalid email format',
                    'message': 'Please provide a valid email address'
                }
            
            # Create booking
            booking = {
                'booking_id': str(uuid.uuid4()),
                'hotel_id': booking_data['hotel_id'],
                'guest_name': booking_data['guest_name'],
                'guest_email': booking_data['guest_email'],
                'guest_phone': booking_data.get('guest_phone', ''),
                'check_in': booking_data['check_in'],
                'check_out': booking_data['check_out'],
                'adults': int(booking_data['adults']),
                'children': int(booking_data.get('children', 0)),
                'room_type': booking_data.get('room_type', 'Deluxe'),
                'special_requests': booking_data.get('special_requests', ''),
                'booking_date': datetime.now().isoformat(),
                'status': 'confirmed'
            }
            
            # Calculate total price
            df = self.load_data()
            hotel = df[df['hotel_id'] == booking_data['hotel_id']].iloc[0]
            nights = (dates[1] - dates[0]).days
            booking['total_price'] = hotel['price_per_night'] * nights
            booking['price_per_night'] = hotel['price_per_night']
            
            self.bookings.append(booking)
            self.save_bookings()
            
            return {
                'booking': booking,
                'message': 'Booking created successfully'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Error occurred while creating booking'
            }
    
    def get_booking(self, booking_id):
        """Get booking details by booking ID"""
        try:
            for booking in self.bookings:
                if booking['booking_id'] == booking_id:
                    return {
                        'booking': booking,
                        'message': 'Booking retrieved successfully'
                    }
            
            return {
                'error': 'Booking not found',
                'message': f'No booking found with ID: {booking_id}'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Error occurred while retrieving booking'
            }
    
    def cancel_booking(self, booking_id):
        """Cancel a booking"""
        try:
            for i, booking in enumerate(self.bookings):
                if booking['booking_id'] == booking_id:
                    if booking['status'] == 'cancelled':
                        return {
                            'error': 'Booking already cancelled',
                            'message': 'This booking has already been cancelled'
                        }
                    
                    # Check if booking is within 24 hours
                    booking_date = datetime.fromisoformat(booking['booking_date'])
                    if datetime.now() - booking_date < timedelta(hours=24):
                        self.bookings[i]['status'] = 'cancelled'
                        self.save_bookings()
                        return {
                            'booking': self.bookings[i],
                            'message': 'Booking cancelled successfully'
                        }
                    else:
                        return {
                            'error': 'Cancellation not allowed',
                            'message': 'Bookings can only be cancelled within 24 hours of creation'
                        }
            
            return {
                'error': 'Booking not found',
                'message': f'No booking found with ID: {booking_id}'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Error occurred while cancelling booking'
            }
    
    def get_locations(self):
        """Get all available locations"""
        try:
            df = self.load_data()
            locations = df['location'].unique().tolist()
            return {
                'locations': locations,
                'count': len(locations)
            }
        except Exception as e:
            return {
                'error': str(e),
                'locations': [],
                'count': 0
            }
    
    def get_amenities(self):
        """Get all available amenities"""
        try:
            df = self.load_data()
            all_amenities = []
            for amenities_str in df['amenities']:
                amenities = amenities_str.split(',')
                all_amenities.extend([a.strip() for a in amenities])
            
            unique_amenities = list(set(all_amenities))
            return {
                'amenities': unique_amenities,
                'count': len(unique_amenities)
            }
        except Exception as e:
            return {
                'error': str(e),
                'amenities': [],
                'count': 0
            }
    
    def get_room_types(self):
        """Get all available room types"""
        try:
            df = self.load_data()
            all_room_types = []
            for room_types_str in df['room_types']:
                room_types = room_types_str.split(',')
                all_room_types.extend([rt.strip() for rt in room_types])
            
            unique_room_types = list(set(all_room_types))
            return {
                'room_types': unique_room_types,
                'count': len(unique_room_types)
            }
        except Exception as e:
            return {
                'error': str(e),
                'room_types': [],
                'count': 0
            }

# Initialize the server
server = RetellSpecificServer()

@app.route('/')
def home():
    """Root endpoint"""
    return jsonify({
        'message': 'Enhanced Retell-Specific MCP Server',
        'version': '2.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'tools': '/tools',
            'execute': '/execute'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Enhanced Retell-Specific MCP Server is running',
        'timestamp': datetime.now().isoformat(),
        'hotels_count': len(server.load_data()),
        'bookings_count': len(server.bookings)
    })

@app.route('/tools', methods=['GET'])
def get_tools():
    """Get available tools - Enhanced Retell-specific format"""
    return jsonify({
        "tools": [
            {
                "name": "searchHotels",
                "description": "Search for hotels based on customer preferences with availability check",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City or location"},
                        "adults": {"type": "integer", "description": "Number of adults"},
                        "children": {"type": "integer", "description": "Number of children"},
                        "amenities": {"type": "string", "description": "Preferred amenities (comma-separated)"},
                        "min_price": {"type": "number", "description": "Minimum price per night"},
                        "max_price": {"type": "number", "description": "Maximum price per night"},
                        "min_stars": {"type": "integer", "description": "Minimum star rating (1-5)"},
                        "min_rating": {"type": "number", "description": "Minimum guest rating (0.0-5.0)"},
                        "check_in": {"type": "string", "description": "Check-in date (YYYY-MM-DD)"},
                        "check_out": {"type": "string", "description": "Check-out date (YYYY-MM-DD)"}
                    },
                    "required": ["location", "adults"]
                }
            },
            {
                "name": "getHotelDetails",
                "description": "Get detailed information about a specific hotel including availability",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "hotel_id": {"type": "string", "description": "Hotel ID"}
                    },
                    "required": ["hotel_id"]
                }
            },
            {
                "name": "createBooking",
                "description": "Create a new hotel booking",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "hotel_id": {"type": "string", "description": "Hotel ID"},
                        "guest_name": {"type": "string", "description": "Guest full name"},
                        "guest_email": {"type": "string", "description": "Guest email address"},
                        "guest_phone": {"type": "string", "description": "Guest phone number"},
                        "check_in": {"type": "string", "description": "Check-in date (YYYY-MM-DD)"},
                        "check_out": {"type": "string", "description": "Check-out date (YYYY-MM-DD)"},
                        "adults": {"type": "integer", "description": "Number of adults"},
                        "children": {"type": "integer", "description": "Number of children"},
                        "room_type": {"type": "string", "description": "Room type (Deluxe, Suite, Presidential)"},
                        "special_requests": {"type": "string", "description": "Special requests or notes"}
                    },
                    "required": ["hotel_id", "guest_name", "guest_email", "check_in", "check_out", "adults"]
                }
            },
            {
                "name": "getBooking",
                "description": "Get booking details by booking ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "booking_id": {"type": "string", "description": "Booking ID"}
                    },
                    "required": ["booking_id"]
                }
            },
            {
                "name": "cancelBooking",
                "description": "Cancel a booking (within 24 hours of creation)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "booking_id": {"type": "string", "description": "Booking ID"}
                    },
                    "required": ["booking_id"]
                }
            },
            {
                "name": "getLocations",
                "description": "Get all available hotel locations",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "getAmenities",
                "description": "Get all available hotel amenities",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "getRoomTypes",
                "description": "Get all available room types",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
    })

@app.route('/execute', methods=['POST'])
def execute_tool():
    """Execute a tool - Enhanced Retell-specific format"""
    try:
        data = request.json
        tool_name = data.get('name')
        arguments = data.get('arguments', {})
        
        if tool_name == 'searchHotels':
            result = server.search_hotels(arguments)
            return jsonify({
                'success': True,
                'result': result
            })
        
        elif tool_name == 'getHotelDetails':
            result = server.get_hotel_details(arguments.get('hotel_id'))
            return jsonify({
                'success': True,
                'result': result
            })
        
        elif tool_name == 'createBooking':
            result = server.create_booking(arguments)
            return jsonify({
                'success': True,
                'result': result
            })
        
        elif tool_name == 'getBooking':
            result = server.get_booking(arguments.get('booking_id'))
            return jsonify({
                'success': True,
                'result': result
            })
        
        elif tool_name == 'cancelBooking':
            result = server.cancel_booking(arguments.get('booking_id'))
            return jsonify({
                'success': True,
                'result': result
            })
        
        elif tool_name == 'getLocations':
            result = server.get_locations()
            return jsonify({
                'success': True,
                'result': result
            })
        
        elif tool_name == 'getAmenities':
            result = server.get_amenities()
            return jsonify({
                'success': True,
                'result': result
            })
        
        elif tool_name == 'getRoomTypes':
            result = server.get_room_types()
            return jsonify({
                'success': True,
                'result': result
            })
        
        else:
            return jsonify({
                'success': False,
                'error': f'Unknown tool: {tool_name}'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port) 