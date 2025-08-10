#!/usr/bin/env python3
"""
Configuration file for Custom Voice Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class VoiceAgentConfig:
    """Configuration class for the voice agent"""
    
    def __init__(self):
        # OpenAI Configuration
        self.openai_api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key')
        
        # ElevenLabs Configuration
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY', 'your-elevenlabs-api-key')
        self.elevenlabs_voice = os.getenv('ELEVENLABS_VOICE', 'Rachel')
        
        # LiveKit Configuration
        self.livekit_url = os.getenv('LIVEKIT_URL', 'ws://localhost:7880')
        self.livekit_api_key = os.getenv('LIVEKIT_API_KEY', 'your-livekit-api-key')
        self.livekit_api_secret = os.getenv('LIVEKIT_API_SECRET', 'your-livekit-api-secret')
        
        # Hotel Server Configuration
        self.hotel_server_url = os.getenv('HOTEL_SERVER_URL', 'http://localhost:5001')
        
        # Voice Agent Settings
        self.room_name = os.getenv('ROOM_NAME', 'hotel-booking-room')
        self.agent_name = os.getenv('AGENT_NAME', 'Hotel Agent')
        
        # Audio Settings
        self.sample_rate = int(os.getenv('SAMPLE_RATE', '16000'))
        self.channels = int(os.getenv('CHANNELS', '1'))
        
        # Conversation Settings
        self.max_conversation_history = int(os.getenv('MAX_CONVERSATION_HISTORY', '10'))
        self.response_timeout = int(os.getenv('RESPONSE_TIMEOUT', '30'))
        
        # Whisper Settings
        self.whisper_model = os.getenv('WHISPER_MODEL', 'base')
        self.whisper_language = os.getenv('WHISPER_LANGUAGE', 'en')
        
        # GPT-4o Settings
        self.gpt_model = os.getenv('GPT_MODEL', 'gpt-4o')
        self.gpt_max_tokens = int(os.getenv('GPT_MAX_TOKENS', '500'))
        self.gpt_temperature = float(os.getenv('GPT_TEMPERATURE', '0.7'))
    
    def to_dict(self):
        """Convert configuration to dictionary"""
        return {
            'openai_api_key': self.openai_api_key,
            'elevenlabs_api_key': self.elevenlabs_api_key,
            'elevenlabs_voice': self.elevenlabs_voice,
            'livekit_url': self.livekit_url,
            'livekit_api_key': self.livekit_api_key,
            'livekit_api_secret': self.livekit_api_secret,
            'hotel_server_url': self.hotel_server_url,
            'room_name': self.room_name,
            'agent_name': self.agent_name,
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'max_conversation_history': self.max_conversation_history,
            'response_timeout': self.response_timeout,
            'whisper_model': self.whisper_model,
            'whisper_language': self.whisper_language,
            'gpt_model': self.gpt_model,
            'gpt_max_tokens': self.gpt_max_tokens,
            'gpt_temperature': self.gpt_temperature
        }
    
    def validate(self):
        """Validate configuration"""
        errors = []
        
        if not self.openai_api_key or self.openai_api_key == 'your-openai-api-key':
            errors.append("OPENAI_API_KEY is required")
        
        if not self.elevenlabs_api_key or self.elevenlabs_api_key == 'your-elevenlabs-api-key':
            errors.append("ELEVENLABS_API_KEY is required")
        
        if not self.livekit_api_key or self.livekit_api_key == 'your-livekit-api-key':
            errors.append("LIVEKIT_API_KEY is required")
        
        if not self.livekit_api_secret or self.livekit_api_secret == 'your-livekit-api-secret':
            errors.append("LIVEKIT_API_SECRET is required")
        
        return errors

# Create a sample .env file
def create_sample_env():
    """Create a sample .env file"""
    env_content = """# Voice Agent Configuration

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# ElevenLabs Configuration
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
ELEVENLABS_VOICE=Rachel

# LiveKit Configuration
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=your-livekit-api-key-here
LIVEKIT_API_SECRET=your-livekit-api-secret-here

# Hotel Server Configuration
HOTEL_SERVER_URL=http://localhost:5001

# Voice Agent Settings
ROOM_NAME=hotel-booking-room
AGENT_NAME=Hotel Agent

# Audio Settings
SAMPLE_RATE=16000
CHANNELS=1

# Conversation Settings
MAX_CONVERSATION_HISTORY=10
RESPONSE_TIMEOUT=30

# Whisper Settings
WHISPER_MODEL=base
WHISPER_LANGUAGE=en

# GPT-4o Settings
GPT_MODEL=gpt-4o
GPT_MAX_TOKENS=500
GPT_TEMPERATURE=0.7
"""
    
    with open('.env.sample', 'w') as f:
        f.write(env_content)
    
    print("Sample .env file created: .env.sample")
    print("Copy it to .env and fill in your API keys")

if __name__ == "__main__":
    # Create sample .env file
    create_sample_env()
    
    # Test configuration
    config = VoiceAgentConfig()
    errors = config.validate()
    
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Configuration is valid!")
        print(f"Hotel Server URL: {config.hotel_server_url}")
        print(f"Room Name: {config.room_name}")
        print(f"Agent Name: {config.agent_name}")
