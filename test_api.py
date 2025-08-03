#!/usr/bin/env python3
"""
Test script for the Hotel API
Demonstrates various filtering and sorting capabilities
"""

import requests
import json

BASE_URL = "http://localhost:5001"

def test_api():
    """Test various API endpoints"""
    
    print("🏨 Hotel API Test Suite")
    print("=" * 50)
    
    # Test 1: Get API documentation
    print("\n1. Testing API Documentation:")
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API Version: {data['version']}")
        print(f"✅ Message: {data['message']}")
    else:
        print(f"❌ Failed to get API documentation: {response.status_code}")
    
    # Test 2: Get all hotels (should be sorted by rating desc)
    print("\n2. Testing Get All Hotels (sorted by rating desc):")
    response = requests.get(f"{BASE_URL}/api/hotels")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Total hotels: {data['total_count']}")
        print(f"✅ Sorting: {data['sorting']}")
        if data['hotels']:
            first_hotel = data['hotels'][0]
            print(f"✅ Top rated hotel: {first_hotel['name']} (Rating: {first_hotel['guest_rating']})")
    else:
        print(f"❌ Failed to get hotels: {response.status_code}")
    
    # Test 3: Filter by location
    print("\n3. Testing Location Filter (Mumbai):")
    response = requests.get(f"{BASE_URL}/api/hotels?location=Mumbai")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Hotels in Mumbai: {data['total_count']}")
        if data['hotels']:
            print(f"✅ First hotel: {data['hotels'][0]['name']}")
    else:
        print(f"❌ Failed to filter by location: {response.status_code}")
    
    # Test 4: Filter by star rating
    print("\n4. Testing Star Rating Filter (5 stars):")
    response = requests.get(f"{BASE_URL}/api/hotels?min_stars=5")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 5-star hotels: {data['total_count']}")
        if data['hotels']:
            print(f"✅ First 5-star hotel: {data['hotels'][0]['name']}")
    else:
        print(f"❌ Failed to filter by stars: {response.status_code}")
    
    # Test 5: Filter by price range
    print("\n5. Testing Price Filter (under 5000):")
    response = requests.get(f"{BASE_URL}/api/hotels?max_price=5000")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Hotels under 5000: {data['total_count']}")
        if data['hotels']:
            print(f"✅ Cheapest hotel: {data['hotels'][0]['name']} (₹{data['hotels'][0]['price_per_night']})")
    else:
        print(f"❌ Failed to filter by price: {response.status_code}")
    
    # Test 6: Filter by amenities
    print("\n6. Testing Amenities Filter (Gym):")
    response = requests.get(f"{BASE_URL}/api/hotels?amenities=Gym")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Hotels with Gym: {data['total_count']}")
        if data['hotels']:
            print(f"✅ First gym hotel: {data['hotels'][0]['name']}")
    else:
        print(f"❌ Failed to filter by amenities: {response.status_code}")
    
    # Test 7: Advanced filtering with custom sorting
    print("\n7. Testing Advanced Filtering (Delhi, sorted by price asc):")
    response = requests.get(f"{BASE_URL}/api/hotels/advanced?location=Delhi&sort_by=price_per_night&sort_order=asc")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Hotels in Delhi (price asc): {data['total_count']}")
        if data['hotels']:
            print(f"✅ Cheapest in Delhi: {data['hotels'][0]['name']} (₹{data['hotels'][0]['price_per_night']})")
            print(f"✅ Sorting: {data['sorting']['field']} {data['sorting']['order']}")
    else:
        print(f"❌ Failed to test advanced filtering: {response.status_code}")
    
    # Test 8: Get statistics
    print("\n8. Testing Statistics:")
    response = requests.get(f"{BASE_URL}/api/stats")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Total hotels: {data['total_hotels']}")
        print(f"✅ Average price: ₹{data['average_price']}")
        print(f"✅ Average rating: {data['average_rating']}")
        print(f"✅ Price range: ₹{data['price_range']['min']} - ₹{data['price_range']['max']}")
        print(f"✅ Locations: {data['locations_count']}")
    else:
        print(f"❌ Failed to get statistics: {response.status_code}")
    
    # Test 9: Get available locations
    print("\n9. Testing Available Locations:")
    response = requests.get(f"{BASE_URL}/api/locations")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Available locations: {len(data['locations'])}")
        print(f"✅ Sample locations: {', '.join(data['locations'][:5])}")
    else:
        print(f"❌ Failed to get locations: {response.status_code}")
    
    # Test 10: Get available amenities
    print("\n10. Testing Available Amenities:")
    response = requests.get(f"{BASE_URL}/api/amenities")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Available amenities: {len(data['amenities'])}")
        print(f"✅ Sample amenities: {', '.join(data['amenities'][:5])}")
    else:
        print(f"❌ Failed to get amenities: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 API Test Suite Completed!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API. Make sure the Flask app is running on http://localhost:5001")
    except Exception as e:
        print(f"❌ Error: {e}") 