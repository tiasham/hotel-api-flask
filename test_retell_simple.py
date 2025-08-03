#!/usr/bin/env python3
"""
Simple test for Retell MCP compatibility
"""

import requests
import json
import time

BASE_URL = "https://hotel-api-flask-production.up.railway.app"

def test_retell_compatibility():
    """Test if the API is compatible with Retell MCP"""
    
    print("🧪 Testing Retell MCP Compatibility")
    print("=" * 50)
    
    # Wait for Railway to redeploy
    print("⏳ Waiting for Railway to redeploy...")
    time.sleep(60)
    
    # Test 1: Root endpoint
    print("\n1. Testing Root Endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            data = response.json()
            print(f"✅ Message: {data.get('message')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 2: OpenAPI specification
    print("\n2. Testing OpenAPI Specification:")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=10)
        if response.status_code == 200:
            print("✅ OpenAPI specification accessible")
            
            # Parse and validate the spec
            spec = response.json()
            
            # Check basic structure
            if 'openapi' in spec and 'info' in spec and 'paths' in spec:
                print("✅ OpenAPI structure valid")
                print(f"✅ Version: {spec['openapi']}")
                print(f"✅ Title: {spec['info']['title']}")
                
                # Check for required endpoints
                paths = spec.get('paths', {})
                required_paths = ['/api/hotels/search', '/api/locations', '/api/amenities']
                
                for path in required_paths:
                    if path in paths:
                        print(f"✅ Path found: {path}")
                        # Check for operationId
                        if 'get' in paths[path] and 'operationId' in paths[path]['get']:
                            print(f"  ✅ Operation ID: {paths[path]['get']['operationId']}")
                        else:
                            print(f"  ❌ Missing operationId in {path}")
                    else:
                        print(f"❌ Missing path: {path}")
                
                # Check for components/schemas
                if 'components' in spec and 'schemas' in spec['components']:
                    print("✅ Schemas defined")
                    schemas = spec['components']['schemas']
                    if 'Hotel' in schemas:
                        print("✅ Hotel schema found")
                    else:
                        print("❌ Hotel schema missing")
                else:
                    print("❌ No schemas defined")
                
            else:
                print("❌ Invalid OpenAPI structure")
                
        else:
            print(f"❌ OpenAPI spec failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ OpenAPI spec error: {e}")
    
    # Test 3: Simple search endpoint test
    print("\n3. Testing Search Endpoint:")
    try:
        params = {
            'location': 'Mumbai',
            'check_in_date': '2024-08-15',
            'check_out_date': '2024-08-20',
            'adults': 2
        }
        response = requests.get(f"{BASE_URL}/api/hotels/search", params=params, timeout=10)
        if response.status_code == 200:
            print("✅ Search endpoint working")
            data = response.json()
            if 'search_results' in data:
                print(f"✅ Search results structure correct")
                print(f"✅ Total matches: {data['search_results'].get('total_matches', 0)}")
            else:
                print("❌ Unexpected response structure")
        else:
            print(f"❌ Search endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Search endpoint error: {e}")
    
    # Test 4: Locations endpoint
    print("\n4. Testing Locations Endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/api/locations", timeout=10)
        if response.status_code == 200:
            print("✅ Locations endpoint working")
            data = response.json()
            if 'locations' in data:
                print(f"✅ Found {len(data['locations'])} locations")
            else:
                print("❌ Unexpected response structure")
        else:
            print(f"❌ Locations endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Locations endpoint error: {e}")
    
    # Test 5: Amenities endpoint
    print("\n5. Testing Amenities Endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/api/amenities", timeout=10)
        if response.status_code == 200:
            print("✅ Amenities endpoint working")
            data = response.json()
            if 'amenities' in data:
                print(f"✅ Found {len(data['amenities'])} amenities")
            else:
                print("❌ Unexpected response structure")
        else:
            print(f"❌ Amenities endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Amenities endpoint error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Retell MCP Configuration:")
    print("✅ Use this URL in Retell:")
    print(f"   {BASE_URL}/openapi.json")
    print("\n📋 Available Tools for Retell:")
    print("  • searchHotels - Search for hotels")
    print("  • getLocations - Get available locations")
    print("  • getAmenities - Get available amenities")
    print("\n🔧 If tools still don't load:")
    print("  1. Clear browser cache")
    print("  2. Try incognito mode")
    print("  3. Check browser console for errors")
    print("  4. Verify the OpenAPI URL in browser")

if __name__ == "__main__":
    test_retell_compatibility() 