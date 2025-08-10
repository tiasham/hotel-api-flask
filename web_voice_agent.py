#!/usr/bin/env python3
"""
Web-based Voice Agent
- STT (Speech-to-Text) using Web Speech API
- TTS (Text-to-Speech) using Web Speech API
- VAD (Voice Activity Detection) using Web Audio API
- Dialogue Manager
- Hotel API Integration
"""
from flask import Flask, request, jsonify, render_template_string
import requests
import json
import logging
from datetime import datetime
from typing import Dict, List
import re
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class HotelAPI:
    """Hotel API integration"""
    
    def __init__(self, base_url: str = "https://hotel-api-flask-production.up.railway.app"):
        self.base_url = base_url
    
    def search_hotels(self, parameters: Dict) -> Dict:
        """Search hotels using the API"""
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json={
                    "name": "searchHotels",
                    "arguments": parameters
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Hotel API error: {e}")
            return {"error": str(e), "hotels": []}
    
    def get_locations(self) -> List[str]:
        """Get available locations"""
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json={
                    "name": "getLocations",
                    "arguments": {}
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result.get("result", {}).get("locations", [])
        except Exception as e:
            logger.error(f"Locations API error: {e}")
            return []
    
    def get_amenities(self) -> List[str]:
        """Get available amenities"""
        try:
            response = requests.post(
                f"{self.base_url}/execute",
                json={
                    "name": "getAmenities",
                    "arguments": {}
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result.get("result", {}).get("amenities", [])
        except Exception as e:
            logger.error(f"Amenities API error: {e}")
            return []

class DialogueManager:
    """Manages conversation flow and context"""
    
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.current_context: Dict = {}
        self.hotel_api = HotelAPI()
        
        # Available locations and amenities
        self.locations = self.hotel_api.get_locations()
        self.amenities = self.hotel_api.get_amenities()
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def extract_search_parameters(self, user_input: str) -> Dict:
        """Extract hotel search parameters from user input"""
        params = {}
        
        # Extract location
        for location in self.locations:
            if location.lower() in user_input.lower():
                params["location"] = location
                break
        
        # Extract number of adults
        adults_match = re.search(r'(\d+)\s*(adult|adults|person|people)', user_input.lower())
        if adults_match:
            params["adults"] = int(adults_match.group(1))
        
        # Extract number of children
        children_match = re.search(r'(\d+)\s*(child|children|kid|kids)', user_input.lower())
        if children_match:
            params["children"] = int(children_match.group(1))
        
        # Extract amenities
        found_amenities = []
        for amenity in self.amenities:
            if amenity.lower() in user_input.lower():
                found_amenities.append(amenity)
        if found_amenities:
            params["amenities"] = ",".join(found_amenities)
        
        # Extract price range
        price_match = re.search(r'(\d+)\s*(to|-)\s*(\d+)\s*(rs|rupees|price)', user_input.lower())
        if price_match:
            params["min_price"] = int(price_match.group(1))
            params["max_price"] = int(price_match.group(3))
        
        # Extract star rating
        stars_match = re.search(r'(\d+)\s*star', user_input.lower())
        if stars_match:
            params["min_stars"] = int(stars_match.group(1))
        
        return params
    
    def generate_response(self, user_input: str) -> str:
        """Generate appropriate response based on user input"""
        self.add_message("user", user_input)
        
        # Check if user wants to search for hotels
        search_keywords = ["hotel", "book", "search", "find", "stay", "accommodation"]
        is_search_request = any(keyword in user_input.lower() for keyword in search_keywords)
        
        if is_search_request:
            # Extract search parameters
            params = self.extract_search_parameters(user_input)
            
            if not params.get("location"):
                return "I'd be happy to help you find a hotel! Which city or location would you like to stay in?"
            
            if not params.get("adults"):
                return f"Great! I can help you find hotels in {params['location']}. How many adults will be traveling?"
            
            # Search for hotels
            result = self.hotel_api.search_hotels(params)
            
            if result.get("success") and result.get("result", {}).get("hotels"):
                hotels = result["result"]["hotels"]
                response = f"I found {len(hotels)} hotels in {params['location']} that match your criteria:\n\n"
                
                for i, hotel in enumerate(hotels[:3], 1):  # Show top 3
                    response += f"{i}. {hotel['name']} - {hotel['stars']} stars, Rating: {hotel['guest_rating']}/5\n"
                    response += f"   Price: ₹{hotel['price_per_night']}/night, Amenities: {hotel['amenities']}\n\n"
                
                response += "Would you like me to provide more details about any of these hotels?"
            else:
                response = f"I couldn't find hotels matching your criteria in {params['location']}. Would you like to try different search parameters?"
        else:
            # General conversation
            response = "Hello! I'm your hotel booking assistant. I can help you find and book hotels. What would you like to do?"
        
        self.add_message("assistant", response)
        return response

# Initialize dialogue manager
dialogue_manager = DialogueManager()

# HTML template for the voice agent interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hotel Voice Agent</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 30px;
            max-width: 600px;
            width: 100%;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #333;
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            color: #666;
            margin: 10px 0 0 0;
        }
        .voice-controls {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .btn-primary {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        .btn-secondary {
            background: #f8f9fa;
            color: #333;
            border: 2px solid #e9ecef;
        }
        .btn-secondary:hover {
            background: #e9ecef;
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .conversation {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
        }
        .assistant-message {
            background: white;
            color: #333;
            border: 1px solid #e9ecef;
        }
        .status {
            text-align: center;
            color: #666;
            font-style: italic;
            margin: 10px 0;
        }
        .mic-icon {
            width: 20px;
            height: 20px;
            fill: currentColor;
        }
        .pulse {
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏨 Hotel Voice Agent</h1>
            <p>Your AI-powered hotel booking assistant</p>
        </div>
        
        <div class="voice-controls">
            <button id="startBtn" class="btn btn-primary">
                <svg class="mic-icon" viewBox="0 0 24 24">
                    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                    <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
                Start Listening
            </button>
            <button id="stopBtn" class="btn btn-secondary" disabled>Stop</button>
        </div>
        
        <div class="status" id="status">Click "Start Listening" to begin</div>
        
        <div class="conversation" id="conversation">
            <div class="message assistant-message">
                Hello! I'm your hotel booking assistant. I can help you find and book hotels. What would you like to do?
            </div>
        </div>
    </div>

    <script>
        class VoiceAgent {
            constructor() {
                this.recognition = null;
                this.synthesis = window.speechSynthesis;
                this.isListening = false;
                this.isSpeaking = false;
                
                this.initializeSpeechRecognition();
                this.bindEvents();
            }
            
            initializeSpeechRecognition() {
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    this.recognition = new SpeechRecognition();
                    
                    this.recognition.continuous = false;
                    this.recognition.interimResults = false;
                    this.recognition.lang = 'en-US';
                    
                    this.recognition.onstart = () => {
                        this.isListening = true;
                        this.updateUI();
                        this.updateStatus('Listening... Speak now!');
                    };
                    
                    this.recognition.onresult = (event) => {
                        const transcript = event.results[0][0].transcript;
                        this.addMessage('user', transcript);
                        this.updateStatus('Processing your request...');
                        
                        // Send to backend
                        this.sendToBackend(transcript);
                    };
                    
                    this.recognition.onerror = (event) => {
                        console.error('Speech recognition error:', event.error);
                        this.updateStatus('Error: ' + event.error);
                        this.stopListening();
                    };
                    
                    this.recognition.onend = () => {
                        this.isListening = false;
                        this.updateUI();
                        this.updateStatus('Click "Start Listening" to begin');
                    };
                } else {
                    this.updateStatus('Speech recognition not supported in this browser');
                }
            }
            
            bindEvents() {
                document.getElementById('startBtn').addEventListener('click', () => {
                    this.startListening();
                });
                
                document.getElementById('stopBtn').addEventListener('click', () => {
                    this.stopListening();
                });
            }
            
            startListening() {
                if (this.recognition && !this.isListening) {
                    this.recognition.start();
                }
            }
            
            stopListening() {
                if (this.recognition && this.isListening) {
                    this.recognition.stop();
                }
            }
            
            updateUI() {
                const startBtn = document.getElementById('startBtn');
                const stopBtn = document.getElementById('stopBtn');
                
                if (this.isListening) {
                    startBtn.disabled = true;
                    stopBtn.disabled = false;
                    startBtn.classList.add('pulse');
                } else {
                    startBtn.disabled = false;
                    stopBtn.disabled = true;
                    startBtn.classList.remove('pulse');
                }
            }
            
            updateStatus(message) {
                document.getElementById('status').textContent = message;
            }
            
            addMessage(role, content) {
                const conversation = document.getElementById('conversation');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${role}-message`;
                messageDiv.textContent = content;
                conversation.appendChild(messageDiv);
                conversation.scrollTop = conversation.scrollHeight;
            }
            
            async sendToBackend(userInput) {
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: userInput })
                    });
                    
                    const data = await response.json();
                    const assistantResponse = data.response;
                    
                    this.addMessage('assistant', assistantResponse);
                    this.speak(assistantResponse);
                    
                } catch (error) {
                    console.error('Error sending to backend:', error);
                    this.updateStatus('Error communicating with server');
                }
            }
            
            speak(text) {
                if (this.isSpeaking) {
                    this.synthesis.cancel();
                }
                
                this.isSpeaking = true;
                this.updateStatus('Speaking...');
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.9;
                utterance.pitch = 1;
                utterance.volume = 1;
                
                utterance.onstart = () => {
                    this.isSpeaking = true;
                };
                
                utterance.onend = () => {
                    this.isSpeaking = false;
                    this.updateStatus('Click "Start Listening" to begin');
                };
                
                utterance.onerror = (event) => {
                    console.error('Speech synthesis error:', event.error);
                    this.isSpeaking = false;
                    this.updateStatus('Error with speech synthesis');
                };
                
                this.synthesis.speak(utterance);
            }
        }
        
        // Initialize voice agent when page loads
        document.addEventListener('DOMContentLoaded', () => {
            new VoiceAgent();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Serve the voice agent interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Generate response using dialogue manager
        response = dialogue_manager.generate_response(user_message)
        
        return jsonify({'response': response})
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Voice Agent is running',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port) 