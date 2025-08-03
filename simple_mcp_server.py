#!/usr/bin/env python3
"""
Simple MCP Server for Retell - Clean and Reliable
"""
from flask import Flask, request, jsonify
import pandas as pd
import json
from datetime import datetime
import os

app = Flask(__name__)

class SimpleHotelServer:
    def __init__(self):
        self.csv_file = 'Hotel_Dataset.csv'
        self.create_sample_data_if_needed()
    
    def create_sample_data_if_needed(self):
        """Create sample hotel data if CSV doesn't exist"""
        if not os.path.exists(self.csv_file):
            # Create sample hotel data
            hotels_data = {
                'hotel_id': ['HOTEL001', 'HOTEL002', 'HOTEL003', 'HOTEL004', 'HOTEL005'],
                'name': ['Hotel A', 'Hotel B', 'Hotel C', 'Hotel D', 'Hotel E'],
                'location': ['Mumbai', 'Delhi', 'Bangalore', 'Mumbai', 'Delhi'],
                'check_in_date': ['2024-06-01', '2024-06-02', '2024-06-03', '2024-06-04', '2024-06-05'],
                'check_out_date': ['2024-06-05', '2024-06-07', '2024-06-08', '2024-06-09', '2024-06-10'],
                'stars': [4, 5, 3, 4, 5],
                'guest_rating': [4.5, 4.8, 4.2, 4.6, 4.9],
                'amenities': ['Gym,Pool,Restaurant', 'Spa,Gym,Restaurant', 'Pool,Restaurant', 'Gym,Restaurant', 'Spa,Pool,Gym'],
                'price_per_night': [5000, 8000, 3000, 6000, 9000],
                'max_adults': [2, 4, 2, 3, 4],
                'max_children': [1, 2, 1, 2, 2]
            }
            df = pd.DataFrame(hotels_data)
            df.to_csv(self.csv_file, index=False)
            print(f"Created sample data in {self.csv_file}")
    
    def load_data(self):
        """Load hotel data from CSV"""
        try:
            return pd.read_csv(self.csv_file)
        except Exception as e:
            print(f"Error loading data: {e}")
            self.create_sample_data_if_needed()
            return pd.read_csv(self.csv_file)
    
    def search_hotels(self, parameters):
        """Search hotels based on parameters"""
        try:
            df = self.load_data()
            
            # Apply filters
            if 'location' in parameters and parameters['location']:
                df = df[df['location'].str.contains(parameters['location'], case=False, na=False)]
            
            if 'adults' in parameters and parameters['adults']:
                try:
                    adults = int(parameters['adults'])
                    df = df[df['max_adults'] >= adults]
                except:
                    pass
            
            if 'children' in parameters and parameters['children']:
                try:
                    children = int(parameters['children'])
                    df = df[df['max_children'] >= children]
                except:
                    pass
            
            if 'amenities' in parameters and parameters['amenities']:
                amenities = parameters['amenities'].split(',')
                for amenity in amenities:
                    df = df[df['amenities'].str.contains(amenity.strip(), case=False, na=False)]
            
            if 'min_price' in parameters and parameters['min_price']:
                try:
                    min_price = float(parameters['min_price'])
                    df = df[df['price_per_night'] >= min_price]
                except:
                    pass
            
            if 'max_price' in parameters and parameters['max_price']:
                try:
                    max_price = float(parameters['max_price'])
                    df = df[df['price_per_night'] <= max_price]
                except:
                    pass
            
            if 'min_stars' in parameters and parameters['min_stars']:
                try:
                    min_stars = int(parameters['min_stars'])
                    df = df[df['stars'] >= min_stars]
                except:
                    pass
            
            if 'min_rating' in parameters and parameters['min_rating']:
                try:
                    min_rating = float(parameters['min_rating'])
                    df = df[df['guest_rating'] >= min_rating]
                except:
                    pass
            
            # Sort by rating and get top 5
            df = df.sort_values('guest_rating', ascending=False).head(5)
            
            # Convert to list of dictionaries
            hotels = df.to_dict('records')
            
            return {
                'total_matches': len(df),
                'hotels': hotels,
                'search_criteria': parameters,
                'message': f"Found {len(hotels)} hotels matching your criteria"
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Error occurred while searching hotels'
            }
    
    def get_locations(self):
        """Get all available locations"""
        try:
            df = self.load_data()
            locations = df['location'].unique().tolist()
            return {
                'locations': locations,
                'count': len(locations)
            }
        except Exception as e:
            return {
                'error': str(e),
                'locations': [],
                'count': 0
            }
    
    def get_amenities(self):
        """Get all available amenities"""
        try:
            df = self.load_data()
            all_amenities = []
            for amenities_str in df['amenities']:
                amenities = amenities_str.split(',')
                all_amenities.extend([a.strip() for a in amenities])
            
            unique_amenities = list(set(all_amenities))
            return {
                'amenities': unique_amenities,
                'count': len(unique_amenities)
            }
        except Exception as e:
            return {
                'error': str(e),
                'amenities': [],
                'count': 0
            }

# Initialize the server
hotel_server = SimpleHotelServer()

@app.route('/')
def home():
    """Root endpoint"""
    return jsonify({
        'message': 'Simple Hotel MCP Server',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'mcp_health': '/mcp/health',
            'mcp_tools': '/mcp/tools',
            'mcp_execute': '/mcp/execute'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Simple Hotel MCP Server is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/mcp/health')
def mcp_health():
    """MCP health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'MCP Hotel Server is running',
        'timestamp': datetime.now().isoformat(),
        'tools': ['searchHotels', 'getLocations', 'getAmenities']
    })

@app.route('/mcp/tools')
def mcp_tools():
    """MCP tool discovery endpoint"""
    return jsonify({
        "tools": [
            {
                "name": "searchHotels",
                "description": "Search for hotels based on customer preferences",
                "parameters": {
                    "location": {"type": "string", "required": True, "description": "City or location"},
                    "adults": {"type": "integer", "required": True, "description": "Number of adults"},
                    "children": {"type": "integer", "required": False, "description": "Number of children"},
                    "amenities": {"type": "string", "required": False, "description": "Preferred amenities (comma-separated)"},
                    "min_price": {"type": "number", "required": False, "description": "Minimum price per night"},
                    "max_price": {"type": "number", "required": False, "description": "Maximum price per night"},
                    "min_stars": {"type": "integer", "required": False, "description": "Minimum star rating (1-5)"},
                    "min_rating": {"type": "number", "required": False, "description": "Minimum guest rating (0.0-5.0)"}
                }
            },
            {
                "name": "getLocations",
                "description": "Get all available hotel locations",
                "parameters": {}
            },
            {
                "name": "getAmenities",
                "description": "Get all available hotel amenities",
                "parameters": {}
            }
        ]
    })

@app.route('/mcp/execute', methods=['POST'])
def mcp_execute():
    """MCP tool execution endpoint"""
    try:
        data = request.json
        tool_name = data.get('tool')
        parameters = data.get('parameters', {})
        
        if tool_name == 'searchHotels':
            result = hotel_server.search_hotels(parameters)
            return jsonify({
                'success': True,
                'result': result,
                'tool': tool_name
            })
        
        elif tool_name == 'getLocations':
            result = hotel_server.get_locations()
            return jsonify({
                'success': True,
                'result': result,
                'tool': tool_name
            })
        
        elif tool_name == 'getAmenities':
            result = hotel_server.get_amenities()
            return jsonify({
                'success': True,
                'result': result,
                'tool': tool_name
            })
        
        else:
            return jsonify({
                'success': False,
                'error': f'Unknown tool: {tool_name}'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port) 