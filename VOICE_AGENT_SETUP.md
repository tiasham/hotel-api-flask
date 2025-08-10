# Custom Voice Agent Setup Guide

Build your own hotel booking voice agent using LiveKit Agents Framework with GPT-4o, Whisper STT, and ElevenLabs TTS!

## 🚀 Quick Start

### Option 1: Web Interface (Easy Testing)
```bash
# 1. Install dependencies
pip install -r requirements_voice_agent.txt

# 2. Set up configuration
python voice_agent_config.py
cp .env.sample .env
# Edit .env with your API keys

# 3. Start hotel server
python run_enhanced_server.py

# 4. Start web interface
python voice_agent_web.py

# 5. Open http://localhost:5002 in browser
```

### Option 2: LiveKit Voice Agent (Full Voice Experience)
```bash
# 1. Install dependencies
pip install -r requirements_voice_agent.txt

# 2. Set up configuration
python voice_agent_config.py
cp .env.sample .env
# Edit .env with your API keys

# 3. Start hotel server
python run_enhanced_server.py

# 4. Start voice agent
python run_livekit_agent.py
```

## 🔧 API Setup

### OpenAI (GPT-4o + Whisper)
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account and get your API key
3. Add to `.env`: `OPENAI_API_KEY=your-key-here`

### ElevenLabs (TTS)
1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Sign up and get your API key
3. Add to `.env`: `ELEVENLABS_API_KEY=your-key-here`
4. Choose a voice: `ELEVENLABS_VOICE=Rachel`

### LiveKit (Real-time Communication)
1. Go to [LiveKit Cloud](https://cloud.livekit.io/)
2. Create an account and project
3. Get your API key and secret
4. Add to `.env`:
   ```
   LIVEKIT_URL=wss://your-project.livekit.cloud
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   ```

### Local LiveKit Server (Alternative)
```bash
# Install LiveKit CLI
curl -sSL https://get.livekit.io | bash

# Start local server
livekit-server --dev
```

## 📁 Project Structure

```
hotel_api.py/
├── retell_specific_server.py      # Enhanced hotel booking server
├── livekit_voice_agent.py         # LiveKit Agents voice agent
├── voice_agent_web.py             # Web interface for testing
├── run_livekit_agent.py           # Voice agent runner
├── voice_agent_config.py          # Configuration management
├── requirements_voice_agent.txt   # Dependencies
├── templates/
│   └── voice_agent.html          # Web UI template
├── .env                          # API keys (create from .env.sample)
└── VOICE_AGENT_SETUP.md          # This guide
```

## 🎯 Features

### Voice Agent Capabilities (LiveKit Agents)
- **Real-time voice communication** via LiveKit Agents Framework
- **Speech-to-text** using OpenAI Whisper
- **Natural language processing** using GPT-4o
- **Text-to-speech** using ElevenLabs
- **Voice Activity Detection** using Silero VAD
- **Hotel booking integration** with our enhanced server

### Web Interface Capabilities
- **Text-based chat** for easy testing
- **Real-time conversation history**
- **Example queries** for quick testing
- **Status monitoring** and debugging

### Hotel Booking Features
- **Search hotels** by location, amenities, price
- **Get hotel details** with availability
- **Create bookings** with validation
- **Manage bookings** (view, cancel)
- **Real-time availability** checking

## 🔄 Architecture Flow

### LiveKit Voice Agent
```
User Voice → LiveKit → Silero VAD → Whisper STT → GPT-4o → Hotel Server → ElevenLabs TTS → LiveKit → User
```

### Web Interface
```
User Text → Flask → GPT-4o → Hotel Server → Response → Web UI
```

## 🛠️ Configuration Options

### Voice Settings
```env
ELEVENLABS_VOICE=Rachel          # Voice personality
SAMPLE_RATE=16000                # Audio quality
CHANNELS=1                       # Mono audio
```

### GPT-4o Settings
```env
GPT_MODEL=gpt-4o                 # AI model
GPT_MAX_TOKENS=500               # Response length
GPT_TEMPERATURE=0.7              # Creativity level
```

### LiveKit Settings
```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
```

### Conversation Settings
```env
MAX_CONVERSATION_HISTORY=10      # Memory length
RESPONSE_TIMEOUT=30              # Timeout seconds
```

## 🧪 Testing

### Web Interface Testing (Recommended for Development)
1. Start the web interface: `python voice_agent_web.py`
2. Open http://localhost:5002
3. Try example queries:
   - "Find hotels in Mumbai"
   - "Search for hotels with pool in Delhi"
   - "What amenities do you have?"
   - "Book a room for 2 adults"

### Voice Testing (Production)
1. Set up LiveKit room
2. Run voice agent: `python run_livekit_agent.py`
3. Join room with audio device
4. Test voice interactions:
   - "Find hotels in Mumbai"
   - "Book a room for 2 adults and 1 child"
   - "What amenities do you have?"
   - "Cancel my booking"

### API Testing
```bash
# Test hotel server
curl http://localhost:5001/health

# Test voice agent web API
curl http://localhost:5002/api/status
```

## 🔍 Troubleshooting

### Common Issues

#### 1. LiveKit Agents Import Error
```
Error: No module named 'livekit_agents'
```
**Solution**: Install the LiveKit Agents framework:
```bash
pip install livekit-agents
```

#### 2. API Key Errors
```
Error: OPENAI_API_KEY is required
```
**Solution**: Check your `.env` file and ensure all API keys are set correctly.

#### 3. LiveKit Connection Issues
```
Error: Failed to connect to LiveKit
```
**Solution**: 
- Verify LiveKit URL, API key, and secret
- Check if LiveKit server is running
- Try local LiveKit server for testing

#### 4. Hotel Server Not Found
```
Error: Failed to load tools from hotel server
```
**Solution**: Ensure hotel server is running on port 5001

#### 5. Audio Issues
```
Error: Audio processing failed
```
**Solution**: 
- Check audio device permissions
- Verify sample rate and channel settings
- Test with web interface first

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python run_livekit_agent.py
```

### Health Checks
```bash
# Check hotel server
curl http://localhost:5001/health

# Check voice agent web interface
curl http://localhost:5002/api/status

# Check LiveKit
curl https://your-livekit-url/health
```

## 🚀 Production Deployment

### Environment Variables
```bash
# Production settings
export FLASK_ENV=production
export LOG_LEVEL=INFO
export PORT=5002
```

### Security
```bash
# Use strong secret key
export FLASK_SECRET_KEY=your-strong-secret-key

# Enable HTTPS
export HTTPS_ENABLED=true
```

### Scaling
- **Load balancing** for multiple voice agents
- **Redis** for conversation state
- **Database** for persistent storage
- **CDN** for static assets

## 📊 Monitoring

### Logs
```bash
# View logs
tail -f voice_agent.log

# Monitor API calls
grep "API call" voice_agent.log
```

### Metrics
- Conversation success rate
- API response times
- Error rates
- User satisfaction

## 🔮 Future Enhancements

### Planned Features
- **Multi-language support** (Hindi, Spanish, etc.)
- **Voice biometrics** for user identification
- **Advanced NLP** for better intent recognition
- **Payment integration** for bookings
- **SMS notifications** for confirmations
- **Analytics dashboard** for insights

### Technical Improvements
- **WebRTC** for better audio quality
- **Custom Whisper models** for domain-specific speech
- **Fine-tuned GPT models** for hotel booking
- **Real-time translation** for international users

## 📞 Support

### Getting Help
1. Check this setup guide
2. Review error logs
3. Test with web interface first
4. Verify all API keys are valid
5. Check network connectivity

### Useful Commands
```bash
# Check all services
python voice_agent_config.py
python test_enhanced_retell_server.py

# Restart services
pkill -f "python.*voice_agent"
pkill -f "python.*retell_specific_server"

# View running processes
ps aux | grep python
```

### Development Workflow
1. **Start with web interface** for quick testing and debugging
2. **Test voice agent** once web interface works
3. **Use LiveKit Agents** for production voice interactions
4. **Monitor logs** for any issues

---

**Ready to build your voice agent!** 🎉

This setup gives you a complete, production-ready voice agent for hotel booking with cutting-edge AI technology using the LiveKit Agents framework.
