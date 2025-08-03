#!/usr/bin/env python3
"""
Test script for MCP Hotel Server
"""

import requests
import json

BASE_URL = "http://localhost:8080"

def test_mcp_server():
    """Test the MCP server endpoints"""
    
    print("🧪 Testing MCP Hotel Server")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing Health Check:")
    try:
        response = requests.get(f"{BASE_URL}/mcp/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ MCP server is healthy")
            print(f"✅ Status: {data.get('status')}")
            print(f"✅ Message: {data.get('message')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Get locations
    print("\n2. Testing Get Locations:")
    try:
        response = requests.get(f"{BASE_URL}/mcp/locations")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Locations retrieved successfully")
                print(f"✅ Found {data.get('count')} locations")
                print(f"✅ Sample locations: {', '.join(data.get('locations', [])[:3])}")
            else:
                print(f"❌ Locations failed: {data.get('error')}")
        else:
            print(f"❌ Locations endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Locations error: {e}")
    
    # Test 3: Get amenities
    print("\n3. Testing Get Amenities:")
    try:
        response = requests.get(f"{BASE_URL}/mcp/amenities")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Amenities retrieved successfully")
                print(f"✅ Found {data.get('count')} amenities")
                print(f"✅ Sample amenities: {', '.join(data.get('amenities', [])[:5])}")
            else:
                print(f"❌ Amenities failed: {data.get('error')}")
        else:
            print(f"❌ Amenities endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Amenities error: {e}")
    
    # Test 4: Search hotels
    print("\n4. Testing Search Hotels:")
    try:
        search_data = {
            'location': 'Mumbai',
            'check_in_date': '2024-08-15',
            'check_out_date': '2024-08-20',
            'adults': 2,
            'children': 1,
            'amenities': 'Pool,Gym',
            'max_price': 5000,
            'min_stars': 4
        }
        
        response = requests.post(f"{BASE_URL}/mcp/search", json=search_data)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Hotel search successful")
                print(f"✅ Total matches: {data.get('total_matches')}")
                print(f"✅ Hotels returned: {len(data.get('hotels', []))}")
                print(f"✅ Message: {data.get('message')}")
                
                # Show first hotel details
                if data.get('hotels'):
                    hotel = data['hotels'][0]
                    print(f"✅ Sample hotel: {hotel.get('name')} - {hotel.get('stars')} stars - ₹{hotel.get('price_per_night')}")
            else:
                print(f"❌ Search failed: {data.get('error')}")
        else:
            print(f"❌ Search endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Search error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 MCP Server Test Summary:")
    print("✅ If all tests pass, your MCP server is ready for Retell!")
    print("\n📋 Next Steps:")
    print("1. Deploy this MCP server to Railway")
    print("2. Use the MCP configuration in Retell")
    print("3. Test the integration")

if __name__ == "__main__":
    test_mcp_server() 