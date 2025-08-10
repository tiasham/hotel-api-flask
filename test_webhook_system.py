#!/usr/bin/env python3
"""
Test script for Voice Agent Webhook System
Demonstrates complete flow: trigger → collect info → search hotels → get filtered responses
"""
import requests
import json
import time
from datetime import datetime

# Configuration
WEBHOOK_API_URL = "http://localhost:5004"

def test_webhook_system():
    """Test the complete webhook system"""
    print("🏨 Testing Voice Agent Webhook System")
    print("=" * 60)
    
    # Test 1: Check health
    print("\n1. 💚 Health Check...")
    try:
        response = requests.get(f"{WEBHOOK_API_URL}/webhook/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check passed!")
            print(f"   Status: {data['status']}")
            print(f"   Active Conversations: {data['active_conversations']}")
            print(f"   Hotel Dataset Loaded: {data['hotel_dataset_loaded']}")
            print(f"   Hotel Count: {data['hotel_count']}")
            print(f"   LiveKit Configured: {data['livekit_configured']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Cannot connect to webhook system: {e}")
        print("   Please start the webhook system first:")
        print("   python voice_agent_webhook_system.py")
        return None
    
    # Test 2: Trigger voice agent (text only)
    print("\n2. 🚀 Triggering voice agent (text mode)...")
    try:
        response = requests.post(f"{WEBHOOK_API_URL}/webhook/trigger", json={
            "user_id": "test_user_webhook",
            "start_voice": False
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ Voice agent triggered successfully!")
                print(f"   Session ID: {data['session_id']}")
                print(f"   User ID: {data['user_id']}")
                print(f"   Ticket: {data['ticket_number']}")
                print(f"   Message: {data['message']}")
                print(f"   Voice Session Active: {data['voice_session_active']}")
                
                session_id = data['session_id']
                return session_id
            else:
                print(f"   ❌ Failed to trigger voice agent: {data.get('error')}")
                return None
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error triggering voice agent: {e}")
        return None

def test_conversation_flow(session_id):
    """Test the complete conversation flow"""
    print(f"\n3. 💬 Testing conversation flow for session: {session_id}")
    print("-" * 60)
    
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
            response = requests.post(f"{WEBHOOK_API_URL}/webhook/chat", json={
                "session_id": session_id,
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

def test_hotel_search(session_id):
    """Test hotel search functionality"""
    print(f"\n4. 🔍 Testing hotel search for session: {session_id}")
    print("-" * 60)
    
    try:
        response = requests.post(f"{WEBHOOK_API_URL}/webhook/hotels/search", json={
            "session_id": session_id
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                hotels = data['hotels']
                count = data['count']
                
                print(f"   ✅ Hotel search completed successfully!")
                print(f"   Found {count} hotels matching criteria")
                
                if hotels:
                    print(f"   Top hotels:")
                    for i, hotel in enumerate(hotels[:3], 1):
                        print(f"     {i}. {hotel['name']} - {hotel['stars']}★ - ₹{hotel['price_per_night']}/night")
                        print(f"        Location: {hotel['location']}, Rating: {hotel['guest_rating']}/5")
                        print(f"        Amenities: {hotel['amenities']}")
                else:
                    print(f"   ⚠️  No hotels found matching criteria")
                    
            else:
                print(f"   ❌ Hotel search failed: {data.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error in hotel search: {e}")

def test_conversation_history(session_id):
    """Test getting conversation history"""
    print(f"\n5. 📜 Testing conversation history for session: {session_id}")
    print("-" * 60)
    
    try:
        response = requests.get(f"{WEBHOOK_API_URL}/webhook/conversation/{session_id}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                conversation = data['conversation']
                print(f"   ✅ Conversation history retrieved!")
                print(f"   Session ID: {conversation['session_id']}")
                print(f"   Ticket: {conversation['ticket_number']}")
                print(f"   Started: {conversation['conversation_started']}")
                print(f"   User Name: {conversation['user_name']}")
                print(f"   Messages: {len(conversation['conversation_history'])}")
                print(f"   Voice Session Active: {conversation['voice_session_active']}")
                
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

def test_voice_session_trigger(session_id):
    """Test triggering voice session"""
    print(f"\n6. 🎤 Testing voice session trigger for session: {session_id}")
    print("-" * 60)
    
    try:
        response = requests.post(f"{WEBHOOK_API_URL}/webhook/start-voice", json={
            "session_id": session_id
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ Voice session started successfully!")
                print(f"   Room Name: {data['room_name']}")
                print(f"   Message: {data['message']}")
            else:
                print(f"   ⚠️  Voice session not started: {data.get('error')}")
                print(f"   (This is expected if LiveKit is not configured)")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error starting voice session: {e}")

def test_end_conversation(session_id):
    """Test ending the conversation"""
    print(f"\n7. 🏁 Testing end conversation for session: {session_id}")
    print("-" * 60)
    
    try:
        response = requests.delete(f"{WEBHOOK_API_URL}/webhook/conversation/{session_id}")
        
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

def test_trigger_with_voice():
    """Test triggering voice agent with voice session"""
    print(f"\n8. 🎤 Testing trigger with voice session...")
    print("-" * 60)
    
    try:
        response = requests.post(f"{WEBHOOK_API_URL}/webhook/trigger", json={
            "user_id": "test_user_voice",
            "start_voice": True
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ Voice agent triggered with voice session!")
                print(f"   Session ID: {data['session_id']}")
                print(f"   Voice Session Active: {data['voice_session_active']}")
                
                if data.get('voice_session_active'):
                    print(f"   Room Name: {data['room_name']}")
                    print(f"   Voice Message: {data['voice_message']}")
                else:
                    print(f"   Voice Error: {data.get('voice_error', 'Unknown error')}")
                
                # Clean up
                session_id = data['session_id']
                requests.delete(f"{WEBHOOK_API_URL}/webhook/conversation/{session_id}")
                
            else:
                print(f"   ❌ Failed to trigger voice agent: {data.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error triggering voice agent: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Voice Agent Webhook System Tests")
    print("=" * 80)
    
    # Run tests
    session_id = test_webhook_system()
    
    if session_id:
        test_conversation_flow(session_id)
        test_hotel_search(session_id)
        test_conversation_history(session_id)
        test_voice_session_trigger(session_id)
        test_end_conversation(session_id)
    
    test_trigger_with_voice()
    
    print("\n" + "=" * 80)
    print("✅ All webhook system tests completed!")

if __name__ == "__main__":
    main()
