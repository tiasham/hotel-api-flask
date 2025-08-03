#!/usr/bin/env python3
"""
Check Railway deployment status after fixes
"""

import requests
import time
import json

BASE_URL = "https://hotel-api-flask-production.up.railway.app"

def check_deployment():
    """Check if the deployment is working correctly"""
    
    print("🚀 Checking Railway Deployment Status")
    print("=" * 50)
    
    # Wait a bit for Railway to redeploy
    print("⏳ Waiting for Railway to redeploy (30 seconds)...")
    time.sleep(30)
    
    # Test 1: Health check endpoint
    print("\n1. Testing Health Check:")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"✅ Status: {data.get('status')}")
            print(f"✅ Message: {data.get('message')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: OpenAPI specification
    print("\n2. Testing OpenAPI Specification:")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=10)
        if response.status_code == 200:
            print("✅ OpenAPI specification accessible")
            spec = response.json()
            print(f"✅ API Title: {spec['info']['title']}")
            print(f"✅ Version: {spec['info']['version']}")
            
            # Check for required endpoints
            paths = spec.get('paths', {})
            required_endpoints = ['/api/hotels/search', '/api/locations', '/api/amenities']
            
            for endpoint in required_endpoints:
                if endpoint in paths:
                    print(f"✅ Endpoint found: {endpoint}")
                else:
                    print(f"❌ Missing endpoint: {endpoint}")
        else:
            print(f"❌ OpenAPI spec failed: {response.status_code}")
    except Exception as e:
        print(f"❌ OpenAPI spec error: {e}")
    
    # Test 3: Test endpoint
    print("\n3. Testing Test Endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/test", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Test endpoint working")
            print(f"✅ Status: {data.get('status')}")
            print(f"✅ Message: {data.get('message')}")
        else:
            print(f"❌ Test endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Test endpoint error: {e}")
    
    # Test 4: Search endpoint (with required parameters)
    print("\n4. Testing Search Endpoint:")
    try:
        params = {
            'location': 'Mumbai',
            'check_in_date': '2024-08-15',
            'check_out_date': '2024-08-20',
            'adults': 2
        }
        response = requests.get(f"{BASE_URL}/api/hotels/search", params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Search endpoint working")
            print(f"✅ Total matches: {data['search_results']['total_matches']}")
            print(f"✅ Top 5 hotels returned: {len(data['search_results']['top_5_hotels'])}")
        else:
            print(f"❌ Search endpoint failed: {response.status_code}")
            print(f"❌ Response: {response.text}")
    except Exception as e:
        print(f"❌ Search endpoint error: {e}")
    
    # Test 5: Check for development server warning
    print("\n5. Checking Server Type:")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            # Check if response contains any development server indicators
            if "development server" in response.text.lower():
                print("⚠️  Still using development server")
            else:
                print("✅ Using production server (Gunicorn)")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Server type check error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Deployment Status Summary:")
    print("✅ If all tests pass, your Railway deployment is working correctly!")
    print("✅ The OpenAPI URL for Retell should now work:")
    print(f"   {BASE_URL}/openapi.json")
    print("\n🔧 If any tests fail, wait 2-3 more minutes and run this script again.")

if __name__ == "__main__":
    check_deployment() 