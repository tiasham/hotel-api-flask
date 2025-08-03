#!/usr/bin/env python3
"""
MCP Server for Hotel Search API
This server implements the Model Context Protocol for Retell integration
"""

import json
import asyncio
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HotelMCPServer:
    def __init__(self):
        self.hotel_data = None
        self.load_hotel_data()
    
    def load_hotel_data(self):
        """Load hotel data from CSV file"""
        try:
            csv_file = 'Hotel_Dataset.csv'
            self.hotel_data = pd.read_csv(csv_file)
            
            # Convert date columns if they exist
            if 'check_in_date' in self.hotel_data.columns:
                self.hotel_data['check_in_date'] = pd.to_datetime(self.hotel_data['check_in_date'])
            if 'check_out_date' in self.hotel_data.columns:
                self.hotel_data['check_out_date'] = pd.to_datetime(self.hotel_data['check_out_date'])
                
            logger.info(f"Loaded {len(self.hotel_data)} hotels from {csv_file}")
        except FileNotFoundError:
            logger.warning(f"CSV file not found, creating sample data")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample hotel data if CSV doesn't exist"""
        import random
        
        locations = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Kolkata', 'Pune', 'Goa', 'Jaipur', 'Udaipur']
        amenities_list = ['WiFi', 'Pool', 'Gym', 'Restaurant', 'Spa', 'Beach', 'Mountain View', 'City View', 'Parking', 'Room Service']
        
        hotels = []
        for i in range(100):
            location = random.choice(locations)
            amenities = random.sample(amenities_list, random.randint(2, 5))
            
            hotel = {
                'hotel_id': f'HOTEL_{i+1:03d}',
                'name': f'{location} Hotel {i+1}',
                'location': location,
                'check_in_date': '2024-08-01',
                'check_out_date': '2024-08-05',
                'stars': random.randint(1, 5),
                'guest_rating': round(random.uniform(3.0, 5.0), 1),
                'amenities': ','.join(amenities),
                'price_per_night': random.randint(1000, 10000),
                'max_adults': random.randint(1, 4),
                'max_children': random.randint(0, 3)
            }
            hotels.append(hotel)
        
        self.hotel_data = pd.DataFrame(hotels)
        self.hotel_data.to_csv('Hotel_Dataset.csv', index=False)
        logger.info(f"Created sample data with {len(hotels)} hotels")
    
    def search_hotels(self, **kwargs) -> Dict[str, Any]:
        """Search hotels based on criteria"""
        try:
            df = self.hotel_data.copy()
            
            # Apply filters
            if 'location' in kwargs and kwargs['location']:
                df = df[df['location'].str.contains(kwargs['location'], case=False, na=False)]
            
            if 'check_in_date' in kwargs and kwargs['check_in_date']:
                check_in = pd.to_datetime(kwargs['check_in_date'])
                df = df[df['check_in_date'] >= check_in]
            
            if 'check_out_date' in kwargs and kwargs['check_out_date']:
                check_out = pd.to_datetime(kwargs['check_out_date'])
                df = df[df['check_out_date'] <= check_out]
            
            if 'adults' in kwargs and kwargs['adults']:
                adults = int(kwargs['adults'])
                df = df[df['max_adults'] >= adults]
            
            if 'children' in kwargs and kwargs['children']:
                children = int(kwargs['children'])
                df = df[df['max_children'] >= children]
            
            if 'amenities' in kwargs and kwargs['amenities']:
                amenities = kwargs['amenities'].split(',')
                for amenity in amenities:
                    df = df[df['amenities'].str.contains(amenity.strip(), case=False, na=False)]
            
            if 'min_price' in kwargs and kwargs['min_price']:
                min_price = float(kwargs['min_price'])
                df = df[df['price_per_night'] >= min_price]
            
            if 'max_price' in kwargs and kwargs['max_price']:
                max_price = float(kwargs['max_price'])
                df = df[df['price_per_night'] <= max_price]
            
            if 'min_stars' in kwargs and kwargs['min_stars']:
                min_stars = int(kwargs['min_stars'])
                df = df[df['stars'] >= min_stars]
            
            if 'max_stars' in kwargs and kwargs['max_stars']:
                max_stars = int(kwargs['max_stars'])
                df = df[df['stars'] <= max_stars]
            
            if 'min_rating' in kwargs and kwargs['min_rating']:
                min_rating = float(kwargs['min_rating'])
                df = df[df['guest_rating'] >= min_rating]
            
            if 'max_rating' in kwargs and kwargs['max_rating']:
                max_rating = float(kwargs['max_rating'])
                df = df[df['guest_rating'] <= max_rating]
            
            # Sort by rating and get top 5
            df = df.sort_values('guest_rating', ascending=False).head(5)
            
            # Convert to list of dictionaries
            hotels = df.to_dict('records')
            
            return {
                'success': True,
                'total_matches': len(df),
                'hotels': hotels,
                'search_criteria': kwargs,
                'message': f"Found {len(hotels)} hotels matching your criteria"
            }
            
        except Exception as e:
            logger.error(f"Error searching hotels: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error occurred while searching hotels'
            }
    
    def get_locations(self) -> Dict[str, Any]:
        """Get all available locations"""
        try:
            locations = self.hotel_data['location'].unique().tolist()
            return {
                'success': True,
                'locations': locations,
                'count': len(locations)
            }
        except Exception as e:
            logger.error(f"Error getting locations: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_amenities(self) -> Dict[str, Any]:
        """Get all available amenities"""
        try:
            all_amenities = []
            for amenities_str in self.hotel_data['amenities']:
                amenities = amenities_str.split(',')
                all_amenities.extend([a.strip() for a in amenities])
            
            unique_amenities = list(set(all_amenities))
            return {
                'success': True,
                'amenities': unique_amenities,
                'count': len(unique_amenities)
            }
        except Exception as e:
            logger.error(f"Error getting amenities: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# MCP Server implementation
class MCPServer:
    def __init__(self):
        self.hotel_server = HotelMCPServer()
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests"""
        method = request.get('method')
        params = request.get('params', {})
        
        if method == 'searchHotels':
            result = self.hotel_server.search_hotels(**params)
            return {
                'id': request.get('id'),
                'result': result,
                'error': None
            }
        
        elif method == 'getLocations':
            result = self.hotel_server.get_locations()
            return {
                'id': request.get('id'),
                'result': result,
                'error': None
            }
        
        elif method == 'getAmenities':
            result = self.hotel_server.get_amenities()
            return {
                'id': request.get('id'),
                'result': result,
                'error': None
            }
        
        else:
            return {
                'id': request.get('id'),
                'result': None,
                'error': {
                    'code': -32601,
                    'message': f'Method {method} not found'
                }
            }

# Flask app for HTTP interface
from flask import Flask, request, jsonify

app = Flask(__name__)
mcp_server = MCPServer()

@app.route('/mcp/search', methods=['POST'])
def mcp_search():
    """MCP search endpoint"""
    try:
        data = request.json
        result = mcp_server.hotel_server.search_hotels(**data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/mcp/locations', methods=['GET'])
def mcp_locations():
    """MCP locations endpoint"""
    try:
        result = mcp_server.hotel_server.get_locations()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/mcp/amenities', methods=['GET'])
def mcp_amenities():
    """MCP amenities endpoint"""
    try:
        result = mcp_server.hotel_server.get_amenities()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/mcp/health', methods=['GET'])
def mcp_health():
    """MCP health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'MCP Hotel Server is running',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port) 