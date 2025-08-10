#!/usr/bin/env python3
"""
Test script for Voice Agent Trigger API
Demonstrates the Hindi/Hinglish hotel booking conversation flow
"""
import requests
import json
import time
from datetime import datetime

# Configuration
TRIGGER_API_URL = "http://localhost:5003"

def test_trigger_api():
    """Test the voice agent trigger API"""
    print("🏨 Testing Voice Agent Trigger API")
    print("=" * 50)
    
    # Test 1: Trigger a new conversation
    print("\n1. 🚀 Triggering new conversation...")
    try:
        response = requests.post(f"{TRIGGER_API_URL}/trigger", json={
            "user_id": "test_user_001"
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Conversation triggered successfully!")
                print(f"   User ID: {data['user_id']}")
                print(f"   Ticket: {data['ticket_number']}")
                print(f"   Message: {data['message']}")
                
                user_id = data['user_id']
                return user_id
            else:
                print(f"❌ Failed to trigger conversation: {data.get('error')}")
                return None
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error triggering conversation: {e}")
        return None

def test_conversation_flow(user_id):
    """Test the complete conversation flow"""
    print(f"\n2. 💬 Testing conversation flow for user: {user_id}")
    print("-" * 50)
    
    # Sample conversation flow
    conversation_steps = [
        {
            "step": "Location",
            "message": "मुझे Mumbai में hotel चाहिए",
            "expected_keywords": ["Great", "Mumbai", "होटल ढूंढेंगे"]
        },
        {
            "step": "Dates", 
            "message": "Check-in 20 December और check-out 23 December",
            "expected_keywords": ["dates", "check-in", "check-out"]
        },
        {
            "step": "Guests",
            "message": "2 adults और 1 child",
            "expected_keywords": ["adults", "child", "लोग"]
        },
        {
            "step": "Rooms",
            "message": "1 room चाहिए",
            "expected_keywords": ["room", "कमरे"]
        },
        {
            "step": "Amenities",
            "message": "WiFi और pool चाहिए",
            "expected_keywords": ["amenities", "wifi", "pool"]
        },
        {
            "step": "Budget",
            "message": "Budget 10,000 से 20,000 rupees per night",
            "expected_keywords": ["budget", "price", "rupees"]
        },
        {
            "step": "Star Rating",
            "message": "5 star hotels चाहिए",
            "expected_keywords": ["star", "rating"]
        },
        {
            "step": "Guest Rating",
            "message": "4 plus rating चाहिए",
            "expected_keywords": ["guest", "rating", "reviews"]
        },
        {
            "step": "Name",
            "message": "मेरा नाम Rahul है",
            "expected_keywords": ["Perfect", "Rahul", "booking"]
        }
    ]
    
    for i, step in enumerate(conversation_steps, 1):
        print(f"\n{i}. {step['step']}:")
        print(f"   User: {step['message']}")
        
        try:
            response = requests.post(f"{TRIGGER_API_URL}/chat", json={
                "user_id": user_id,
                "message": step['message']
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    assistant_response = data['response']
                    print(f"   Assistant: {assistant_response}")
                    
                    # Check if response contains expected keywords
                    expected_keywords = step['expected_keywords']
                    found_keywords = [kw for kw in expected_keywords if kw.lower() in assistant_response.lower()]
                    
                    if found_keywords:
                        print(f"   ✅ Response contains expected keywords: {found_keywords}")
                    else:
                        print(f"   ⚠️  Response may not contain expected keywords: {expected_keywords}")
                    
                    # Add delay between messages
                    time.sleep(1)
                    
                else:
                    print(f"   ❌ Chat failed: {data.get('error')}")
                    break
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                break
                
        except Exception as e:
            print(f"   ❌ Error in chat: {e}")
            break

def test_hotel_search_completion(user_id):
    """Test hotel search after completing the flow"""
    print(f"\n3. 🔍 Testing hotel search completion...")
    print("-" * 50)
    
    # Send a message that should trigger hotel search
    completion_message = "हाँ, सब कुछ सही है"
    
    try:
        response = requests.post(f"{TRIGGER_API_URL}/chat", json={
            "user_id": user_id,
            "message": completion_message
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                assistant_response = data['response']
                print(f"   User: {completion_message}")
                print(f"   Assistant: {assistant_response}")
                
                # Check if response contains hotel information
                if any(keyword in assistant_response.lower() for keyword in ['hotel', 'option', 'star', 'price', 'rating']):
                    print("   ✅ Hotel search completed successfully!")
                else:
                    print("   ⚠️  Hotel search may not have completed")
                    
            else:
                print(f"   ❌ Chat failed: {data.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error in hotel search: {e}")

def test_conversation_history(user_id):
    """Test getting conversation history"""
    print(f"\n4. 📜 Testing conversation history...")
    print("-" * 50)
    
    try:
        response = requests.get(f"{TRIGGER_API_URL}/conversation/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                conversation = data['conversation']
                print(f"   ✅ Conversation history retrieved!")
                print(f"   Ticket: {conversation['ticket_number']}")
                print(f"   Started: {conversation['conversation_started']}")
                print(f"   User Name: {conversation['user_name']}")
                print(f"   Messages: {len(conversation['conversation_history'])}")
                
                # Show booking info
                booking_info = conversation['booking_info']
                print(f"   Booking Info:")
                for key, value in booking_info.items():
                    if value:
                        print(f"     {key}: {value}")
                        
            else:
                print(f"   ❌ Failed to get history: {data.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error getting history: {e}")

def test_end_conversation(user_id):
    """Test ending the conversation"""
    print(f"\n5. 🏁 Testing end conversation...")
    print("-" * 50)
    
    try:
        response = requests.delete(f"{TRIGGER_API_URL}/conversation/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ Conversation ended successfully!")
            else:
                print(f"   ❌ Failed to end conversation: {data.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error ending conversation: {e}")

def test_health_check():
    """Test health check endpoint"""
    print(f"\n6. 💚 Testing health check...")
    print("-" * 50)
    
    try:
        response = requests.get(f"{TRIGGER_API_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check passed!")
            print(f"   Status: {data['status']}")
            print(f"   Active Conversations: {data['active_conversations']}")
            print(f"   Hotel Server URL: {data['hotel_server_url']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error in health check: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Voice Agent Trigger API Tests")
    print("=" * 60)
    
    # Check if trigger API is running
    try:
        response = requests.get(f"{TRIGGER_API_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Trigger API is not running. Please start it first:")
            print("   python voice_agent_trigger.py")
            return
    except:
        print("❌ Cannot connect to Trigger API. Please start it first:")
        print("   python voice_agent_trigger.py")
        return
    
    # Run tests
    user_id = test_trigger_api()
    
    if user_id:
        test_conversation_flow(user_id)
        test_hotel_search_completion(user_id)
        test_conversation_history(user_id)
        test_end_conversation(user_id)
    
    test_health_check()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")

if __name__ == "__main__":
    main()
