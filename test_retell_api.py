#!/usr/bin/env python3
"""
Test script for Retell-compatible API endpoints
"""

import requests
import json

BASE_URL = "https://hotel-api-flask-production.up.railway.app"

def test_retell_endpoints():
    """Test the API endpoints that Retell will use"""
    
    print("🧪 Testing Retell-Compatible API Endpoints")
    print("=" * 50)
    
    # Test 1: OpenAPI Specification
    print("\n1. Testing OpenAPI Specification:")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            print("✅ OpenAPI specification accessible")
            spec = response.json()
            print(f"✅ API Title: {spec['info']['title']}")
            print(f"✅ Version: {spec['info']['version']}")
        else:
            print(f"❌ OpenAPI spec failed: {response.status_code}")
    except Exception as e:
        print(f"❌ OpenAPI spec error: {e}")
    
    # Test 2: Search Hotels (with required parameters)
    print("\n2. Testing Hotel Search (with required parameters):")
    try:
        params = {
            'location': 'Mumbai',
            'check_in_date': '2024-08-15',
            'check_out_date': '2024-08-20',
            'adults': 2
        }
        response = requests.get(f"{BASE_URL}/api/hotels/search", params=params)
        if response.status_code == 200:
            data = response.json()
            print("✅ Hotel search successful")
            print(f"✅ Total matches: {data['search_results']['total_matches']}")
            print(f"✅ Top 5 hotels returned: {len(data['search_results']['top_5_hotels'])}")
        else:
            print(f"❌ Hotel search failed: {response.status_code}")
            print(f"❌ Response: {response.text}")
    except Exception as e:
        print(f"❌ Hotel search error: {e}")
    
    # Test 3: Search Hotels (with all parameters)
    print("\n3. Testing Hotel Search (with all parameters):")
    try:
        params = {
            'location': 'Delhi',
            'check_in_date': '2024-08-10',
            'check_out_date': '2024-08-15',
            'adults': 2,
            'children': 1,
            'amenities': 'Gym,Pool',
            'max_price': 5000,
            'min_stars': 4,
            'min_rating': 4.0
        }
        response = requests.get(f"{BASE_URL}/api/hotels/search", params=params)
        if response.status_code == 200:
            data = response.json()
            print("✅ Comprehensive search successful")
            print(f"✅ Total matches: {data['search_results']['total_matches']}")
            print(f"✅ Price range: ₹{data['search_results']['price_range']['min']} - ₹{data['search_results']['price_range']['max']}")
        else:
            print(f"❌ Comprehensive search failed: {response.status_code}")
            print(f"❌ Response: {response.text}")
    except Exception as e:
        print(f"❌ Comprehensive search error: {e}")
    
    # Test 4: Get Locations
    print("\n4. Testing Get Locations:")
    try:
        response = requests.get(f"{BASE_URL}/api/locations")
        if response.status_code == 200:
            data = response.json()
            print("✅ Locations retrieved successfully")
            print(f"✅ Available locations: {len(data['locations'])}")
            print(f"✅ Sample locations: {', '.join(data['locations'][:3])}")
        else:
            print(f"❌ Locations failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Locations error: {e}")
    
    # Test 5: Get Amenities
    print("\n5. Testing Get Amenities:")
    try:
        response = requests.get(f"{BASE_URL}/api/amenities")
        if response.status_code == 200:
            data = response.json()
            print("✅ Amenities retrieved successfully")
            print(f"✅ Available amenities: {len(data['amenities'])}")
            print(f"✅ Sample amenities: {', '.join(data['amenities'][:5])}")
        else:
            print(f"❌ Amenities failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Amenities error: {e}")
    
    # Test 6: Error handling (missing required parameters)
    print("\n6. Testing Error Handling (missing required parameters):")
    try:
        params = {
            'location': 'Mumbai'
            # Missing required parameters
        }
        response = requests.get(f"{BASE_URL}/api/hotels/search", params=params)
        if response.status_code == 400:
            print("✅ Error handling working correctly")
            print(f"✅ Error message: {response.json().get('error', 'No error message')}")
        else:
            print(f"❌ Expected 400 error, got: {response.status_code}")
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Retell API Test Suite Completed!")

if __name__ == "__main__":
    try:
        test_retell_endpoints()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API. Make sure the Railway deployment is running.")
    except Exception as e:
        print(f"❌ Error: {e}") 