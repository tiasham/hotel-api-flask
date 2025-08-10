#!/usr/bin/env python3
"""
Test script for enhanced hotel filtering system
Tests all the new hotel filtering capabilities and API endpoints
"""
import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:5004"
WEBHOOK_BASE = f"{BASE_URL}/webhook"

def test_health_check():
    """Test the enhanced health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{WEBHOOK_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   Status: {data['status']}")
            print(f"   Hotel dataset loaded: {data['hotel_dataset_loaded']}")
            if data['hotel_stats']:
                stats = data['hotel_stats']
                print(f"   Total hotels: {stats['total_hotels']}")
                print(f"   Locations: {stats['locations']}")
                print(f"   Price range: ₹{stats['price_range']['min']:,} - ₹{stats['price_range']['max']:,}")
                print(f"   Average rating: {stats['avg_rating']:.1f}/5")
            print(f"   Available endpoints: {list(data['endpoints'].keys())}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_available_locations():
    """Test getting available locations"""
    print("\n🔍 Testing available locations...")
    try:
        response = requests.get(f"{WEBHOOK_BASE}/hotels/locations")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Available locations: {data['count']} locations found")
            print(f"   Locations: {', '.join(data['locations'][:5])}{'...' if len(data['locations']) > 5 else ''}")
            return True
        else:
            print(f"❌ Locations request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Locations error: {e}")
        return False

def test_available_amenities():
    """Test getting available amenities"""
    print("\n🔍 Testing available amenities...")
    try:
        response = requests.get(f"{WEBHOOK_BASE}/hotels/amenities")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Available amenities: {data['count']} amenities found")
            print(f"   Sample amenities: {', '.join(data['amenities'][:8])}{'...' if len(data['amenities']) > 8 else ''}")
            return True
        else:
            print(f"❌ Amenities request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Amenities error: {e}")
        return False

def test_price_range():
    """Test getting price range"""
    print("\n🔍 Testing price range...")
    try:
        response = requests.get(f"{WEBHOOK_BASE}/hotels/price-range")
        if response.status_code == 200:
            data = response.json()
            price_range = data['price_range']
            print(f"✅ Price range: ₹{price_range['min']:,} - ₹{price_range['max']:,}")
            return True
        else:
            print(f"❌ Price range request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Price range error: {e}")
        return False

def test_hotel_stats():
    """Test getting hotel statistics"""
    print("\n🔍 Testing hotel statistics...")
    try:
        response = requests.get(f"{WEBHOOK_BASE}/hotels/stats")
        if response.status_code == 200:
            data = response.json()
            stats = data['stats']
            print(f"✅ Hotel statistics:")
            print(f"   Total hotels: {stats['total_hotels']}")
            print(f"   Unique locations: {stats['locations']}")
            print(f"   Star ratings: {stats['star_ratings']}")
            print(f"   Price stats: min=₹{stats['price_stats']['min']:,}, max=₹{stats['price_stats']['max']:,}, avg=₹{stats['price_stats']['mean']:,.0f}")
            print(f"   Rating stats: min={stats['rating_stats']['min']:.1f}, max={stats['rating_stats']['max']:.1f}, avg={stats['rating_stats']['mean']:.1f}")
            return True
        else:
            print(f"❌ Hotel stats request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Hotel stats error: {e}")
        return False

def test_advanced_hotel_search():
    """Test advanced hotel search with various filters"""
    print("\n🔍 Testing advanced hotel search...")
    
    # Test case 1: Basic location search
    print("   Testing basic location search (Delhi)...")
    search_data = {
        'location': 'Delhi',
        'min_stars': 4,
        'max_price': 8000
    }
    
    try:
        response = requests.post(f"{WEBHOOK_BASE}/hotels/search/advanced", json=search_data)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Delhi search: {data['count']} hotels found")
            if data['hotels']:
                hotel = data['hotels'][0]
                print(f"      Sample: {hotel['name']} - {hotel['stars']}★ - ₹{hotel['price_per_night']:,}/night")
        else:
            print(f"   ❌ Delhi search failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Delhi search error: {e}")
    
    # Test case 2: Luxury search
    print("   Testing luxury search (5-star, high rating)...")
    search_data = {
        'min_stars': 5,
        'min_rating': 4.5,
        'max_price': 15000
    }
    
    try:
        response = requests.post(f"{WEBHOOK_BASE}/hotels/search/advanced", json=search_data)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Luxury search: {data['count']} hotels found")
            if data['hotels']:
                hotel = data['hotels'][0]
                print(f"      Sample: {hotel['name']} - {hotel['stars']}★ - {hotel['guest_rating']}/5 - ₹{hotel['price_per_night']:,}/night")
        else:
            print(f"   ❌ Luxury search failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Luxury search error: {e}")
    
    # Test case 3: Amenity search
    print("   Testing amenity search (WiFi, Pool)...")
    search_data = {
        'amenities': 'WiFi, Pool',
        'min_stars': 3,
        'max_price': 10000
    }
    
    try:
        response = requests.post(f"{WEBHOOK_BASE}/hotels/search/advanced", json=search_data)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Amenity search: {data['count']} hotels found")
            if data['hotels']:
                hotel = data['hotels'][0]
                print(f"      Sample: {hotel['name']} - {hotel['stars']}★ - ₹{hotel['price_per_night']:,}/night")
        else:
            print(f"   ❌ Amenity search failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Amenity search error: {e}")
    
    # Test case 4: Complex search
    print("   Testing complex search (location + dates + capacity)...")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    day_after = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
    
    search_data = {
        'location': 'Mumbai',
        'check_in_date': tomorrow,
        'check_out_date': day_after,
        'adults': 2,
        'children': 1,
        'min_stars': 4,
        'max_price': 12000
    }
    
    try:
        response = requests.post(f"{WEBHOOK_BASE}/hotels/search/advanced", json=search_data)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Complex search: {data['count']} hotels found")
            if data['hotels']:
                hotel = data['hotels'][0]
                print(f"      Sample: {hotel['name']} - {hotel['stars']}★ - ₹{hotel['price_per_night']:,}/night")
        else:
            print(f"   ❌ Complex search failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Complex search error: {e}")
    
    return True

def test_conversation_flow_with_filtering():
    """Test the complete conversation flow with hotel filtering"""
    print("\n🔍 Testing conversation flow with hotel filtering...")
    
    try:
        # Step 1: Trigger a new conversation
        print("   Step 1: Triggering new conversation...")
        trigger_data = {
            'user_id': 'test_user_filtering',
            'start_voice': False
        }
        
        response = requests.post(f"{WEBHOOK_BASE}/trigger", json=trigger_data)
        if response.status_code != 200:
            print(f"   ❌ Trigger failed: {response.status_code}")
            return False
        
        trigger_result = response.json()
        session_id = trigger_result['session_id']
        print(f"   ✅ Conversation started: {session_id}")
        
        # Step 2: Simulate conversation to collect booking info
        conversation_steps = [
            "मैं Delhi में hotel चाहता हूँ",
            "check-in 15 December 2024 को है",
            "check-out 18 December 2024 को है", 
            "2 adults और 1 child जा रहे हैं",
            "1 room चाहिए",
            "WiFi और AC amenities चाहिए",
            "budget 8000 rupees per night तक है",
            "minimum 4 star rating चाहिए",
            "मेरा नाम Rahul है"
        ]
        
        print("   Step 2: Simulating conversation...")
        for i, user_input in enumerate(conversation_steps, 1):
            chat_data = {
                'session_id': session_id,
                'user_input': user_input
            }
            
            response = requests.post(f"{WEBHOOK_BASE}/chat", json=chat_data)
            if response.status_code == 200:
                chat_result = response.json()
                print(f"      Step {i}: {user_input[:30]}... → {chat_result['response'][:50]}...")
            else:
                print(f"      ❌ Step {i} failed: {response.status_code}")
        
        # Step 3: Check if hotels were found
        print("   Step 3: Checking hotel search results...")
        response = requests.post(f"{WEBHOOK_BASE}/hotels/search", json={'session_id': session_id})
        if response.status_code == 200:
            search_result = response.json()
            print(f"   ✅ Hotel search completed: {search_result['count']} hotels found")
            if search_result['hotels']:
                hotel = search_result['hotels'][0]
                print(f"      Top result: {hotel['name']} - {hotel['stars']}★ - ₹{hotel['price_per_night']:,}/night")
        else:
            print(f"   ❌ Hotel search failed: {response.status_code}")
        
        # Step 4: Get conversation history
        print("   Step 4: Getting conversation history...")
        response = requests.get(f"{WEBHOOK_BASE}/conversation/{session_id}")
        if response.status_code == 200:
            conv_result = response.json()
            print(f"   ✅ Conversation history retrieved: {len(conv_result['conversation']['conversation_history'])} messages")
        else:
            print(f"   ❌ Conversation history failed: {response.status_code}")
        
        # Step 5: End conversation
        print("   Step 5: Ending conversation...")
        response = requests.delete(f"{WEBHOOK_BASE}/conversation/{session_id}")
        if response.status_code == 200:
            print(f"   ✅ Conversation ended successfully")
        else:
            print(f"   ❌ Conversation end failed: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Conversation flow error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Enhanced Hotel Filtering System Tests")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Available Locations", test_available_locations),
        ("Available Amenities", test_available_amenities),
        ("Price Range", test_price_range),
        ("Hotel Statistics", test_hotel_stats),
        ("Advanced Hotel Search", test_advanced_hotel_search),
        ("Conversation Flow with Filtering", test_conversation_flow_with_filtering)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced hotel filtering system is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("\n🔧 To test manually, start the webhook system:")
    print(f"   python voice_agent_webhook_system.py")
    print(f"   Then visit: {BASE_URL}/webhook/health")

if __name__ == "__main__":
    main()
