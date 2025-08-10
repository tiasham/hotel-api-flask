# Voice Agent Webhook System Guide

A complete system that allows you to trigger a voice agent via API/webhook, collect booking information through Hindi/Hinglish conversations, and get filtered hotel responses from the hotel dataset.

## 🎯 System Overview

```
API/Webhook Trigger → Voice Agent → Collect Info → Search Hotels → Filtered Responses
```

### Key Features:
- ✅ **API/Webhook trigger** for voice agent
- ✅ **Hindi/Hinglish conversation flow** with "राज" personality
- ✅ **Step-by-step information collection**
- ✅ **Direct hotel dataset integration** (Hotel_Dataset.csv)
- ✅ **Filtered hotel responses** based on user criteria
- ✅ **LiveKit voice session support**
- ✅ **Complete conversation state management**

## 🚀 Quick Start

### 1. Start the Services
```bash
# Start hotel server (for enhanced features)
python run_enhanced_server.py

# Start webhook system
python voice_agent_webhook_system.py
```

### 2. Test the System
```bash
# Run comprehensive tests
python test_webhook_system.py
```

## 📋 API Endpoints

### Base URL
```
http://localhost:5004
```

### Endpoints
- `POST /webhook/trigger` - Trigger voice agent
- `POST /webhook/chat` - Send chat message
- `POST /webhook/start-voice` - Start voice session
- `POST /webhook/hotels/search` - Search hotels from dataset
- `GET /webhook/conversation/{session_id}` - Get conversation history
- `DELETE /webhook/conversation/{session_id}` - End conversation
- `GET /webhook/health` - Health check

## 🔥 Complete Usage Examples

### 1. Trigger Voice Agent

```bash
# Trigger with text conversation only
curl -X POST http://localhost:5004/webhook/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "start_voice": false
  }'
```

**Response:**
```json
{
  "success": true,
  "session_id": "session_a1b2c3d4",
  "user_id": "user_123",
  "ticket_number": "SR3017861",
  "message": "Hey, welcome to Cleartrip Hotel Support! मैं राज बोल रहा हूँ — super excited हूँ आपकी hotel booking में help करने के लिए! बताइए, कहाँ जाना है आपको? (Ticket: SR3017861)",
  "conversation_started": "2024-12-19T10:30:00.000Z",
  "voice_session_active": false
}
```

### 2. Trigger with Voice Session

```bash
# Trigger with voice session (requires LiveKit configuration)
curl -X POST http://localhost:5004/webhook/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "start_voice": true
  }'
```

**Response:**
```json
{
  "success": true,
  "session_id": "session_a1b2c3d4",
  "user_id": "user_123",
  "ticket_number": "SR3017861",
  "message": "Hey, welcome to Cleartrip Hotel Support! मैं राज बोल रहा हूँ...",
  "conversation_started": "2024-12-19T10:30:00.000Z",
  "voice_session_active": true,
  "room_name": "hotel_booking_session_a1b2c3d4",
  "voice_message": "Voice session started successfully"
}
```

### 3. Send Location Information

```bash
curl -X POST http://localhost:5004/webhook/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_a1b2c3d4",
    "message": "मुझे Mumbai में hotel चाहिए"
  }'
```

**Response:**
```json
{
  "success": true,
  "response": "Great! Mumbai में होटल ढूंढेंगे। Check-in और check-out की dates क्या होंगी?",
  "timestamp": "2024-12-19T10:30:05.000Z"
}
```

### 4. Send Dates

```bash
curl -X POST http://localhost:5004/webhook/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_a1b2c3d4",
    "message": "Check-in 20 December और check-out 23 December"
  }'
```

**Response:**
```json
{
  "success": true,
  "response": "Adult और बच्चे — कितने लोग जा रहे हैं?",
  "timestamp": "2024-12-19T10:30:10.000Z"
}
```

### 5. Complete Conversation Flow

```bash
#!/bin/bash

# 1. Trigger conversation
SESSION_RESPONSE=$(curl -s -X POST http://localhost:5004/webhook/trigger \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "start_voice": false}')

SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.session_id')
echo "Session ID: $SESSION_ID"

# 2. Send location
curl -s -X POST http://localhost:5004/webhook/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"मुझे Mumbai में hotel चाहिए\"}"

# 3. Send dates
curl -s -X POST http://localhost:5004/webhook/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"Check-in 20 December और check-out 23 December\"}"

# 4. Send guests
curl -s -X POST http://localhost:5004/webhook/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"2 adults और 1 child\"}"

# 5. Send rooms
curl -s -X POST http://localhost:5004/webhook/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"1 room चाहिए\"}"

# 6. Send amenities
curl -s -X POST http://localhost:5004/webhook/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"WiFi और pool चाहिए\"}"

# 7. Send budget
curl -s -X POST http://localhost:5004/webhook/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"Budget 10,000 से 20,000 rupees per night\"}"

# 8. Send star rating
curl -s -X POST http://localhost:5004/webhook/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"5 star hotels चाहिए\"}"

# 9. Send guest rating
curl -s -X POST http://localhost:5004/webhook/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"4 plus rating चाहिए\"}"

# 10. Send name
curl -s -X POST http://localhost:5004/webhook/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"मेरा नाम Rahul है\"}"

echo "Conversation completed!"
```

### 6. Search Hotels from Dataset

```bash
curl -X POST http://localhost:5004/webhook/hotels/search \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_a1b2c3d4"
  }'
```

**Response:**
```json
{
  "success": true,
  "hotels": [
    {
      "hotel_id": "HOTEL001",
      "name": "Taj Palace Mumbai",
      "location": "Mumbai",
      "stars": 5,
      "guest_rating": 4.8,
      "price_per_night": 15000,
      "amenities": "Gym,Pool,Restaurant,Spa,WiFi,Parking,Concierge",
      "max_adults": 4,
      "max_children": 2
    },
    {
      "hotel_id": "HOTEL004",
      "name": "Leela Palace Mumbai",
      "location": "Mumbai",
      "stars": 5,
      "guest_rating": 4.8,
      "price_per_night": 16000,
      "amenities": "Gym,Restaurant,Spa,WiFi,Parking,Concierge,Pool",
      "max_adults": 4,
      "max_children": 2
    }
  ],
  "count": 2
}
```

### 7. Get Conversation History

```bash
curl -X GET http://localhost:5004/webhook/conversation/session_a1b2c3d4
```

**Response:**
```json
{
  "success": true,
  "conversation": {
    "session_id": "session_a1b2c3d4",
    "user_id": "user_123",
    "ticket_number": "SR3017861",
    "conversation_started": "2024-12-19T10:30:00.000Z",
    "current_step": "hotel_search_complete",
    "user_name": "Rahul",
    "booking_info": {
      "location": "Mumbai",
      "check_in_date": "2024-12-20",
      "check_out_date": "2024-12-23",
      "adults": 2,
      "children": 1,
      "rooms": 1,
      "amenities": "WiFi,Pool",
      "min_price": 10000,
      "max_price": 20000,
      "min_stars": 5,
      "min_rating": 4
    },
    "conversation_history": [
      {
        "role": "user",
        "content": "मुझे Mumbai में hotel चाहिए",
        "timestamp": "2024-12-19T10:30:05.000Z"
      },
      {
        "role": "assistant",
        "content": "Great! Mumbai में होटल ढूंढेंगे। Check-in और check-out की dates क्या होंगी?",
        "timestamp": "2024-12-19T10:30:05.000Z"
      }
    ],
    "voice_session_active": false,
    "livekit_room_name": null
  }
}
```

### 8. Start Voice Session

```bash
curl -X POST http://localhost:5004/webhook/start-voice \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_a1b2c3d4"
  }'
```

**Response:**
```json
{
  "success": true,
  "room_name": "hotel_booking_session_a1b2c3d4",
  "message": "Voice session started successfully"
}
```

### 9. End Conversation

```bash
curl -X DELETE http://localhost:5004/webhook/conversation/session_a1b2c3d4
```

**Response:**
```json
{
  "success": true,
  "message": "Conversation ended"
}
```

### 10. Health Check

```bash
curl -X GET http://localhost:5004/webhook/health
```

**Response:**
```json
{
  "status": "healthy",
  "active_conversations": 1,
  "hotel_dataset_loaded": true,
  "hotel_count": 15,
  "livekit_configured": true
}
```

## 🔧 Integration Examples

### Python Integration

```python
import requests
import json

class VoiceAgentWebhookClient:
    def __init__(self, base_url="http://localhost:5004"):
        self.base_url = base_url
    
    def trigger_agent(self, user_id, start_voice=False):
        response = requests.post(f"{self.base_url}/webhook/trigger", json={
            "user_id": user_id,
            "start_voice": start_voice
        })
        return response.json()
    
    def send_message(self, session_id, message):
        response = requests.post(f"{self.base_url}/webhook/chat", json={
            "session_id": session_id,
            "message": message
        })
        return response.json()
    
    def search_hotels(self, session_id):
        response = requests.post(f"{self.base_url}/webhook/hotels/search", json={
            "session_id": session_id
        })
        return response.json()
    
    def get_history(self, session_id):
        response = requests.get(f"{self.base_url}/webhook/conversation/{session_id}")
        return response.json()
    
    def start_voice(self, session_id):
        response = requests.post(f"{self.base_url}/webhook/start-voice", json={
            "session_id": session_id
        })
        return response.json()
    
    def end_conversation(self, session_id):
        response = requests.delete(f"{self.base_url}/webhook/conversation/{session_id}")
        return response.json()

# Usage
client = VoiceAgentWebhookClient()

# Trigger agent
result = client.trigger_agent("user_123")
session_id = result['session_id']
print(f"Session started: {result['message']}")

# Send location
response = client.send_message(session_id, "मुझे Mumbai में hotel चाहिए")
print(f"Assistant: {response['response']}")

# Search hotels
hotels = client.search_hotels(session_id)
print(f"Found {hotels['count']} hotels")

# End conversation
client.end_conversation(session_id)
```

### JavaScript Integration

```javascript
class VoiceAgentWebhookClient {
    constructor(baseUrl = 'http://localhost:5004') {
        this.baseUrl = baseUrl;
    }
    
    async triggerAgent(userId, startVoice = false) {
        const response = await fetch(`${this.baseUrl}/webhook/trigger`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, start_voice: startVoice })
        });
        return response.json();
    }
    
    async sendMessage(sessionId, message) {
        const response = await fetch(`${this.baseUrl}/webhook/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, message })
        });
        return response.json();
    }
    
    async searchHotels(sessionId) {
        const response = await fetch(`${this.baseUrl}/webhook/hotels/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId })
        });
        return response.json();
    }
    
    async getHistory(sessionId) {
        const response = await fetch(`${this.baseUrl}/webhook/conversation/${sessionId}`);
        return response.json();
    }
    
    async startVoice(sessionId) {
        const response = await fetch(`${this.baseUrl}/webhook/start-voice`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId })
        });
        return response.json();
    }
    
    async endConversation(sessionId) {
        const response = await fetch(`${this.baseUrl}/webhook/conversation/${sessionId}`, {
            method: 'DELETE'
        });
        return response.json();
    }
}

// Usage
const client = new VoiceAgentWebhookClient();

// Trigger agent
client.triggerAgent('user_123').then(result => {
    console.log('Session started:', result.message);
    
    // Send location
    return client.sendMessage(result.session_id, 'मुझे Mumbai में hotel चाहिए');
}).then(response => {
    console.log('Assistant:', response.response);
});
```

## 🎯 Conversation Flow

The system follows this step-by-step conversation flow:

1. **Greeting**: "Hey, welcome to Cleartrip Hotel Support! मैं राज बोल रहा हूँ..."
2. **Location**: "सबसे पहले बताइए — आपको किस शहर या एरिया में होटल चाहिए?"
3. **Dates**: "Check-in और check-out की dates क्या होंगी?"
4. **Guests**: "Adult और बच्चे — कितने लोग जा रहे हैं?"
5. **Rooms**: "आपको कितने rooms की ज़रूरत होगी?"
6. **Amenities**: "कोई specific amenities चाहिए?"
7. **Budget**: "आपका budget क्या है?"
8. **Star Rating**: "कोई specific star rating चाहिए?"
9. **Guest Rating**: "Guest reviews matter करते हैं क्या?"
10. **Name**: "Perfect! Booking शुरू करने से पहले — अपना नाम बता दीजिए।"

## 🔍 Hotel Dataset Integration

The system directly searches the `Hotel_Dataset.csv` file and applies filters based on:

- **Location** (Mumbai, Delhi, Bangalore, etc.)
- **Capacity** (adults, children)
- **Amenities** (WiFi, Pool, AC, etc.)
- **Price Range** (min/max price per night)
- **Star Rating** (1-5 stars)
- **Guest Rating** (0.0-5.0)

## 🎤 Voice Session Support

When `start_voice: true` is set, the system:

1. Creates a LiveKit room
2. Starts the LiveKit voice agent
3. Connects to the room for voice communication
4. Maintains conversation state across voice and text

## 🚀 Ready to Use!

The Voice Agent Webhook System provides a complete solution for:

✅ **API/Webhook triggering** of voice agents  
✅ **Hindi/Hinglish conversation flow**  
✅ **Information collection** from users  
✅ **Direct hotel dataset search**  
✅ **Filtered responses** based on criteria  
✅ **Voice session support**  
✅ **Complete state management**  

Perfect for integrating into your hotel booking platform! 🏨
