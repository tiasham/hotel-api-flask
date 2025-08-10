# 📞 Twilio Voice Agent Setup Guide

Complete setup guide for the Hindi/Hinglish hotel booking voice agent using Twilio.

## 🎯 What You'll Get

- **📞 Phone number** that customers can call
- **🎤 Speech recognition** - understands Hindi/Hinglish
- **🗣️ Text-to-speech** - responds in Hindi/Hinglish
- **🏨 Hotel booking** - complete booking flow
- **📱 SMS confirmation** - sends booking details

## 🚀 Quick Setup

### 1. Create Twilio Account

1. Go to [twilio.com](https://twilio.com)
2. Sign up for a free account
3. Get your **Account SID** and **Auth Token**

### 2. Get a Phone Number

1. In Twilio Console, go to **Phone Numbers** → **Manage** → **Buy a number**
2. Choose a number with **Voice** capability
3. Note down your phone number

### 3. Deploy the Voice Agent

#### Option A: Deploy to Railway (Recommended)

```bash
# Update Procfile
echo "web: gunicorn twilio_voice_agent:app" > Procfile

# Commit and push
git add .
git commit -m "Add Twilio voice agent"
git push origin main
```

#### Option B: Deploy to Heroku

```bash
# Create Heroku app
heroku create your-twilio-voice-agent

# Set environment variables
heroku config:set TWILIO_ACCOUNT_SID=your_account_sid
heroku config:set TWILIO_AUTH_TOKEN=your_auth_token

# Deploy
git push heroku main
```

### 4. Configure Twilio Webhook

1. In Twilio Console, go to your phone number
2. Set **Voice Configuration**:
   - **Webhook URL**: `https://your-app.railway.app/incoming_call`
   - **HTTP Method**: `POST`

## 🔧 Environment Variables

Set these in your deployment platform:

```bash
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
```

## 📞 How It Works

### Call Flow

1. **Customer calls** your Twilio number
2. **Agent greets** in Hindi/Hinglish: "Hey, welcome to Cleartrip Hotel Support!"
3. **Collects information** step by step:
   - Location (Mumbai, Delhi, etc.)
   - Dates (check-in/check-out)
   - Guests (adults/children)
   - Rooms needed
   - Amenities (WiFi, Pool, etc.)
   - Budget range
   - Customer name
4. **Searches hotels** and presents options
5. **Confirms booking** and sends SMS

### Example Conversation

**Agent**: "Hey, welcome to Cleartrip Hotel Support! मैं राज बोल रहा हूँ — super excited हूँ आपकी hotel booking में help करने के लिए! बताइए, कहाँ जाना है आपको?"

**Customer**: "मुझे Mumbai में hotel चाहिए"

**Agent**: "Great! Mumbai में होटल ढूंढेंगे। Check-in और check-out की dates क्या होंगी?"

**Customer**: "15th December से 18th December"

**Agent**: "Perfect! Adult और बच्चे — कितने लोग जा रहे हैं?"

**Customer**: "2 adults और 1 child"

**Agent**: "Perfect Rahul! मैंने आपके लिए 3 hotels ढूंढे हैं Mumbai में। एक शानदार option है Taj Mahal Palace, ये एक 5-star property है, guest rating है 4.8/5, और price around 15000 rupees per night है। मैंने Taj Mahal Palace को आपके cart में डाल दिया है — आप आराम से review कर सकते हैं। जब आप ready हों, बस बता दीजिए — मैं तुरंत booking confirm कर दूँगा।"

## 🧪 Testing

### Test Locally

```bash
# Install dependencies
pip install -r requirements_twilio.txt

# Run the agent
python twilio_voice_agent.py

# Test conversation
curl -X POST http://localhost:5001/test_conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "मुझे Mumbai में hotel चाहिए"}'
```

### Test with Twilio

1. **Use ngrok** for local testing:
   ```bash
   ngrok http 5001
   ```

2. **Update Twilio webhook** to your ngrok URL:
   ```
   https://your-ngrok-url.ngrok.io/incoming_call
   ```

3. **Call your Twilio number** and test the conversation

## 📱 SMS Integration

Add SMS confirmation by updating the `handle_speech` function:

```python
from twilio.rest import Client

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Send SMS confirmation
message = client.messages.create(
    body=f"Booking confirmed! Hotel: {hotel_name}, Dates: {check_in} to {check_out}",
    from_=twilio_number,
    to=customer_number
)
```

## 🎨 Customization

### Change Voice

Update the TwiML voice attribute:

```xml
<Say voice="alice" language="en-IN">Your message</Say>
```

Available voices: `alice`, `man`, `woman`

### Add More Locations

Update the `locations` list in `TwilioDialogueManager`:

```python
self.locations = ["Mumbai", "Delhi", "Bangalore", "Your_City"]
```

### Add More Hotels

Update the `sample_hotels` dictionary:

```python
self.sample_hotels["Your_City"] = [
    {"name": "Hotel Name", "stars": 5, "rating": 4.8, "price": 10000, "amenities": "WiFi,Pool"}
]
```

## 🔍 Troubleshooting

### Common Issues

1. **Webhook not receiving calls**
   - Check webhook URL is correct
   - Ensure HTTPS is used
   - Verify server is running

2. **Speech not recognized**
   - Check language setting (`en-IN`)
   - Ensure clear audio
   - Test with simple words first

3. **Agent not responding**
   - Check server logs
   - Verify dialogue manager is working
   - Test with `/test_conversation` endpoint

### Debug Mode

Enable debug logging:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 💰 Pricing

- **Twilio Phone Number**: ~$1/month
- **Voice Calls**: ~$0.01/minute
- **SMS**: ~$0.0075/message
- **Speech Recognition**: Included in voice calls

## 🎉 Success!

Your Twilio voice agent is now ready to handle hotel booking calls in Hindi/Hinglish! 🏨📞

## 📞 Support

- **Twilio Documentation**: [twilio.com/docs](https://twilio.com/docs)
- **Voice Agent Issues**: Check server logs
- **Webhook Issues**: Use Twilio Console logs 