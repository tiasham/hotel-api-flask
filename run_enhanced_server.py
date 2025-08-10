#!/usr/bin/env python3
"""
Enhanced Retell-Specific MCP Server Runner
"""
import os
import sys
import subprocess
import time
import signal
import requests
from datetime import datetime

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = ['flask', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def check_port_availability(port):
    """Check if the specified port is available"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def wait_for_server(url, max_attempts=30):
    """Wait for server to be ready"""
    print(f"⏳ Waiting for server to start at {url}...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{url}/health", timeout=2)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Server is ready!")
                print(f"   Status: {data.get('status', 'unknown')}")
                print(f"   Hotels: {data.get('hotels_count', 'N/A')}")
                print(f"   Bookings: {data.get('bookings_count', 'N/A')}")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        if attempt % 5 == 0:
            print(f"   Still waiting... ({attempt + 1}/{max_attempts})")
    
    print("❌ Server failed to start within expected time")
    return False

def run_server():
    """Run the enhanced Retell server"""
    print("🚀 Starting Enhanced Retell-Specific MCP Server")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Set up environment
    port = int(os.environ.get('PORT', 5001))
    host = '0.0.0.0'
    
    # Check port availability
    if not check_port_availability(port):
        print(f"❌ Port {port} is already in use")
        print(f"   Please stop any existing server or use a different port")
        print(f"   You can set a different port with: export PORT=<port_number>")
        return False
    
    print(f"🔧 Server configuration:")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   URL: http://localhost:{port}")
    
    # Start the server
    print(f"\n🚀 Starting server...")
    try:
        # Import and run the server
        from retell_specific_server import app
        
        print(f"✅ Server started successfully!")
        print(f"📡 Server URL: http://localhost:{port}")
        print(f"🔗 Health check: http://localhost:{port}/health")
        print(f"🛠️  Tools endpoint: http://localhost:{port}/tools")
        print(f"⚡ Execute endpoint: http://localhost:{port}/execute")
        
        print(f"\n📋 Available endpoints:")
        print(f"   GET  /         - Server information")
        print(f"   GET  /health   - Health check")
        print(f"   GET  /tools    - Available tools")
        print(f"   POST /execute  - Execute tools")
        
        print(f"\n🛠️  Available tools:")
        print(f"   - searchHotels     - Search for hotels")
        print(f"   - getHotelDetails  - Get hotel details")
        print(f"   - createBooking    - Create booking")
        print(f"   - getBooking       - Get booking details")
        print(f"   - cancelBooking    - Cancel booking")
        print(f"   - getLocations     - Get locations")
        print(f"   - getAmenities     - Get amenities")
        print(f"   - getRoomTypes     - Get room types")
        
        print(f"\n🧪 To test the server, run:")
        print(f"   python test_enhanced_retell_server.py")
        
        print(f"\n⏹️  Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run the Flask app
        app.run(debug=False, host=host, port=port)
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def main():
    """Main function"""
    try:
        success = run_server()
        if success:
            print("✅ Server stopped successfully")
        else:
            print("❌ Server failed to start")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 