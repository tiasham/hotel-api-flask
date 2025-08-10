#!/usr/bin/env python3
"""
Test script for Enhanced Retell-Specific MCP Server
"""
import requests
import json
import time
from datetime import datetime, timedelta

# Server configuration
BASE_URL = "http://localhost:5001"

def test_server_health():
    """Test server health endpoint"""
    print("=== Testing Server Health ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server is healthy")
            print(f"   Hotels count: {data.get('hotels_count', 'N/A')}")
            print(f"   Bookings count: {data.get('bookings_count', 'N/A')}")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return False

def test_get_tools():
    """Test getting available tools"""
    print("\n=== Testing Get Tools ===")
    try:
        response = requests.get(f"{BASE_URL}/tools")
        if response.status_code == 200:
            data = response.json()
            tools = data.get('tools', [])
            print(f"✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"   - {tool['name']}: {tool['description']}")
            return tools
        else:
            print(f"❌ Failed to get tools: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting tools: {e}")
        return []

def test_get_locations():
    """Test getting available locations"""
    print("\n=== Testing Get Locations ===")
    try:
        response = requests.post(f"{BASE_URL}/execute", json={
            "name": "getLocations",
            "arguments": {}
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data['result']
                print(f"✅ Found {result['count']} locations:")
                for location in result['locations']:
                    print(f"   - {location}")
                return result['locations']
            else:
                print(f"❌ Failed to get locations: {data.get('error')}")
                return []
        else:
            print(f"❌ Request failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting locations: {e}")
        return []

def test_get_amenities():
    """Test getting available amenities"""
    print("\n=== Testing Get Amenities ===")
    try:
        response = requests.post(f"{BASE_URL}/execute", json={
            "name": "getAmenities",
            "arguments": {}
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data['result']
                print(f"✅ Found {result['count']} amenities:")
                for amenity in result['amenities']:
                    print(f"   - {amenity}")
                return result['amenities']
            else:
                print(f"❌ Failed to get amenities: {data.get('error')}")
                return []
        else:
            print(f"❌ Request failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting amenities: {e}")
        return []

def test_get_room_types():
    """Test getting available room types"""
    print("\n=== Testing Get Room Types ===")
    try:
        response = requests.post(f"{BASE_URL}/execute", json={
            "name": "getRoomTypes",
            "arguments": {}
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data['result']
                print(f"✅ Found {result['count']} room types:")
                for room_type in result['room_types']:
                    print(f"   - {room_type}")
                return result['room_types']
            else:
                print(f"❌ Failed to get room types: {data.get('error')}")
                return []
        else:
            print(f"❌ Request failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting room types: {e}")
        return []

def test_search_hotels():
    """Test hotel search functionality"""
    print("\n=== Testing Hotel Search ===")
    
    # Test 1: Basic search
    print("1. Basic search in Mumbai:")
    try:
        response = requests.post(f"{BASE_URL}/execute", json={
            "name": "searchHotels",
            "arguments": {
                "location": "Mumbai",
                "adults": 2
            }
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data['result']
                print(f"✅ Found {result['total_matches']} hotels")
                for hotel in result['hotels'][:3]:  # Show first 3
                    print(f"   - {hotel['name']} ({hotel['stars']}★, ₹{hotel['price_per_night']})")
            else:
                print(f"❌ Search failed: {data.get('error')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error in basic search: {e}")
    
    # Test 2: Advanced search with filters
    print("\n2. Advanced search with filters:")
    try:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        day_after = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        
        response = requests.post(f"{BASE_URL}/execute", json={
            "name": "searchHotels",
            "arguments": {
                "location": "Delhi",
                "adults": 2,
                "children": 1,
                "amenities": "Spa,Pool",
                "min_price": 15000,
                "max_price": 25000,
                "min_stars": 5,
                "min_rating": 4.5,
                "check_in": tomorrow,
                "check_out": day_after
            }
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data['result']
                print(f"✅ Found {result['total_matches']} hotels with filters")
                for hotel in result['hotels']:
                    print(f"   - {hotel['name']} ({hotel['stars']}★, ₹{hotel['price_per_night']}, Rating: {hotel['guest_rating']})")
            else:
                print(f"❌ Advanced search failed: {data.get('error')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error in advanced search: {e}")

def test_get_hotel_details():
    """Test getting detailed hotel information"""
    print("\n=== Testing Get Hotel Details ===")
    try:
        response = requests.post(f"{BASE_URL}/execute", json={
            "name": "getHotelDetails",
            "arguments": {
                "hotel_id": "HOTEL001"
            }
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data['result']
                hotel = result['hotel']
                print(f"✅ Hotel details for {hotel['name']}:")
                print(f"   Location: {hotel['location']}")
                print(f"   Address: {hotel['address']}")
                print(f"   Stars: {hotel['stars']}★")
                print(f"   Rating: {hotel['guest_rating']}")
                print(f"   Price: ₹{hotel['price_per_night']}/night")
                print(f"   Amenities: {hotel['amenities']}")
                print(f"   Room Types: {hotel['room_types']}")
                print(f"   Description: {hotel['description']}")
                
                # Show availability for next 5 days
                availability = hotel.get('availability', [])[:5]
                print(f"   Availability (next 5 days):")
                for day in availability:
                    status = "✅ Available" if day['available'] else "❌ Booked"
                    print(f"     {day['date']}: {status}")
                
                return hotel['hotel_id']
            else:
                print(f"❌ Failed to get hotel details: {data.get('error')}")
                return None
        else:
            print(f"❌ Request failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error getting hotel details: {e}")
        return None

def test_create_booking():
    """Test creating a hotel booking"""
    print("\n=== Testing Create Booking ===")
    try:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        day_after = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        
        response = requests.post(f"{BASE_URL}/execute", json={
            "name": "createBooking",
            "arguments": {
                "hotel_id": "HOTEL001",
                "guest_name": "John Doe",
                "guest_email": "john.doe@example.com",
                "guest_phone": "+91-9876543210",
                "check_in": tomorrow,
                "check_out": day_after,
                "adults": 2,
                "children": 1,
                "room_type": "Deluxe",
                "special_requests": "Early check-in preferred"
            }
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data['result']
                booking = result['booking']
                print(f"✅ Booking created successfully!")
                print(f"   Booking ID: {booking['booking_id']}")
                print(f"   Guest: {booking['guest_name']}")
                print(f"   Hotel: {booking['hotel_id']}")
                print(f"   Check-in: {booking['check_in']}")
                print(f"   Check-out: {booking['check_out']}")
                print(f"   Total Price: ₹{booking['total_price']}")
                print(f"   Status: {booking['status']}")
                return booking['booking_id']
            else:
                print(f"❌ Failed to create booking: {data.get('error')}")
                return None
        else:
            print(f"❌ Request failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error creating booking: {e}")
        return None

def test_get_booking(booking_id):
    """Test getting booking details"""
    if not booking_id:
        print("❌ No booking ID provided")
        return
    
    print(f"\n=== Testing Get Booking ({booking_id}) ===")
    try:
        response = requests.post(f"{BASE_URL}/execute", json={
            "name": "getBooking",
            "arguments": {
                "booking_id": booking_id
            }
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data['result']
                booking = result['booking']
                print(f"✅ Booking details retrieved:")
                print(f"   Booking ID: {booking['booking_id']}")
                print(f"   Guest: {booking['guest_name']} ({booking['guest_email']})")
                print(f"   Hotel: {booking['hotel_id']}")
                print(f"   Dates: {booking['check_in']} to {booking['check_out']}")
                print(f"   Guests: {booking['adults']} adults, {booking['children']} children")
                print(f"   Room Type: {booking['room_type']}")
                print(f"   Total Price: ₹{booking['total_price']}")
                print(f"   Status: {booking['status']}")
                if booking.get('special_requests'):
                    print(f"   Special Requests: {booking['special_requests']}")
            else:
                print(f"❌ Failed to get booking: {data.get('error')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting booking: {e}")

def test_cancel_booking(booking_id):
    """Test cancelling a booking"""
    if not booking_id:
        print("❌ No booking ID provided")
        return
    
    print(f"\n=== Testing Cancel Booking ({booking_id}) ===")
    try:
        response = requests.post(f"{BASE_URL}/execute", json={
            "name": "cancelBooking",
            "arguments": {
                "booking_id": booking_id
            }
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data['result']
                booking = result['booking']
                print(f"✅ Booking cancelled successfully!")
                print(f"   Booking ID: {booking['booking_id']}")
                print(f"   Status: {booking['status']}")
            else:
                print(f"❌ Failed to cancel booking: {data.get('error')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error cancelling booking: {e}")

def test_error_handling():
    """Test error handling scenarios"""
    print("\n=== Testing Error Handling ===")
    
    # Test 1: Invalid hotel ID
    print("1. Testing invalid hotel ID:")
    try:
        response = requests.post(f"{BASE_URL}/execute", json={
            "name": "getHotelDetails",
            "arguments": {
                "hotel_id": "INVALID_HOTEL"
            }
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                result = data['result']
                print(f"❌ Should have failed but didn't")
            else:
                print(f"✅ Correctly handled invalid hotel ID: {data['result'].get('error')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error in invalid hotel test: {e}")
    
    # Test 2: Invalid booking data
    print("\n2. Testing invalid booking data:")
    try:
        response = requests.post(f"{BASE_URL}/execute", json={
            "name": "createBooking",
            "arguments": {
                "hotel_id": "HOTEL001",
                "guest_name": "Test User",
                "guest_email": "invalid-email",
                "check_in": "2024-01-01",  # Past date
                "check_out": "2024-01-02",
                "adults": 2
            }
        })
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"❌ Should have failed but didn't")
            else:
                print(f"✅ Correctly handled invalid booking data: {data['result'].get('error')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error in invalid booking test: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Enhanced Retell-Specific MCP Server Tests")
    print("=" * 60)
    
    # Check if server is running
    if not test_server_health():
        print("❌ Server is not running. Please start the server first.")
        return
    
    # Test basic functionality
    tools = test_get_tools()
    if not tools:
        print("❌ Failed to get tools. Stopping tests.")
        return
    
    locations = test_get_locations()
    amenities = test_get_amenities()
    room_types = test_get_room_types()
    
    # Test hotel search
    test_search_hotels()
    
    # Test hotel details
    hotel_id = test_get_hotel_details()
    
    # Test booking functionality
    booking_id = test_create_booking()
    if booking_id:
        test_get_booking(booking_id)
        test_cancel_booking(booking_id)
    
    # Test error handling
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")

if __name__ == "__main__":
    main() 