# Voice Agent Trigger API Usage Examples

This guide shows how to use the Voice Agent Trigger API to create Hindi/Hinglish hotel booking conversations.

## 🚀 Quick Start

### 1. Start the Services
```bash
# Start hotel server
python run_enhanced_server.py

# Start voice agent trigger API
python voice_agent_trigger.py
```

### 2. Test the API
```bash
# Run the test script
python test_voice_agent_trigger.py
```

## 📋 API Endpoints

### Base URL
```
http://localhost:5003
```

### Endpoints
- `POST /trigger` - Start a new conversation
- `POST /chat` - Send a message
- `GET /conversation/{user_id}` - Get conversation history
- `DELETE /conversation/{user_id}` - End conversation
- `GET /health` - Health check

## 🔥 Curl Examples

### 1. Trigger a New Conversation

```bash
curl -X POST http://localhost:5003/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123"
  }'
```

**Response:**
```json
{
  "success": true,
  "user_id": "user_123",
  "ticket_number": "SR3017861",
  "message": "Hey, welcome to Cleartrip Hotel Support! मैं राज बोल रहा हूँ — super excited हूँ आपकी hotel booking में help करने के लिए! बताइए, कहाँ जाना है आपको? (Ticket: SR3017861)",
  "conversation_started": "2024-12-19T10:30:00.000Z"
}
```

### 2. Send Location Information

```bash
curl -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
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

### 3. Send Dates

```bash
curl -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
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

### 4. Send Guest Information

```bash
curl -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "message": "2 adults और 1 child"
  }'
```

**Response:**
```json
{
  "success": true,
  "response": "आपको कितने rooms की ज़रूरत होगी?",
  "timestamp": "2024-12-19T10:30:15.000Z"
}
```

### 5. Send Room Information

```bash
curl -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "message": "1 room चाहिए"
  }'
```

**Response:**
```json
{
  "success": true,
  "response": "हर room में लगभग कितने guests रुकेंगे?",
  "timestamp": "2024-12-19T10:30:20.000Z"
}
```

### 6. Send Amenities

```bash
curl -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "message": "WiFi और pool चाहिए"
  }'
```

**Response:**
```json
{
  "success": true,
  "response": "आपका budget क्या है — minimum और maximum per night price बताइए।",
  "timestamp": "2024-12-19T10:30:25.000Z"
}
```

### 7. Send Budget

```bash
curl -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "message": "Budget 10,000 से 20,000 rupees per night"
  }'
```

**Response:**
```json
{
  "success": true,
  "response": "कोई specific star rating चाहिए? जैसे three star, four star, five star?",
  "timestamp": "2024-12-19T10:30:30.000Z"
}
```

### 8. Send Star Rating

```bash
curl -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "message": "5 star hotels चाहिए"
  }'
```

**Response:**
```json
{
  "success": true,
  "response": "Guest reviews matter करते हैं क्या? Minimum four-plus rating दिखाऊँ?",
  "timestamp": "2024-12-19T10:30:35.000Z"
}
```

### 9. Send Guest Rating Preference

```bash
curl -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "message": "4 plus rating चाहिए"
  }'
```

**Response:**
```json
{
  "success": true,
  "response": "Perfect! Booking शुरू करने से पहले — अपना नाम बता दीजिए।",
  "timestamp": "2024-12-19T10:30:40.000Z"
}
```

### 10. Send Name

```bash
curl -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "message": "मेरा नाम Rahul है"
  }'
```

**Response:**
```json
{
  "success": true,
  "response": "Perfect Rahul! मैंने आपके लिए 5 hotels ढूंढे हैं। एक शानदार option है Taj Palace Mumbai, ये एक 5-star property है, guest rating है 4.8/5, और price around 15000 rupees per night है। मैंने Taj Palace Mumbai को आपके cart में डाल दिया है — आप आराम से review कर सकते हैं। जब आप ready हों, बस बता दीजिए — मैं तुरंत booking confirm कर दूँगा।",
  "timestamp": "2024-12-19T10:30:45.000Z"
}
```

### 11. Get Conversation History

```bash
curl -X GET http://localhost:5003/conversation/user_123
```

**Response:**
```json
{
  "success": true,
  "conversation": {
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
    ]
  }
}
```

### 12. End Conversation

```bash
curl -X DELETE http://localhost:5003/conversation/user_123
```

**Response:**
```json
{
  "success": true,
  "message": "Conversation ended"
}
```

### 13. Health Check

```bash
curl -X GET http://localhost:5003/health
```

**Response:**
```json
{
  "status": "healthy",
  "active_conversations": 1,
  "hotel_server_url": "http://localhost:5001"
}
```

## 🎯 Complete Conversation Flow

Here's a complete conversation flow using curl:

```bash
#!/bin/bash

# 1. Trigger conversation
USER_ID="user_$(date +%s)"
echo "Starting conversation for user: $USER_ID"

TRIGGER_RESPONSE=$(curl -s -X POST http://localhost:5003/trigger \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"$USER_ID\"}")

echo "Trigger response: $TRIGGER_RESPONSE"

# 2. Send location
curl -s -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"$USER_ID\", \"message\": \"मुझे Mumbai में hotel चाहिए\"}"

# 3. Send dates
curl -s -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"$USER_ID\", \"message\": \"Check-in 20 December और check-out 23 December\"}"

# 4. Send guests
curl -s -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"$USER_ID\", \"message\": \"2 adults और 1 child\"}"

# 5. Send rooms
curl -s -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"$USER_ID\", \"message\": \"1 room चाहिए\"}"

# 6. Send amenities
curl -s -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"$USER_ID\", \"message\": \"WiFi और pool चाहिए\"}"

# 7. Send budget
curl -s -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"$USER_ID\", \"message\": \"Budget 10,000 से 20,000 rupees per night\"}"

# 8. Send star rating
curl -s -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"$USER_ID\", \"message\": \"5 star hotels चाहिए\"}"

# 9. Send guest rating
curl -s -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"$USER_ID\", \"message\": \"4 plus rating चाहिए\"}"

# 10. Send name
curl -s -X POST http://localhost:5003/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"$USER_ID\", \"message\": \"मेरा नाम Rahul है\"}"

# 11. Get conversation history
curl -s -X GET http://localhost:5003/conversation/$USER_ID

# 12. End conversation
curl -s -X DELETE http://localhost:5003/conversation/$USER_ID

echo "Conversation completed for user: $USER_ID"
```

## 🔧 Integration Examples

### Python Integration

```python
import requests
import json

class VoiceAgentClient:
    def __init__(self, base_url="http://localhost:5003"):
        self.base_url = base_url
    
    def start_conversation(self, user_id):
        response = requests.post(f"{self.base_url}/trigger", json={"user_id": user_id})
        return response.json()
    
    def send_message(self, user_id, message):
        response = requests.post(f"{self.base_url}/chat", json={
            "user_id": user_id,
            "message": message
        })
        return response.json()
    
    def get_history(self, user_id):
        response = requests.get(f"{self.base_url}/conversation/{user_id}")
        return response.json()
    
    def end_conversation(self, user_id):
        response = requests.delete(f"{self.base_url}/conversation/{user_id}")
        return response.json()

# Usage
client = VoiceAgentClient()
conversation = client.start_conversation("user_123")
print(conversation['message'])

response = client.send_message("user_123", "मुझे Mumbai में hotel चाहिए")
print(response['response'])
```

### JavaScript Integration

```javascript
class VoiceAgentClient {
    constructor(baseUrl = 'http://localhost:5003') {
        this.baseUrl = baseUrl;
    }
    
    async startConversation(userId) {
        const response = await fetch(`${this.baseUrl}/trigger`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId })
        });
        return response.json();
    }
    
    async sendMessage(userId, message) {
        const response = await fetch(`${this.baseUrl}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, message })
        });
        return response.json();
    }
    
    async getHistory(userId) {
        const response = await fetch(`${this.baseUrl}/conversation/${userId}`);
        return response.json();
    }
    
    async endConversation(userId) {
        const response = await fetch(`${this.baseUrl}/conversation/${userId}`, {
            method: 'DELETE'
        });
        return response.json();
    }
}

// Usage
const client = new VoiceAgentClient();
client.startConversation('user_123').then(conversation => {
    console.log(conversation.message);
});

client.sendMessage('user_123', 'मुझे Mumbai में hotel चाहिए').then(response => {
    console.log(response.response);
});
```

## 🎯 Key Features

✅ **Hindi/Hinglish conversation flow**  
✅ **Step-by-step information collection**  
✅ **Natural language processing**  
✅ **Hotel search integration**  
✅ **Conversation state management**  
✅ **Ticket number generation**  
✅ **Complete conversation history**  

## 🚀 Ready to Use!

The Voice Agent Trigger API is now ready for integration with your voice agent system. It provides a complete Hindi/Hinglish hotel booking conversation flow that can be triggered via API calls.
