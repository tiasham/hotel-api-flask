#!/usr/bin/env python3
"""
Deployment script for LiveKit Voice Agent
"""
import os
import subprocess
import sys

def install_dependencies():
    """Install LiveKit dependencies"""
    print("Installing LiveKit dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_livekit.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def setup_environment():
    """Setup environment variables"""
    print("Setting up environment variables...")
    
    # Check if environment variables are set
    required_vars = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set the following environment variables:")
        print("export LIVEKIT_URL=your_livekit_url")
        print("export LIVEKIT_API_KEY=your_api_key")
        print("export LIVEKIT_API_SECRET=your_api_secret")
        return False
    
    print("✅ Environment variables configured!")
    return True

def test_agent():
    """Test the voice agent"""
    print("Testing voice agent...")
    try:
        # Test import
        from livekit_voice_agent import HindiHotelVoiceAgent
        print("✅ Voice agent imports successfully!")
        
        # Test dialogue manager
        from livekit_voice_agent import HindiDialogueManager
        dm = HindiDialogueManager()
        print("✅ Dialogue manager initialized!")
        
        return True
    except Exception as e:
        print(f"❌ Error testing agent: {e}")
        return False

def run_agent():
    """Run the voice agent"""
    print("Starting LiveKit Voice Agent...")
    try:
        subprocess.run([sys.executable, "livekit_voice_agent.py"])
    except KeyboardInterrupt:
        print("\n🛑 Voice agent stopped by user")
    except Exception as e:
        print(f"❌ Error running agent: {e}")

def main():
    """Main deployment function"""
    print("🚀 LiveKit Voice Agent Deployment")
    print("=" * 40)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        return
    
    # Step 2: Setup environment
    if not setup_environment():
        return
    
    # Step 3: Test agent
    if not test_agent():
        return
    
    # Step 4: Run agent
    print("\n🎯 Starting voice agent...")
    run_agent()

if __name__ == "__main__":
    main() 