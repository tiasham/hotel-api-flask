# Enhanced Retell-Specific MCP Server

A comprehensive hotel booking system designed specifically for Retell's voice agent requirements, featuring advanced search capabilities, booking management, and real-time availability checking.

## 🚀 Features

### Core Functionality
- **Advanced Hotel Search**: Multi-criteria search with location, capacity, amenities, price, and rating filters
- **Real-time Availability**: Check hotel availability for specific dates
- **Booking Management**: Create, view, and cancel bookings with validation
- **Comprehensive Data**: 15 luxury hotels across Mumbai, Delhi, and Bangalore
- **Date Validation**: Ensures all dates are valid and in the future
- **Email Validation**: Proper email format validation for bookings

### Enhanced Tools
1. **searchHotels** - Advanced hotel search with availability checking
2. **getHotelDetails** - Detailed hotel information with 30-day availability
3. **createBooking** - Create new bookings with full validation
4. **getBooking** - Retrieve booking details by booking ID
5. **cancelBooking** - Cancel bookings within 24 hours
6. **getLocations** - List all available locations
7. **getAmenities** - List all available amenities
8. **getRoomTypes** - List all available room types

## 🏗️ Architecture

### Data Structure
- **Hotels**: CSV-based storage with comprehensive hotel information
- **Bookings**: JSON-based storage with persistent booking data
- **Validation**: Multi-layer validation for dates, emails, and business rules

### API Endpoints
- `GET /` - Server information
- `GET /health` - Health check with statistics
- `GET /tools` - Available tools and schemas
- `POST /execute` - Execute tools with arguments

## 📊 Hotel Data

The system includes 15 luxury hotels with the following information:
- **Names**: Real luxury hotel names (Taj, Oberoi, ITC, etc.)
- **Locations**: Mumbai, Delhi, Bangalore
- **Ratings**: 5-star hotels with guest ratings
- **Amenities**: Comprehensive amenity lists
- **Pricing**: Realistic pricing for luxury hotels
- **Room Types**: Deluxe, Suite, Presidential options

## 🔧 Installation & Setup

### Prerequisites
```bash
pip install flask pandas
```

### Running the Server
```bash
python retell_specific_server.py
```

The server runs on port 5001 by default, or uses the `PORT` environment variable.

### Testing
```bash
python test_enhanced_retell_server.py
```

## 📋 API Usage Examples

### 1. Search Hotels
```json
{
  "name": "searchHotels",
  "arguments": {
    "location": "Mumbai",
    "adults": 2,
    "children": 1,
    "amenities": "Spa,Pool",
    "min_price": 15000,
    "max_price": 25000,
    "min_stars": 5,
    "check_in": "2024-12-20",
    "check_out": "2024-12-23"
  }
}
```

### 2. Get Hotel Details
```json
{
  "name": "getHotelDetails",
  "arguments": {
    "hotel_id": "HOTEL001"
  }
}
```

### 3. Create Booking
```json
{
  "name": "createBooking",
  "arguments": {
    "hotel_id": "HOTEL001",
    "guest_name": "John Doe",
    "guest_email": "john.doe@example.com",
    "guest_phone": "+91-9876543210",
    "check_in": "2024-12-20",
    "check_out": "2024-12-23",
    "adults": 2,
    "children": 1,
    "room_type": "Deluxe",
    "special_requests": "Early check-in preferred"
  }
}
```

### 4. Get Booking Details
```json
{
  "name": "getBooking",
  "arguments": {
    "booking_id": "booking-uuid-here"
  }
}
```

### 5. Cancel Booking
```json
{
  "name": "cancelBooking",
  "arguments": {
    "booking_id": "booking-uuid-here"
  }
}
```

## 🔍 Search Capabilities

### Location Filtering
- Exact city matching (Mumbai, Delhi, Bangalore)
- Case-insensitive search

### Capacity Filtering
- Adults: Maximum capacity check
- Children: Maximum children capacity check

### Amenity Filtering
- Multiple amenities support (comma-separated)
- Case-insensitive matching
- Partial matching

### Price Filtering
- Minimum price per night
- Maximum price per night
- Range-based filtering

### Rating Filtering
- Minimum star rating (1-5)
- Minimum guest rating (0.0-5.0)

### Date Availability
- Real-time availability checking
- Conflict detection with existing bookings
- Future date validation

## ✅ Validation Rules

### Date Validation
- All dates must be in YYYY-MM-DD format
- Check-in and check-out dates must be in the future
- Check-out date must be after check-in date

### Email Validation
- Standard email format validation
- Regex-based validation

### Booking Validation
- Required fields: hotel_id, guest_name, guest_email, check_in, check_out, adults
- Hotel availability check
- Capacity validation

### Cancellation Rules
- Bookings can only be cancelled within 24 hours of creation
- Already cancelled bookings cannot be cancelled again

## 📈 Response Format

### Success Response
```json
{
  "success": true,
  "result": {
    "data": "...",
    "message": "Operation completed successfully"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error description"
}
```

## 🗄️ Data Storage

### Hotel Data (CSV)
- File: `Hotel_Dataset.csv`
- Auto-generated if not exists
- 15 luxury hotels with comprehensive details

### Booking Data (JSON)
- File: `bookings.json`
- Persistent storage across server restarts
- UUID-based booking IDs

## 🔄 Business Logic

### Availability Checking
- Checks for date conflicts with existing bookings
- Returns only available hotels for date ranges
- Real-time availability for hotel details

### Price Calculation
- Automatic calculation based on nights and room rate
- Includes price per night in booking details

### Search Ranking
- Results sorted by guest rating (highest first)
- Limited to top 10 results for performance

## 🛡️ Error Handling

### Comprehensive Error Messages
- Missing required fields
- Invalid date formats
- Hotel not found
- Booking conflicts
- Invalid email formats
- Cancellation restrictions

### Graceful Degradation
- Server continues running on data errors
- Fallback to sample data if CSV is corrupted
- JSON parsing error handling

## 🚀 Performance Features

### Efficient Search
- Pandas-based filtering for fast queries
- Indexed data access
- Optimized date range checking

### Memory Management
- Lazy loading of hotel data
- Efficient booking storage
- Minimal memory footprint

## 🔧 Configuration

### Environment Variables
- `PORT`: Server port (default: 5001)

### File Paths
- Hotel data: `Hotel_Dataset.csv`
- Booking data: `bookings.json`

## 📝 Logging & Monitoring

### Health Endpoint
- Server status
- Hotel count
- Booking count
- Timestamp

### Error Tracking
- Detailed error messages
- Stack trace preservation
- User-friendly error responses

## 🔮 Future Enhancements

### Potential Additions
- Payment processing integration
- Guest review system
- Hotel image management
- Multi-language support
- Advanced analytics
- Email confirmation system
- SMS notifications

### Scalability Improvements
- Database integration (PostgreSQL/MySQL)
- Redis caching
- Load balancing
- Microservices architecture

## 🤝 Integration with Retell

This server is specifically designed for Retell's voice agent requirements:

### Voice-Friendly Responses
- Clear, concise messages
- Structured data for voice synthesis
- Natural language error messages

### Tool Schema Compliance
- Retell-specific tool naming
- Proper input/output schemas
- Consistent response formats

### Real-time Capabilities
- Instant availability checking
- Live booking status
- Immediate confirmation responses

## 📞 Support

For questions or issues:
1. Check the test file for usage examples
2. Review the API documentation
3. Test with the provided test script
4. Check server logs for detailed error information

---

**Version**: 2.0.0  
**Last Updated**: December 2024  
**Compatibility**: Retell Voice Agent Platform 