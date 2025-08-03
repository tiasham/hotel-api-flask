#!/usr/bin/env python3
"""
Test MCP tool discovery endpoints
"""

import requests
import json
import time

BASE_URL = "https://hotel-api-flask-production.up.railway.app"

def test_mcp_discovery():
    """Test the MCP tool discovery endpoints"""
    
    print("🧪 Testing MCP Tool Discovery")
    print("=" * 50)
    
    # Wait for Railway to redeploy
    print("⏳ Waiting for Railway to redeploy...")
    time.sleep(60)
    
    # Test 1: MCP Tools Discovery
    print("\n1. Testing MCP Tools Discovery:")
    try:
        response = requests.get(f"{BASE_URL}/mcp/tools", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ MCP tools discovery working")
            print(f"✅ Found {len(data.get('tools', []))} tools:")
            
            for tool in data.get('tools', []):
                print(f"  • {tool.get('name')} - {tool.get('description')}")
                if tool.get('parameters'):
                    print(f"    Parameters: {len(tool['parameters'])} parameters")
                else:
                    print(f"    Parameters: None")
        else:
            print(f"❌ MCP tools discovery failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ MCP tools discovery error: {e}")
    
    # Test 2: MCP Execute - Get Locations
    print("\n2. Testing MCP Execute - Get Locations:")
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
    
    # Test 3: MCP Execute - Search Hotels
    print("\n3. Testing MCP Execute - Search Hotels:")
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
    print("🎯 MCP Discovery Test Summary:")
    print("✅ If all tests pass, Retell should be able to discover tools!")
    print("\n📋 For Retell Configuration:")
    print("1. Use this URL: https://hotel-api-flask-production.up.railway.app")
    print("2. The tools should now appear in the dropdown:")
    print("   • searchHotels")
    print("   • getLocations")
    print("   • getAmenities")
    print("\n🔧 If tools still don't load:")
    print("  1. Wait 2-3 more minutes for Railway to redeploy")
    print("  2. Refresh the Retell page")
    print("  3. Clear browser cache")

if __name__ == "__main__":
    test_mcp_discovery() 