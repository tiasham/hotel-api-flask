#!/usr/bin/env python3
"""
Verify OpenAPI specification for Retell compatibility
"""

import requests
import json

BASE_URL = "https://hotel-api-flask-production.up.railway.app"

def verify_openapi():
    """Verify the OpenAPI specification"""
    
    print("🔍 Verifying OpenAPI Specification for Retell")
    print("=" * 50)
    
    # Test 1: Check if OpenAPI spec is accessible
    print("\n1. Testing OpenAPI endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=10)
        if response.status_code == 200:
            print("✅ OpenAPI specification is accessible")
            
            # Parse the JSON to check structure
            spec = response.json()
            
            # Check required fields
            if 'openapi' in spec and 'info' in spec and 'paths' in spec:
                print("✅ OpenAPI structure is valid")
                print(f"✅ Version: {spec['openapi']}")
                print(f"✅ Title: {spec['info']['title']}")
                
                # Check for required endpoints
                paths = spec.get('paths', {})
                required_endpoints = ['/api/hotels/search', '/api/locations', '/api/amenities']
                
                for endpoint in required_endpoints:
                    if endpoint in paths:
                        print(f"✅ Endpoint found: {endpoint}")
                    else:
                        print(f"❌ Missing endpoint: {endpoint}")
                
                # Check for operationId (important for Retell)
                search_path = paths.get('/api/hotels/search', {})
                if 'get' in search_path and 'operationId' in search_path['get']:
                    print(f"✅ Operation ID found: {search_path['get']['operationId']}")
                else:
                    print("❌ Missing operationId in search endpoint")
                
                # Print available tools for Retell
                print("\n📋 Available Tools for Retell:")
                for path, methods in paths.items():
                    for method, details in methods.items():
                        if 'operationId' in details:
                            print(f"  • {details['operationId']} - {details.get('summary', 'No summary')}")
                
            else:
                print("❌ OpenAPI structure is invalid")
                
        else:
            print(f"❌ OpenAPI endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error accessing OpenAPI: {e}")
    
    # Test 2: Check if test endpoint works
    print("\n2. Testing API connectivity:")
    try:
        response = requests.get(f"{BASE_URL}/test", timeout=10)
        if response.status_code == 200:
            print("✅ API is responding correctly")
            data = response.json()
            print(f"✅ Status: {data.get('status')}")
            print(f"✅ Message: {data.get('message')}")
        else:
            print(f"❌ Test endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing API: {e}")
    
    # Test 3: Validate JSON structure
    print("\n3. Validating JSON structure:")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=10)
        if response.status_code == 200:
            # Try to parse JSON
            spec = response.json()
            
            # Check for common Retell issues
            issues = []
            
            # Check for nested objects that might cause issues
            for path, methods in spec.get('paths', {}).items():
                for method, details in methods.items():
                    # Check for complex nested schemas
                    if 'responses' in details:
                        for status, response_info in details['responses'].items():
                            if 'content' in response_info:
                                for content_type, content_info in response_info['content'].items():
                                    if 'schema' in content_info:
                                        schema = content_info['schema']
                                        if isinstance(schema, dict) and len(schema) > 10:
                                            issues.append(f"Complex schema in {path} {method}")
            
            if issues:
                print("⚠️  Potential issues found:")
                for issue in issues:
                    print(f"  • {issue}")
            else:
                print("✅ JSON structure looks good for Retell")
                
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
    except Exception as e:
        print(f"❌ Error validating JSON: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps for Retell:")
    print("1. Wait 2-3 minutes for Railway to redeploy")
    print("2. Try adding the OpenAPI URL again in Retell:")
    print(f"   {BASE_URL}/openapi.json")
    print("3. If still loading, try refreshing the Retell page")
    print("4. Check Retell's browser console for any errors")

if __name__ == "__main__":
    verify_openapi() 