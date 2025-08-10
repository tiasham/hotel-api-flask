#!/usr/bin/env python3
"""
Runner script for LiveKit Voice Agent
"""
import logging
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed"""
    logger.info("🔍 Checking dependencies...")
    
    required_packages = [
        'livekit_agents',
        'openai', 
        'elevenlabs',
        'torch',
        'torchaudio'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            logger.info(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            logger.error(f"❌ {package} is missing")
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.error("Please install missing packages:")
        logger.error(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_configuration():
    """Check if required environment variables are set"""
    logger.info("🔧 Checking configuration...")
    
    required_vars = [
        'OPENAI_API_KEY',
        'ELEVENLABS_API_KEY',
        'LIVEKIT_URL',
        'LIVEKIT_API_KEY',
        'LIVEKIT_API_SECRET'
    ]
    
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            logger.error(f"❌ {var} is not set")
    
    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these in your .env file")
        return False
    
    logger.info("✅ Configuration is valid")
    return True

def check_hotel_server():
    """Check if hotel server is running"""
    logger.info("🏨 Checking hotel server...")
    
    try:
        import requests
        hotel_url = os.getenv('HOTEL_SERVER_URL', 'http://localhost:5001')
        response = requests.get(f"{hotel_url}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Hotel server is running")
            logger.info(f"   Hotels: {data.get('hotels_count', 'N/A')}")
            logger.info(f"   Bookings: {data.get('bookings_count', 'N/A')}")
            return True
        else:
            logger.error(f"❌ Hotel server returned status {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Cannot connect to hotel server: {e}")
        logger.error("Please start the hotel server first:")
        logger.error("python run_enhanced_server.py")
        return False

def run_voice_agent():
    """Run the LiveKit voice agent"""
    logger.info("🚀 Starting LiveKit Voice Agent...")
    
    try:
        from livekit_agents import run_app
        from livekit_agents import WorkerOptions
        from livekit_voice_agent import entrypoint
        
        # Configure worker options
        options = WorkerOptions(
            url=os.getenv("LIVEKIT_URL"),
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET"),
        )
        
        logger.info(f"📡 Connecting to LiveKit: {os.getenv('LIVEKIT_URL')}")
        logger.info("🎤 Voice agent is ready!")
        logger.info("   - Say 'Find hotels in Mumbai' to search")
        logger.info("   - Say 'Book a room' to start booking")
        logger.info("   - Say 'What amenities do you have?' for info")
        logger.info("⏹️  Press Ctrl+C to stop")
        
        # Run the agent
        import asyncio
        asyncio.run(run_app(entrypoint, options))
        
    except KeyboardInterrupt:
        logger.info("⏹️  Voice agent stopped by user")
    except Exception as e:
        logger.error(f"❌ Failed to start voice agent: {e}")
        return False
    
    return True

def main():
    """Main function"""
    logger.info("🏨 Hotel Booking Voice Agent")
    logger.info("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        logger.error("❌ Dependencies check failed")
        sys.exit(1)
    
    # Check configuration
    if not check_configuration():
        logger.error("❌ Configuration check failed")
        sys.exit(1)
    
    # Check hotel server
    if not check_hotel_server():
        logger.error("❌ Hotel server check failed")
        sys.exit(1)
    
    # Run voice agent
    success = run_voice_agent()
    
    if success:
        logger.info("✅ Voice agent completed successfully")
    else:
        logger.error("❌ Voice agent failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
