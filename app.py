from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
api = Api(app, 
    title='Hotel API',
    version='1.0.0',
    description='A comprehensive Flask API for hotel search and filtering with OpenAPI documentation',
    doc='/docs',
    default='api',
    default_label='Hotel API Endpoints'
)

# Define namespaces
hotels_ns = api.namespace('api/hotels', description='Hotel operations')
locations_ns = api.namespace('api/locations', description='Location operations')
amenities_ns = api.namespace('api/amenities', description='Amenities operations')
stats_ns = api.namespace('api/stats', description='Statistics operations')

# Define models for Swagger documentation
hotel_model = api.model('Hotel', {
    'hotel_id': fields.String(description='Unique hotel identifier'),
    'name': fields.String(description='Hotel name'),
    'location': fields.String(description='Hotel location/city'),
    'check_in_date': fields.String(description='Available check-in date'),
    'check_out_date': fields.String(description='Available check-out date'),
    'stars': fields.Integer(description='Star rating (1-5)'),
    'guest_rating': fields.Float(description='Guest rating (0.0-5.0)'),
    'amenities': fields.String(description='Comma-separated list of amenities'),
    'price_per_night': fields.Integer(description='Price per night in local currency'),
    'max_adults': fields.Integer(description='Maximum number of adults'),
    'max_children': fields.Integer(description='Maximum number of children')
})

search_model = api.model('SearchCriteria', {
    'location': fields.String(required=True, description='Hotel location/city'),
    'check_in_date': fields.String(required=True, description='Check-in date (YYYY-MM-DD)'),
    'check_out_date': fields.String(required=True, description='Check-out date (YYYY-MM-DD)'),
    'adults': fields.Integer(required=True, description='Number of adults'),
    'children': fields.Integer(description='Number of children'),
    'amenities': fields.String(description='Comma-separated amenities'),
    'min_price': fields.Float(description='Minimum price per night'),
    'max_price': fields.Float(description='Maximum price per night'),
    'min_stars': fields.Integer(description='Minimum star rating (1-5)'),
    'max_stars': fields.Integer(description='Maximum star rating (1-5)'),
    'min_rating': fields.Float(description='Minimum guest rating (0.0-5.0)'),
    'max_rating': fields.Float(description='Maximum guest rating (0.0-5.0)')
})

search_response_model = api.model('SearchResponse', {
    'search_results': fields.Nested(api.model('SearchResults', {
        'total_matches': fields.Integer(description='Total number of matching hotels'),
        'top_5_hotels': fields.List(fields.Nested(hotel_model), description='Top 5 hotels by rating'),
        'price_range': fields.Nested(api.model('PriceRange', {
            'min': fields.Integer(description='Minimum price'),
            'max': fields.Integer(description='Maximum price')
        })),
        'average_rating': fields.Float(description='Average rating of matching hotels')
    })),
    'search_criteria': fields.Nested(search_model),
    'message': fields.String(description='Search result message')
})

hotels_response_model = api.model('HotelsResponse', {
    'hotels': fields.List(fields.Nested(hotel_model)),
    'total_count': fields.Integer(description='Total number of hotels'),
    'filters_applied': fields.Raw(description='Applied filters'),
    'sorting': fields.String(description='Sorting information')
})

stats_model = api.model('Stats', {
    'total_hotels': fields.Integer(description='Total number of hotels'),
    'average_price': fields.Float(description='Average price per night'),
    'average_rating': fields.Float(description='Average guest rating'),
    'price_range': fields.Nested(api.model('PriceRange', {
        'min': fields.Integer(description='Minimum price'),
        'max': fields.Integer(description='Maximum price')
    })),
    'rating_range': fields.Nested(api.model('RatingRange', {
        'min': fields.Float(description='Minimum rating'),
        'max': fields.Float(description='Maximum rating')
    })),
    'stars_distribution': fields.Raw(description='Distribution of star ratings'),
    'locations_count': fields.Integer(description='Number of unique locations')
})

# Load hotel data from CSV file
def load_hotel_data():
    """Load hotel data from CSV file"""
    csv_file = 'Hotel_Dataset.csv'
    if not os.path.exists(csv_file):
        # Create sample data if file doesn't exist
        create_sample_data()
    
    try:
        df = pd.read_csv(csv_file)
        # Convert date columns to datetime if they exist
        if 'check_in_date' in df.columns:
            df['check_in_date'] = pd.to_datetime(df['check_in_date'])
        if 'check_out_date' in df.columns:
            df['check_out_date'] = pd.to_datetime(df['check_out_date'])
        return df
    except Exception as e:
        print(f"Error loading hotel data: {e}")
        return pd.DataFrame()

def create_sample_data():
    """Create sample hotel data CSV file"""
    sample_data = {
        'hotel_id': range(1, 21),
        'hotel_name': [
            'Grand Hotel & Spa', 'Seaside Resort', 'Mountain View Lodge', 'City Center Hotel',
            'Beachfront Paradise', 'Historic Inn', 'Business Plaza Hotel', 'Garden Retreat',
            'Luxury Tower', 'Cozy Cottage Inn', 'Riverside Hotel', 'Airport Express',
            'Downtown Suites', 'Countryside Manor', 'Ocean View Resort', 'Urban Boutique',
            'Family Resort', 'Executive Hotel', 'Holiday Inn Express', 'Premium Lodge'
        ],
        'location': [
            'New York', 'Miami', 'Denver', 'Chicago', 'Los Angeles', 'Boston', 'Atlanta',
            'Seattle', 'Las Vegas', 'Portland', 'Austin', 'Phoenix', 'Dallas', 'Nashville',
            'San Diego', 'San Francisco', 'Orlando', 'Houston', 'Philadelphia', 'Detroit'
        ],
        'check_in_date': [
            '2024-01-15', '2024-01-20', '2024-02-01', '2024-02-10', '2024-02-15',
            '2024-03-01', '2024-03-10', '2024-03-20', '2024-04-01', '2024-04-10',
            '2024-04-20', '2024-05-01', '2024-05-10', '2024-05-20', '2024-06-01',
            '2024-06-10', '2024-06-20', '2024-07-01', '2024-07-10', '2024-07-20'
        ],
        'check_out_date': [
            '2024-01-18', '2024-01-23', '2024-02-04', '2024-02-13', '2024-02-18',
            '2024-03-04', '2024-03-13', '2024-03-23', '2024-04-04', '2024-04-13',
            '2024-04-23', '2024-05-04', '2024-05-13', '2024-05-23', '2024-06-04',
            '2024-06-13', '2024-06-23', '2024-07-04', '2024-07-13', '2024-07-23'
        ],
        'stars': [4, 5, 3, 4, 5, 3, 4, 4, 5, 3, 4, 3, 4, 4, 5, 4, 4, 5, 3, 4],
        'guest_rating': [4.2, 4.8, 3.9, 4.1, 4.7, 3.8, 4.3, 4.0, 4.9, 3.7, 4.2, 3.6, 4.4, 4.1, 4.6, 4.3, 4.5, 4.8, 3.9, 4.2],
        'amenities': [
            'WiFi,Pool,Gym,Spa', 'WiFi,Pool,Beach,Gym', 'WiFi,Gym,Restaurant', 'WiFi,Business Center,Gym',
            'WiFi,Pool,Beach,Spa', 'WiFi,Restaurant,Bar', 'WiFi,Business Center,Restaurant', 'WiFi,Garden,Restaurant',
            'WiFi,Pool,Gym,Spa,Restaurant', 'WiFi,Restaurant', 'WiFi,Pool,Restaurant', 'WiFi,Shuttle',
            'WiFi,Business Center,Restaurant', 'WiFi,Garden,Pool', 'WiFi,Pool,Beach,Gym', 'WiFi,Restaurant,Bar',
            'WiFi,Pool,Kids Club,Gym', 'WiFi,Business Center,Gym,Spa', 'WiFi,Breakfast', 'WiFi,Gym,Restaurant'
        ],
        'price_per_night': [150, 300, 120, 180, 250, 100, 160, 140, 400, 90, 130, 110, 170, 125, 280, 200, 220, 350, 95, 135],
        'max_adults': [2, 4, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 4, 2, 2, 2],
        'max_children': [2, 3, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 3, 1, 1, 1]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('Hotel_Dataset.csv', index=False)
    print("Sample hotel data created successfully as Hotel_Dataset.csv!")

@hotels_ns.route('/', methods=['GET'])
class GetHotels(Resource):
    """Get all hotels with optional filtering"""
    @hotels_ns.doc('get_hotels', model=hotels_response_model)
    def get(self):
        """Get all hotels with optional filtering"""
        try:
            # Load hotel data
            df = load_hotel_data()
            
            if df.empty:
                return jsonify({'error': 'No hotel data available'}), 500
            
            # Get filter parameters
            location = request.args.get('location')
            check_in_date = request.args.get('check_in_date')
            check_out_date = request.args.get('check_out_date')
            min_stars = request.args.get('min_stars', type=int)
            max_stars = request.args.get('max_stars', type=int)
            min_rating = request.args.get('min_rating', type=float)
            max_rating = request.args.get('max_rating', type=float)
            amenities = request.args.get('amenities')
            min_price = request.args.get('min_price', type=float)
            max_price = request.args.get('max_price', type=float)
            adults = request.args.get('adults', type=int)
            children = request.args.get('children', type=int)
            
            # Apply filters
            if location:
                df = df[df['location'].str.contains(location, case=False, na=False)]
            
            if check_in_date:
                try:
                    check_in = pd.to_datetime(check_in_date)
                    df = df[df['check_in_date'] >= check_in]
                except:
                    pass
            
            if check_out_date:
                try:
                    check_out = pd.to_datetime(check_out_date)
                    df = df[df['check_out_date'] <= check_out]
                except:
                    pass
            
            if min_stars is not None:
                df = df[df['stars'] >= min_stars]
            
            if max_stars is not None:
                df = df[df['stars'] <= max_stars]
            
            if min_rating is not None:
                df = df[df['guest_rating'] >= min_rating]
            
            if max_rating is not None:
                df = df[df['guest_rating'] <= max_rating]
            
            if amenities:
                amenity_list = [amenity.strip() for amenity in amenities.split(',')]
                for amenity in amenity_list:
                    df = df[df['amenities'].str.contains(amenity, case=False, na=False)]
            
            if min_price is not None:
                df = df[df['price_per_night'] >= min_price]
            
            if max_price is not None:
                df = df[df['price_per_night'] <= max_price]
            
            if adults is not None:
                df = df[df['max_adults'] >= adults]
            
            if children is not None:
                df = df[df['max_children'] >= children]
            
            # Sort by guest rating in descending order
            df = df.sort_values('guest_rating', ascending=False)
            
            # Convert to list of dictionaries
            hotels = df.to_dict('records')
            
            return jsonify({
                'hotels': hotels,
                'total_count': len(hotels),
                'filters_applied': {
                    'location': location,
                    'check_in_date': check_in_date,
                    'check_out_date': check_out_date,
                    'min_stars': min_stars,
                    'max_stars': max_stars,
                    'min_rating': min_rating,
                    'max_rating': max_rating,
                    'amenities': amenities,
                    'min_price': min_price,
                    'max_price': max_price,
                    'adults': adults,
                    'children': children
                },
                'sorting': 'guest_rating_desc'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@hotels_ns.route('/<int:hotel_id>', methods=['GET'])
class GetHotel(Resource):
    """Get a specific hotel by ID"""
    @hotels_ns.doc('get_hotel', model=hotel_model)
    def get(self, hotel_id):
        """Get a specific hotel by ID"""
        try:
            df = load_hotel_data()
            
            if df.empty:
                return jsonify({'error': 'No hotel data available'}), 500
            
            hotel = df[df['hotel_id'] == hotel_id]
            
            if hotel.empty:
                return jsonify({'error': 'Hotel not found'}), 404
            
            return jsonify(hotel.iloc[0].to_dict())
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@hotels_ns.route('/advanced', methods=['GET'])
class GetHotelsAdvanced(Resource):
    """Get hotels with advanced filtering and sorting options"""
    @hotels_ns.doc('get_hotels_advanced', model=hotels_response_model)
    def get(self):
        """Get hotels with advanced filtering and sorting options"""
        try:
            # Load hotel data
            df = load_hotel_data()
            
            if df.empty:
                return jsonify({'error': 'No hotel data available'}), 500
            
            # Get filter parameters
            location = request.args.get('location')
            check_in_date = request.args.get('check_in_date')
            check_out_date = request.args.get('check_out_date')
            min_stars = request.args.get('min_stars', type=int)
            max_stars = request.args.get('max_stars', type=int)
            min_rating = request.args.get('min_rating', type=float)
            max_rating = request.args.get('max_rating', type=float)
            amenities = request.args.get('amenities')
            min_price = request.args.get('min_price', type=float)
            max_price = request.args.get('max_price', type=float)
            adults = request.args.get('adults', type=int)
            children = request.args.get('children', type=int)
            
            # Get sorting parameters
            sort_by = request.args.get('sort_by', 'guest_rating')  # Default sort by guest rating
            sort_order = request.args.get('sort_order', 'desc')  # Default descending order
            
            # Validate sort_by parameter
            valid_sort_fields = ['hotel_id', 'hotel_name', 'location', 'check_in_date', 'check_out_date', 
                               'stars', 'guest_rating', 'price_per_night', 'max_adults', 'max_children']
            if sort_by not in valid_sort_fields:
                sort_by = 'guest_rating'
            
            # Validate sort_order parameter
            if sort_order not in ['asc', 'desc']:
                sort_order = 'desc'
            
            # Apply filters
            if location:
                df = df[df['location'].str.contains(location, case=False, na=False)]
            
            if check_in_date:
                try:
                    check_in = pd.to_datetime(check_in_date)
                    df = df[df['check_in_date'] >= check_in]
                except:
                    pass
            
            if check_out_date:
                try:
                    check_out = pd.to_datetime(check_out_date)
                    df = df[df['check_out_date'] <= check_out]
                except:
                    pass
            
            if min_stars is not None:
                df = df[df['stars'] >= min_stars]
            
            if max_stars is not None:
                df = df[df['stars'] <= max_stars]
            
            if min_rating is not None:
                df = df[df['guest_rating'] >= min_rating]
            
            if max_rating is not None:
                df = df[df['guest_rating'] <= max_rating]
            
            if amenities:
                amenity_list = [amenity.strip() for amenity in amenities.split(',')]
                for amenity in amenity_list:
                    df = df[df['amenities'].str.contains(amenity, case=False, na=False)]
            
            if min_price is not None:
                df = df[df['price_per_night'] >= min_price]
            
            if max_price is not None:
                df = df[df['price_per_night'] <= max_price]
            
            if adults is not None:
                df = df[df['max_adults'] >= adults]
            
            if children is not None:
                df = df[df['max_children'] >= children]
            
            # Sort by specified field and order
            ascending = sort_order == 'asc'
            df = df.sort_values(sort_by, ascending=ascending)
            
            # Convert to list of dictionaries
            hotels = df.to_dict('records')
            
            return jsonify({
                'hotels': hotels,
                'total_count': len(hotels),
                'filters_applied': {
                    'location': location,
                    'check_in_date': check_in_date,
                    'check_out_date': check_out_date,
                    'min_stars': min_stars,
                    'max_stars': max_stars,
                    'min_rating': min_rating,
                    'max_rating': max_rating,
                    'amenities': amenities,
                    'min_price': min_price,
                    'max_price': max_price,
                    'adults': adults,
                    'children': children
                },
                'sorting': {
                    'field': sort_by,
                    'order': sort_order
                }
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@hotels_ns.route('/search', methods=['GET'])
class SearchHotels(Resource):
    """Comprehensive hotel search with all parameters and top 5 results by rating"""
    @hotels_ns.doc('search_hotels', model=search_response_model)
    def get(self):
        """Comprehensive hotel search with all parameters and top 5 results by rating"""
        try:
            # Load hotel data
            df = load_hotel_data()
            
            if df.empty:
                return jsonify({'error': 'No hotel data available'}), 500
            
            # Required parameters (primary filters)
            location = request.args.get('location')
            check_in_date = request.args.get('check_in_date')
            check_out_date = request.args.get('check_out_date')
            adults = request.args.get('adults', type=int)
            children = request.args.get('children', type=int)
            
            # Optional parameters (preferences)
            amenities = request.args.get('amenities')
            min_price = request.args.get('min_price', type=float)
            max_price = request.args.get('max_price', type=float)
            min_stars = request.args.get('min_stars', type=int)
            max_stars = request.args.get('max_stars', type=int)
            min_rating = request.args.get('min_rating', type=float)
            max_rating = request.args.get('max_rating', type=float)
            
            # Validate required parameters
            if not location:
                return jsonify({'error': 'Location is required'}), 400
            
            if not check_in_date:
                return jsonify({'error': 'Check-in date is required'}), 400
            
            if not check_out_date:
                return jsonify({'error': 'Check-out date is required'}), 400
            
            if adults is None:
                return jsonify({'error': 'Number of adults is required'}), 400
            
            # Apply primary filters (required)
            df = df[df['location'].str.contains(location, case=False, na=False)]
            
            try:
                check_in = pd.to_datetime(check_in_date)
                df = df[df['check_in_date'] >= check_in]
            except:
                return jsonify({'error': 'Invalid check-in date format. Use YYYY-MM-DD'}), 400
            
            try:
                check_out = pd.to_datetime(check_out_date)
                df = df[df['check_out_date'] <= check_out]
            except:
                return jsonify({'error': 'Invalid check-out date format. Use YYYY-MM-DD'}), 400
            
            if adults is not None:
                df = df[df['max_adults'] >= adults]
            
            if children is not None:
                df = df[df['max_children'] >= children]
            
            # Apply preference filters (optional)
            if amenities:
                amenity_list = [amenity.strip() for amenity in amenities.split(',')]
                for amenity in amenity_list:
                    df = df[df['amenities'].str.contains(amenity, case=False, na=False)]
            
            if min_price is not None:
                df = df[df['price_per_night'] >= min_price]
            
            if max_price is not None:
                df = df[df['price_per_night'] <= max_price]
            
            if min_stars is not None:
                df = df[df['stars'] >= min_stars]
            
            if max_stars is not None:
                df = df[df['stars'] <= max_stars]
            
            if min_rating is not None:
                df = df[df['guest_rating'] >= min_rating]
            
            if max_rating is not None:
                df = df[df['guest_rating'] <= max_rating]
            
            # Sort by guest rating in descending order and get top 5
            df = df.sort_values('guest_rating', ascending=False)
            top_5_hotels = df.head(5)
            
            # Convert to list of dictionaries
            hotels = top_5_hotels.to_dict('records')
            
            # Calculate search summary
            total_matches = len(df)
            price_range = {
                'min': int(df['price_per_night'].min()) if not df.empty else 0,
                'max': int(df['price_per_night'].max()) if not df.empty else 0
            } if not df.empty else {'min': 0, 'max': 0}
            
            return jsonify({
                'search_results': {
                    'total_matches': total_matches,
                    'top_5_hotels': hotels,
                    'price_range': price_range,
                    'average_rating': round(df['guest_rating'].mean(), 2) if not df.empty else 0
                },
                'search_criteria': {
                    'location': location,
                    'check_in_date': check_in_date,
                    'check_out_date': check_out_date,
                    'adults': adults,
                    'children': children,
                    'amenities': amenities,
                    'min_price': min_price,
                    'max_price': max_price,
                    'min_stars': min_stars,
                    'max_stars': max_stars,
                    'min_rating': min_rating,
                    'max_rating': max_rating
                },
                'message': f"Found {total_matches} hotels matching your criteria. Showing top 5 by rating."
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@locations_ns.route('/', methods=['GET'])
class GetLocations(Resource):
    """Get all available locations"""
    @locations_ns.doc('get_locations')
    def get(self):
        """Get all available locations"""
        try:
            df = load_hotel_data()
            
            if df.empty:
                return jsonify({'error': 'No hotel data available'}), 500
            
            locations = df['location'].unique().tolist()
            return jsonify({'locations': sorted(locations)})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@amenities_ns.route('/', methods=['GET'])
class GetAmenities(Resource):
    """Get all available amenities"""
    @amenities_ns.doc('get_amenities')
    def get(self):
        """Get all available amenities"""
        try:
            df = load_hotel_data()
            
            if df.empty:
                return jsonify({'error': 'No hotel data available'}), 500
            
            # Extract all unique amenities
            all_amenities = set()
            for amenities_str in df['amenities']:
                if pd.notna(amenities_str):
                    amenities_list = [amenity.strip() for amenity in amenities_str.split(',')]
                    all_amenities.update(amenities_list)
            
            return jsonify({'amenities': sorted(list(all_amenities))})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@stats_ns.route('/', methods=['GET'])
class GetStats(Resource):
    """Get hotel statistics"""
    @stats_ns.doc('get_stats', model=stats_model)
    def get(self):
        """Get hotel statistics"""
        try:
            df = load_hotel_data()
            
            if df.empty:
                return jsonify({'error': 'No hotel data available'}), 500
            
            stats = {
                'total_hotels': len(df),
                'average_price': round(df['price_per_night'].mean(), 2),
                'average_rating': round(df['guest_rating'].mean(), 2),
                'price_range': {
                    'min': int(df['price_per_night'].min()),
                    'max': int(df['price_per_night'].max())
                },
                'rating_range': {
                    'min': round(df['guest_rating'].min(), 1),
                    'max': round(df['guest_rating'].max(), 1)
                },
                'stars_distribution': df['stars'].value_counts().to_dict(),
                'locations_count': len(df['location'].unique())
            }
            
            return jsonify(stats)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@api.route('/health', methods=['GET'])
class HealthCheck(Resource):
    """Simple health check endpoint"""
    @api.doc('health_check')
    def get(self):
        """Simple health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'Hotel API is running',
            'timestamp': datetime.now().isoformat()
        })

@api.route('/test')
class TestEndpoint(Resource):
    """Test endpoint for Retell verification"""
    @api.doc('test_endpoint')
    def get(self):
        """Test endpoint for Retell verification"""
        return jsonify({
            'status': 'success',
            'message': 'API is working correctly',
            'timestamp': datetime.now().isoformat(),
            'endpoints': {
                'search': '/api/hotels/search',
                'locations': '/api/locations',
                'amenities': '/api/amenities',
                'openapi': '/openapi.json'
            }
        })

@api.route('/')
class Home(Resource):
    """API documentation"""
    @api.doc('home')
    def get(self):
        """API documentation"""
        return jsonify({
            'message': 'Hotel API',
            'version': '1.0.0',
            'endpoints': {
                'GET /api/hotels': 'Get all hotels with optional filtering (sorted by guest rating desc)',
                'GET /api/hotels/advanced': 'Get hotels with advanced filtering and custom sorting options',
                'GET /api/hotels/search': 'Comprehensive search with all parameters - returns top 5 by rating',
                'GET /api/hotels/<id>': 'Get a specific hotel by ID',
                'GET /api/locations': 'Get all available locations',
                'GET /api/amenities': 'Get all available amenities',
                'GET /api/stats': 'Get hotel statistics',
                'GET /health': 'Health check endpoint'
            },
            'filter_parameters': {
                'location': 'Filter by location (string)',
                'check_in_date': 'Filter by check-in date (YYYY-MM-DD)',
                'check_out_date': 'Filter by check-out date (YYYY-MM-DD)',
                'min_stars': 'Minimum star rating (integer)',
                'max_stars': 'Maximum star rating (integer)',
                'min_rating': 'Minimum guest rating (float)',
                'max_rating': 'Maximum guest rating (float)',
                'amenities': 'Filter by amenities (comma-separated)',
                'min_price': 'Minimum price per night (float)',
                'max_price': 'Maximum price per night (float)',
                'adults': 'Number of adults (integer)',
                'children': 'Number of children (integer)'
            },
            'advanced_sorting_parameters': {
                'sort_by': 'Sort by field (hotel_id, hotel_name, location, check_in_date, check_out_date, stars, guest_rating, price_per_night, max_adults, max_children)',
                'sort_order': 'Sort order (asc or desc)'
            },
            'search_endpoint_parameters': {
                'required': ['location', 'check_in_date', 'check_out_date', 'adults'],
                'optional': ['children', 'amenities', 'min_price', 'max_price', 'min_stars', 'max_stars', 'min_rating', 'max_rating']
            },
            'examples': {
                'basic_filtering': '/api/hotels?location=New York&min_stars=4&max_price=200&adults=2',
                'advanced_filtering': '/api/hotels/advanced?location=Mumbai&amenities=Pool,Beach&sort_by=price_per_night&sort_order=asc',
                'comprehensive_search': '/api/hotels/search?location=Mumbai&check_in_date=2024-06-01&check_out_date=2024-06-05&adults=2&children=1&amenities=Gym,Pool&max_price=5000&min_stars=4',
                'rating_filter': '/api/hotels?min_rating=4.5&max_price=300',
                'date_filter': '/api/hotels?check_in_date=2024-06-01&check_out_date=2024-06-05'
            }
        })

@app.route('/openapi.json')
def openapi_spec():
    """Return OpenAPI specification for Retell"""
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "Hotel Search API",
            "version": "1.0.0",
            "description": "Simple API for searching hotels"
        },
        "servers": [
            {
                "url": "https://hotel-api-flask-production.up.railway.app"
            }
        ],
        "paths": {
            "/api/hotels/search": {
                "get": {
                    "operationId": "searchHotels",
                    "summary": "Search hotels",
                    "parameters": [
                        {
                            "name": "location",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "check_in_date",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "check_out_date",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "adults",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "integer"}
                        },
                        {
                            "name": "children",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer"}
                        },
                        {
                            "name": "amenities",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "string"}
                        },
                        {
                            "name": "min_price",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "number"}
                        },
                        {
                            "name": "max_price",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "number"}
                        },
                        {
                            "name": "min_stars",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer"}
                        },
                        {
                            "name": "max_stars",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "integer"}
                        },
                        {
                            "name": "min_rating",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "number"}
                        },
                        {
                            "name": "max_rating",
                            "in": "query",
                            "required": False,
                            "schema": {"type": "number"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "search_results": {
                                                "type": "object",
                                                "properties": {
                                                    "total_matches": {"type": "integer"},
                                                    "top_5_hotels": {
                                                        "type": "array",
                                                        "items": {"$ref": "#/components/schemas/Hotel"}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Bad request"
                        }
                    }
                }
            },
            "/api/locations": {
                "get": {
                    "operationId": "getLocations",
                    "summary": "Get locations",
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "locations": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/amenities": {
                "get": {
                    "operationId": "getAmenities",
                    "summary": "Get amenities",
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "amenities": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "Hotel": {
                    "type": "object",
                    "properties": {
                        "hotel_id": {"type": "string"},
                        "name": {"type": "string"},
                        "location": {"type": "string"},
                        "stars": {"type": "integer"},
                        "guest_rating": {"type": "number"},
                        "price_per_night": {"type": "integer"}
                    }
                }
            }
        }
    })

@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Hotel API is running',
        'version': '1.0.0',
        'endpoints': {
            'search': '/api/hotels/search',
            'locations': '/api/locations',
            'amenities': '/api/amenities',
            'openapi': '/openapi.json'
        }
    })

@app.route('/mcp/tools', methods=['GET'])
def mcp_tools():
    """MCP tool discovery endpoint for Retell"""
    return jsonify({
        "tools": [
            {
                "name": "searchHotels",
                "description": "Search for hotels based on customer preferences",
                "parameters": {
                    "location": {"type": "string", "required": True, "description": "City or location"},
                    "check_in_date": {"type": "string", "required": True, "description": "Check-in date (YYYY-MM-DD)"},
                    "check_out_date": {"type": "string", "required": True, "description": "Check-out date (YYYY-MM-DD)"},
                    "adults": {"type": "integer", "required": True, "description": "Number of adults"},
                    "children": {"type": "integer", "required": False, "description": "Number of children"},
                    "amenities": {"type": "string", "required": False, "description": "Preferred amenities (comma-separated)"},
                    "min_price": {"type": "number", "required": False, "description": "Minimum price per night"},
                    "max_price": {"type": "number", "required": False, "description": "Maximum price per night"},
                    "min_stars": {"type": "integer", "required": False, "description": "Minimum star rating (1-5)"},
                    "max_stars": {"type": "integer", "required": False, "description": "Maximum star rating (1-5)"},
                    "min_rating": {"type": "number", "required": False, "description": "Minimum guest rating (0.0-5.0)"},
                    "max_rating": {"type": "number", "required": False, "description": "Maximum guest rating (0.0-5.0)"}
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
    """MCP tool execution endpoint for Retell"""
    try:
        data = request.json
        tool_name = data.get('tool')
        parameters = data.get('parameters', {})
        
        if tool_name == 'searchHotels':
            # Use the existing search endpoint logic
            result = search_hotels_logic(parameters)
            return jsonify({
                'success': True,
                'result': result,
                'tool': tool_name
            })
        
        elif tool_name == 'getLocations':
            df = load_hotel_data()
            locations = df['location'].unique().tolist()
            return jsonify({
                'success': True,
                'result': {
                    'locations': locations,
                    'count': len(locations)
                },
                'tool': tool_name
            })
        
        elif tool_name == 'getAmenities':
            df = load_hotel_data()
            all_amenities = []
            for amenities_str in df['amenities']:
                amenities = amenities_str.split(',')
                all_amenities.extend([a.strip() for a in amenities])
            
            unique_amenities = list(set(all_amenities))
            return jsonify({
                'success': True,
                'result': {
                    'amenities': unique_amenities,
                    'count': len(unique_amenities)
                },
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

def search_hotels_logic(parameters):
    """Logic for searching hotels (extracted from existing search endpoint)"""
    try:
        df = load_hotel_data()
        
        # Apply filters
        if 'location' in parameters and parameters['location']:
            df = df[df['location'].str.contains(parameters['location'], case=False, na=False)]
        
        if 'check_in_date' in parameters and parameters['check_in_date']:
            check_in = pd.to_datetime(parameters['check_in_date'])
            df = df[df['check_in_date'] >= check_in]
        
        if 'check_out_date' in parameters and parameters['check_out_date']:
            check_out = pd.to_datetime(parameters['check_out_date'])
            df = df[df['check_out_date'] <= check_out]
        
        if 'adults' in parameters and parameters['adults']:
            adults = int(parameters['adults'])
            df = df[df['max_adults'] >= adults]
        
        if 'children' in parameters and parameters['children']:
            children = int(parameters['children'])
            df = df[df['max_children'] >= children]
        
        if 'amenities' in parameters and parameters['amenities']:
            amenities = parameters['amenities'].split(',')
            for amenity in amenities:
                df = df[df['amenities'].str.contains(amenity.strip(), case=False, na=False)]
        
        if 'min_price' in parameters and parameters['min_price']:
            min_price = float(parameters['min_price'])
            df = df[df['price_per_night'] >= min_price]
        
        if 'max_price' in parameters and parameters['max_price']:
            max_price = float(parameters['max_price'])
            df = df[df['price_per_night'] <= max_price]
        
        if 'min_stars' in parameters and parameters['min_stars']:
            min_stars = int(parameters['min_stars'])
            df = df[df['stars'] >= min_stars]
        
        if 'max_stars' in parameters and parameters['max_stars']:
            max_stars = int(parameters['max_stars'])
            df = df[df['stars'] <= max_stars]
        
        if 'min_rating' in parameters and parameters['min_rating']:
            min_rating = float(parameters['min_rating'])
            df = df[df['guest_rating'] >= min_rating]
        
        if 'max_rating' in parameters and parameters['max_rating']:
            max_rating = float(parameters['max_rating'])
            df = df[df['guest_rating'] <= max_rating]
        
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port) 