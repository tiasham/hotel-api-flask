# 🏨 LiveKit Voice Agent - Hotel Booking Assistant

A **Hindi/Hinglish voice agent** for hotel booking using LiveKit framework with STT, TTS, VAD, and hotel API integration.

## 🎯 Features

- **🎤 Speech-to-Text (STT)** - Converts user speech to text
- **🗣️ Text-to-Speech (TTS)** - Converts responses to speech
- **🎵 Voice Activity Detection (VAD)** - Detects when user is speaking
- **🧠 Dialogue Manager** - Manages conversation flow in Hindi/Hinglish
- **🏨 Hotel API Integration** - Searches and books hotels
- **🇮🇳 Hindi/Hinglish Support** - Natural conversation in mixed language

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_livekit.txt
```

### 2. Setup LiveKit Environment

You need a LiveKit server. You can either:

**Option A: Use LiveKit Cloud (Recommended)**
- Sign up at [livekit.io](https://livekit.io)
- Get your API key and secret

**Option B: Self-host LiveKit**
- Follow [LiveKit self-hosting guide](https://docs.livekit.io/deploy/)

### 3. Set Environment Variables

```bash
export LIVEKIT_URL="wss://your-livekit-server.com"
export LIVEKIT_API_KEY="your_api_key"
export LIVEKIT_API_SECRET="your_api_secret"
```

### 4. Run the Voice Agent

```bash
python deploy_livekit_agent.py
```

## 🎭 Agent Personality

The agent is **"राज"** - a friendly, professional male hotel booking agent from Cleartrip team who:

- Speaks in **Hinglish** (Hindi + English)
- Uses **Devanagari script** for Hindi words
- Maintains **excited and respectful** tone
- Follows **step-by-step booking process**

## 💬 Conversation Flow

1. **Greeting**: "Hey, welcome to Cleartrip Hotel Support! मैं राज बोल रहा हूँ..."
2. **Location**: "सबसे पहले बताइए — आपको किस शहर में होटल चाहिए?"
3. **Dates**: "Check-in और check-out की dates क्या होंगी?"
4. **Guests**: "Adult और बच्चे — कितने लोग जा रहे हैं?"
5. **Rooms**: "आपको कितने rooms की ज़रूरत होगी?"
6. **Amenities**: "कोई specific amenities चाहिए?"
7. **Price**: "आपका budget क्या है?"
8. **Name**: "अपना नाम बता दीजिए"
9. **Search**: API call to find hotels
10. **Results**: Present top 2-3 hotels in Hinglish
11. **Booking**: Add to cart and confirm

## 🔧 API Integration

The agent integrates with your hotel API at:
```
https://hotel-api-flask-production.up.railway.app
```

**Available API Endpoints:**
- `POST /execute` - Search hotels, get locations, get amenities
- `GET /health` - Health check

## 📁 File Structure

```
├── livekit_voice_agent.py      # Main voice agent
├── deploy_livekit_agent.py     # Deployment script
├── requirements_livekit.txt    # Dependencies
├── README_LIVEKIT.md          # This file
└── Hotel_Dataset.csv          # Hotel data
```

## 🎯 Example Conversation

**Agent**: "Hey, welcome to Cleartrip Hotel Support! मैं राज बोल रहा हूँ — super excited हूँ आपकी hotel booking में help करने के लिए! बताइए, कहाँ जाना है आपको?"

**User**: "मुझे Mumbai में hotel चाहिए"

**Agent**: "Great! Mumbai में होटल ढूंढेंगे। Check-in और check-out की dates क्या होंगी?"

**User**: "15th December से 18th December"

**Agent**: "Perfect! Adult और बच्चे — कितने लोग जा रहे हैं?"

**User**: "2 adults और 1 child"

**Agent**: "आपको कितने rooms की ज़रूरत होगी?"

**User**: "1 room"

**Agent**: "अपना नाम बता दीजिए"

**User**: "मेरा नाम Rahul है"

**Agent**: "Perfect Rahul! मैंने आपके लिए 3 hotels ढूंढे हैं Mumbai में। एक शानदार option है Hotel A, ये एक 4-star property है, guest rating है 4.5/5, और price around 5000 rupees per night है। मैंने Hotel A को आपके cart में डाल दिया है — आप आराम से review कर सकते हैं। जब आप ready हों, बस बता दीजिए — मैं तुरंत booking confirm कर दूँगा।"

## 🛠️ Customization

### Modify System Prompt

Edit the `system_prompt` in `HindiDialogueManager` class:

```python
self.system_prompt = """Your custom prompt here"""
```

### Add New Locations

Update the hotel API or modify the locations list:

```python
self.locations = ["Mumbai", "Delhi", "Bangalore", "Your_City"]
```

### Change Agent Personality

Modify the greeting and response patterns in `generate_response()` method.

## 🔍 Troubleshooting

### Common Issues

1. **LiveKit Connection Failed**
   - Check your `LIVEKIT_URL`, `API_KEY`, and `API_SECRET`
   - Ensure LiveKit server is running

2. **Audio Issues**
   - Check microphone permissions
   - Ensure audio drivers are working

3. **API Errors**
   - Verify hotel API is running
   - Check network connectivity

### Debug Mode

Enable debug logging:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

For issues with:
- **LiveKit**: [LiveKit Documentation](https://docs.livekit.io/)
- **Voice Agent**: Check this README
- **Hotel API**: Check your API deployment

## 🎉 Success!

Your LiveKit voice agent is now ready to help users book hotels in natural Hindi/Hinglish conversation! 🏨🎤 