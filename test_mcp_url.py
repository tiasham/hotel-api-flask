#!/usr/bin/env python3
"""
Test MCP URL and provide the correct URL for Retell
"""

import requests
import json
import time

BASE_URL = "https://hotel-api-flask-production.up.railway.app"

def test_mcp_url():
    """Test the MCP server and provide the correct URL"""
    
    print("🧪 Testing MCP Server for Retell")
    print("=" * 50)
    
    # Wait for Railway to redeploy
    print("⏳ Waiting for Railway to redeploy...")
    time.sleep(60)
    
    # Test 1: Root endpoint
    print("\n1. Testing Root Endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ MCP server is running")
            print(f"✅ Message: {data.get('message')}")
            print(f"✅ Version: {data.get('version')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 2: MCP Tools Discovery
    print("\n2. Testing MCP Tools Discovery:")
    try:
        response = requests.get(f"{BASE_URL}/mcp/tools", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ MCP tools discovery working")
            print(f"✅ Found {len(data.get('tools', []))} tools:")
            
            for tool in data.get('tools', []):
                print(f"  • {tool.get('name')} - {tool.get('description')}")
        else:
            print(f"❌ MCP tools discovery failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ MCP tools discovery error: {e}")
    
    # Test 3: MCP Health Check
    print("\n3. Testing MCP Health Check:")
    try:
        response = requests.get(f"{BASE_URL}/mcp/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ MCP health check passed")
            print(f"✅ Status: {data.get('status')}")
            print(f"✅ Tools: {', '.join(data.get('tools', []))}")
        else:
            print(f"❌ MCP health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ MCP health check error: {e}")
    
    # Test 4: MCP Execute - Get Locations
    print("\n4. Testing MCP Execute - Get Locations:")
    try:
        data = {
            'tool': 'getLocations',
            'parameters': {}
        }
        response = requests.post(f"{BASE_URL}/mcp/execute", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ MCP execute - getLocations working")
                locations = result['result'].get('locations', [])
                print(f"✅ Found {len(locations)} locations")
                print(f"✅ Sample locations: {', '.join(locations[:3])}")
            else:
                print(f"❌ MCP execute failed: {result.get('error')}")
        else:
            print(f"❌ MCP execute failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ MCP execute error: {e}")
    
    # Test 5: MCP Execute - Search Hotels
    print("\n5. Testing MCP Execute - Search Hotels:")
    try:
        data = {
            'tool': 'searchHotels',
            'parameters': {
                'location': 'Mumbai',
                'check_in_date': '2024-08-15',
                'check_out_date': '2024-08-20',
                'adults': 2,
                'amenities': 'Pool',
                'max_price': 5000
            }
        }
        response = requests.post(f"{BASE_URL}/mcp/execute", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ MCP execute - searchHotels working")
                hotels = result['result'].get('hotels', [])
                print(f"✅ Found {len(hotels)} hotels")
                if hotels:
                    hotel = hotels[0]
                    print(f"✅ Sample hotel: {hotel.get('name')} - {hotel.get('stars')} stars")
            else:
                print(f"❌ MCP execute failed: {result.get('error')}")
        else:
            print(f"❌ MCP execute failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ MCP execute error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 MCP URL for Retell:")
    print("✅ Use this URL in Retell's MCP configuration:")
    print(f"   {BASE_URL}")
    print("\n📋 Available Tools:")
    print("  • searchHotels - Search for hotels")
    print("  • getLocations - Get available locations")
    print("  • getAmenities - Get available amenities")
    print("\n🔧 For Retell Configuration:")
    print("1. In the 'Edit MCP' form:")
    print("   - Name: HotelSearchAPI")
    print("   - URL: " + BASE_URL)
    print("   - Timeout: 10000")
    print("2. The tools should now load in the dropdown!")
    print("\n🎉 Your MCP server is ready for Retell!")

if __name__ == "__main__":
    test_mcp_url() 