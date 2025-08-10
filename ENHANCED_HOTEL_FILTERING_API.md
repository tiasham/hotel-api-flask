# Enhanced Hotel Filtering System API Documentation

## Overview

The Enhanced Hotel Filtering System provides comprehensive hotel search and filtering capabilities directly from the `Hotel_Dataset.csv` file. It integrates seamlessly with the Voice Agent Webhook System to provide intelligent hotel recommendations based on user preferences.

## Base URL

```
http://localhost:5004/webhook
```

## Authentication

Currently, no authentication is required. All endpoints are publicly accessible.

## Endpoints

### 1. Health Check

**GET** `/webhook/health`

Returns system health status and hotel dataset information.

**Response:**
```json
{
  "status": "healthy",
  "active_conversations": 2,
  "hotel_dataset_loaded": true,
  "hotel_stats": {
    "total_hotels": 100,
    "locations": 15,
    "price_range": {
      "min": 2308.0,
      "max": 9748.0
    },
    "star_ratings": {
      "3": 45,
      "4": 35,
      "5": 20
    },
    "avg_rating": 4.2
  },
  "livekit_configured": true,
  "endpoints": {
    "hotel_search": "/webhook/hotels/search",
    "advanced_search": "/webhook/hotels/search/advanced",
    "locations": "/webhook/hotels/locations",
    "amenities": "/webhook/hotels/amenities",
    "price_range": "/webhook/hotels/price-range",
    "stats": "/webhook/hotels/stats"
  }
}
```

### 2. Available Locations

**GET** `/webhook/hotels/locations`

Returns all available locations in the hotel dataset.

**Response:**
```json
{
  "success": true,
  "locations": [
    "Bangalore",
    "Chennai", 
    "Delhi",
    "Goa",
    "Hyderabad",
    "Jaipur",
    "Kolkata",
    "Mumbai",
    "Pune",
    "Udaipur"
  ],
  "count": 10
}
```

### 3. Available Amenities

**GET** `/webhook/hotels/amenities`

Returns all available amenities in the hotel dataset.

**Response:**
```json
{
  "success": true,
  "amenities": [
    "24-hour security",
    "Air conditioning",
    "Airport shuttle service",
    "Baby Sitting / Child Services",
    "Business center",
    "Children's play area",
    "Game room",
    "Gym",
    "Parking",
    "Power back up",
    "Restaurant",
    "Room service"
  ],
  "count": 12
}
```

### 4. Price Range

**GET** `/webhook/hotels/price-range`

Returns the price range available in the hotel dataset.

**Response:**
```json
{
  "success": true,
  "price_range": {
    "min": 2308.0,
    "max": 9748.0
  }
}
```

### 5. Hotel Statistics

**GET** `/webhook/hotels/stats`

Returns comprehensive statistics about the hotel dataset.

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_hotels": 100,
    "locations": 10,
    "star_ratings": {
      "3": 45,
      "4": 35,
      "5": 20
    },
    "price_stats": {
      "min": 2308.0,
      "max": 9748.0,
      "mean": 6028.0,
      "median": 5800.0
    },
    "rating_stats": {
      "min": 3.0,
      "max": 5.0,
      "mean": 4.2,
      "median": 4.0
    },
    "capacity_stats": {
      "max_adults": 4,
      "max_children": 2
    }
  }
}
```

### 6. Hotel Search (Session-based)

**POST** `/webhook/hotels/search`

Searches for hotels based on the current conversation state.

**Request Body:**
```json
{
  "session_id": "session_abc123"
}
```

**Response:**
```json
{
  "success": true,
  "hotels": [
    {
      "hotel_id": "HOTEL001",
      "name": "Hotel A1",
      "stars": 3,
      "price_per_night": 8939,
      "guest_rating": 5.0,
      "location": "Delhi",
      "amenities": "['Baby Sitting / Child Services', 'Airport shuttle service', 'Power back up', 'Room service']",
      "check_in": "22-Oct-2025",
      "check_out": "24-Oct-2025",
      "guests_adults": 4,
      "guests_children": 1,
      "total_price": 8939,
      "amenities_list": ["Baby Sitting / Child Services", "Airport shuttle service", "Power back up", "Room service"],
      "rating_category": "Excellent",
      "price_category": "Premium"
    }
  ],
  "count": 1
}
```

### 7. Advanced Hotel Search

**POST** `/webhook/hotels/search/advanced`

Searches for hotels with direct filter parameters.

**Request Body:**
```json
{
  "location": "Delhi",
  "check_in_date": "2024-12-15",
  "check_out_date": "2024-12-18",
  "adults": 2,
  "children": 1,
  "rooms": 1,
  "guests_per_room": 3,
  "amenities": "WiFi, AC",
  "min_price": 3000,
  "max_price": 8000,
  "min_stars": 4,
  "max_stars": 5,
  "min_rating": 4.0,
  "max_rating": 5.0
}
```

**All Available Filters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `location` | string | City or area name | "Delhi", "Mumbai" |
| `check_in_date` | string | Check-in date (YYYY-MM-DD) | "2024-12-15" |
| `check_out_date` | string | Check-out date (YYYY-MM-DD) | "2024-12-18" |
| `adults` | integer | Number of adults | 2 |
| `children` | integer | Number of children | 1 |
| `rooms` | integer | Number of rooms needed | 1 |
| `guests_per_room` | integer | Guests per room | 3 |
| `amenities` | string | Comma-separated amenities | "WiFi, AC, Pool" |
| `min_price` | float | Minimum price per night | 3000.0 |
| `max_price` | float | Maximum price per night | 8000.0 |
| `min_stars` | integer | Minimum star rating | 4 |
| `max_stars` | integer | Maximum star rating | 5 |
| `min_rating` | float | Minimum guest rating | 4.0 |
| `max_rating` | float | Maximum guest rating | 5.0 |

**Response:**
```json
{
  "success": true,
  "hotels": [...],
  "count": 5,
  "filters_applied": {
    "location": "Delhi",
    "min_stars": 4,
    "max_price": 8000
  }
}
```

## Hotel Data Structure

Each hotel object contains the following fields:

### Core Fields
- `hotel_id`: Unique hotel identifier
- `name`: Hotel name
- `stars`: Star rating (3, 4, or 5)
- `price_per_night`: Price per night in rupees
- `guest_rating`: Guest rating out of 5
- `location`: City or area
- `amenities`: List of available amenities
- `check_in`: Check-in date
- `check_out`: Check-out date
- `guests_adults`: Maximum adults capacity
- `guests_children`: Maximum children capacity

### Computed Fields
- `total_price`: Total price (same as price_per_night for single night)
- `amenities_list`: Parsed list of amenities
- `rating_category`: Rating category (Excellent, Very Good, Good, Average, Below Average)
- `price_category`: Price category (Budget, Mid-Range, Premium, Luxury)

## Filtering Logic

### Location Filter
- Case-insensitive partial matching
- Matches any part of the location name

### Capacity Filters
- Adults: Hotel must accommodate requested number of adults
- Children: Hotel must accommodate requested number of children
- Room capacity: Calculated as rooms × guests_per_room

### Amenities Filter
- Case-insensitive partial matching
- Multiple amenities can be specified (comma-separated)
- All specified amenities must be available

### Price Filters
- Min price: Hotel price must be >= specified value
- Max price: Hotel price must be <= specified value

### Star Rating Filters
- Min stars: Hotel must have >= specified stars
- Max stars: Hotel must have <= specified stars

### Guest Rating Filters
- Min rating: Hotel must have >= specified rating
- Max rating: Hotel must have <= specified rating

### Date Availability Filter
- Checks if hotel has availability for requested dates
- Simplified availability check (in real system, would check actual availability)

## Sorting and Results

### Sorting Criteria
1. **Primary**: Guest rating (descending)
2. **Secondary**: Price per night (ascending - better deals first)

### Result Limits
- Maximum 10 hotels returned
- Results are automatically sorted by quality and value

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error description"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad request (missing required parameters)
- `404`: Resource not found
- `500`: Internal server error

## Usage Examples

### cURL Examples

#### Get Available Locations
```bash
curl -X GET "http://localhost:5004/webhook/hotels/locations"
```

#### Search Hotels in Delhi
```bash
curl -X POST "http://localhost:5004/webhook/hotels/search/advanced" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Delhi",
    "min_stars": 4,
    "max_price": 8000
  }'
```

#### Get Hotel Statistics
```bash
curl -X GET "http://localhost:5004/webhook/hotels/stats"
```

### Python Examples

#### Search Hotels with Multiple Filters
```python
import requests

url = "http://localhost:5004/webhook/hotels/search/advanced"
data = {
    "location": "Mumbai",
    "adults": 2,
    "children": 1,
    "min_stars": 4,
    "max_price": 10000,
    "amenities": "WiFi, AC"
}

response = requests.post(url, json=data)
if response.status_code == 200:
    result = response.json()
    print(f"Found {result['count']} hotels")
    for hotel in result['hotels']:
        print(f"- {hotel['name']}: {hotel['stars']}★, ₹{hotel['price_per_night']:,}/night")
```

#### Get Available Amenities
```python
import requests

response = requests.get("http://localhost:5004/webhook/hotels/amenities")
if response.status_code == 200:
    amenities = response.json()['amenities']
    print("Available amenities:", ", ".join(amenities))
```

## Integration with Voice Agent

The hotel filtering system integrates seamlessly with the voice agent:

1. **Conversation Flow**: Agent collects booking preferences through conversation
2. **Automatic Filtering**: When all criteria are collected, hotels are automatically filtered
3. **Smart Recommendations**: Top 3 hotels are presented with detailed information
4. **Enhanced Responses**: Hotel suggestions include rating categories, price categories, and amenities

## Performance Considerations

- **Dataset Loading**: Hotel dataset is loaded once at startup
- **Filtering**: All filtering is done in-memory using pandas
- **Result Limiting**: Maximum 10 results to maintain performance
- **Caching**: Conversation states are cached for efficient retrieval

## Future Enhancements

- **Real-time Availability**: Integration with actual hotel booking systems
- **Advanced Filters**: More sophisticated filtering algorithms
- **Personalization**: User preference learning and recommendations
- **Analytics**: Search pattern analysis and insights
- **Caching**: Redis-based caching for improved performance

## Troubleshooting

### Common Issues

1. **Dataset Not Loaded**
   - Check if `Hotel_Dataset.csv` exists in the project directory
   - Verify file permissions and format

2. **No Results Found**
   - Check filter parameters are not too restrictive
   - Verify location names match exactly
   - Ensure price ranges are reasonable

3. **Performance Issues**
   - Reduce result limits
   - Use more specific filters
   - Check system resources

### Debug Information

Enable debug logging to see detailed filtering information:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Support

For issues or questions about the Enhanced Hotel Filtering System:
1. Check the health endpoint for system status
2. Review error messages in the response
3. Check server logs for detailed error information
4. Verify all required dependencies are installed
