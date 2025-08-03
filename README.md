# Hotel API

A Flask-based REST API that loads hotel data from a CSV file (`Hotel_Dataset.csv`) and provides comprehensive filtering capabilities with advanced sorting options.

## Features

- Load hotel data from `Hotel_Dataset.csv` file
- **Comprehensive filtering** across all fields:
  - Location (text search)
  - Check-in and check-out dates (date range)
  - Star rating (min/max range)
  - Guest rating (min/max range)
  - Amenities (comma-separated list)
  - Price per night (min/max range)
  - Number of guests (adults and children capacity)
- **Advanced sorting** by any field in ascending or descending order
- **Default sorting** by guest rating in descending order
- Get hotel statistics
- Get available locations and amenities
- Automatic sample data generation

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the API:**
   - API will be available at `http://localhost:5001`
   - Documentation available at `http://localhost:5001/`

## API Endpoints

### 1. Get All Hotels (Basic Filtering)
```
GET /api/hotels
```
**Features:**
- All filtering options available
- **Results automatically sorted by guest rating (descending)**
- Simple and easy to use

**Query Parameters:**
- `location` - Filter by location (string, case-insensitive search)
- `check_in_date` - Filter by check-in date (YYYY-MM-DD)
- `check_out_date` - Filter by check-out date (YYYY-MM-DD)
- `min_stars` - Minimum star rating (integer, 1-5)
- `max_stars` - Maximum star rating (integer, 1-5)
- `min_rating` - Minimum guest rating (float, 0.0-5.0)
- `max_rating` - Maximum guest rating (float, 0.0-5.0)
- `amenities` - Filter by amenities (comma-separated, case-insensitive)
- `min_price` - Minimum price per night (float)
- `max_price` - Maximum price per night (float)
- `adults` - Number of adults (integer)
- `children` - Number of children (integer)

### 2. Get Hotels (Advanced Filtering & Sorting)
```
GET /api/hotels/advanced
```
**Features:**
- All filtering options from basic endpoint
- **Custom sorting** by any field
- **Flexible sort order** (ascending or descending)

**Additional Query Parameters:**
- `sort_by` - Sort by field (hotel_id, hotel_name, location, check_in_date, check_out_date, stars, guest_rating, price_per_night, max_adults, max_children)
- `sort_order` - Sort order (asc or desc)

### 3. Get Specific Hotel
```
GET /api/hotels/{hotel_id}
```

### 4. Get Available Locations
```
GET /api/locations
```

### 5. Get Available Amenities
```
GET /api/amenities
```

### 6. Get Hotel Statistics
```
GET /api/stats
```

## Sample Data

The API automatically creates sample hotel data with the following fields:
- `hotel_id` - Unique identifier
- `hotel_name` - Name of the hotel
- `location` - City/location
- `check_in_date` - Available check-in date
- `check_out_date` - Available check-out date
- `stars` - Star rating (1-5)
- `guest_rating` - Guest rating (0.0-5.0)
- `amenities` - Comma-separated list of amenities
- `price_per_night` - Price per night in USD
- `max_adults` - Maximum number of adults
- `max_children` - Maximum number of children

## Example Usage

### Basic Filtering Examples

**Get all hotels in New York with 4+ stars under $200/night (sorted by rating desc)**
```bash
curl "http://localhost:5001/api/hotels?location=New York&min_stars=4&max_price=200"
```

**Get hotels with pool and gym amenities**
```bash
curl "http://localhost:5001/api/hotels?amenities=Pool,Gym"
```

**Get hotels available for 2 adults and 1 child**
```bash
curl "http://localhost:5001/api/hotels?adults=2&children=1"
```

**Get hotels with check-in after a specific date**
```bash
curl "http://localhost:5001/api/hotels?check_in_date=2024-06-01"
```

**Get hotels with high guest ratings**
```bash
curl "http://localhost:5001/api/hotels?min_rating=4.5&max_price=300"
```

### Advanced Filtering & Sorting Examples

**Get hotels in Miami with pool and beach, sorted by price (lowest first)**
```bash
curl "http://localhost:5001/api/hotels/advanced?location=Miami&amenities=Pool,Beach&sort_by=price_per_night&sort_order=asc"
```

**Get 5-star hotels sorted by guest rating (highest first)**
```bash
curl "http://localhost:5001/api/hotels/advanced?min_stars=5&sort_by=guest_rating&sort_order=desc"
```

**Get hotels sorted by name alphabetically**
```bash
curl "http://localhost:5001/api/hotels/advanced?sort_by=hotel_name&sort_order=asc"
```

**Get hotels within date range, sorted by check-in date**
```bash
curl "http://localhost:5001/api/hotels/advanced?check_in_date=2024-06-01&check_out_date=2024-06-05&sort_by=check_in_date&sort_order=asc"
```

**Get family-friendly hotels (4+ adults, 2+ children) sorted by price**
```bash
curl "http://localhost:5001/api/hotels/advanced?adults=4&children=2&sort_by=price_per_night&sort_order=asc"
```

## Response Format

All endpoints return JSON responses. The main hotels endpoints return:

```json
{
  "hotels": [
    {
      "hotel_id": 1,
      "hotel_name": "Grand Hotel & Spa",
      "location": "New York",
      "check_in_date": "2024-01-15",
      "check_out_date": "2024-01-18",
      "stars": 4,
      "guest_rating": 4.2,
      "amenities": "WiFi,Pool,Gym,Spa",
      "price_per_night": 150,
      "max_adults": 2,
      "max_children": 2
    }
  ],
  "total_count": 1,
  "filters_applied": {
    "location": "New York",
    "min_stars": 4,
    "max_price": 200
  },
  "sorting": "guest_rating_desc"
}
```

For advanced endpoint:
```json
{
  "hotels": [...],
  "total_count": 1,
  "filters_applied": {...},
  "sorting": {
    "field": "price_per_night",
    "order": "asc"
  }
}
```

## Filtering Capabilities

### Location Filtering
- Case-insensitive text search
- Partial matches supported
- Example: "New York" will match "New York", "new york", etc.

### Date Filtering
- Check-in date: Returns hotels available from this date onwards
- Check-out date: Returns hotels available until this date
- Date format: YYYY-MM-DD

### Rating Filtering
- Star rating: 1-5 stars
- Guest rating: 0.0-5.0 (decimal values supported)
- Min/max ranges for both

### Amenities Filtering
- Comma-separated list of amenities
- Case-insensitive matching
- All specified amenities must be present
- Example: "Pool,Gym" finds hotels with both pool AND gym

### Price Filtering
- Min/max price ranges
- Numeric values only
- Currency: USD

### Guest Capacity Filtering
- Adults: Maximum number of adults the hotel can accommodate
- Children: Maximum number of children the hotel can accommodate
- Returns hotels that can accommodate the specified numbers

## Custom CSV Data

To use your own hotel data, create a `Hotel_Dataset.csv` file in the same directory with the following columns:
- hotel_id
- hotel_name
- location
- check_in_date
- check_out_date
- stars
- guest_rating
- amenities
- price_per_night
- max_adults
- max_children

The API will automatically load your custom data instead of generating sample data. 