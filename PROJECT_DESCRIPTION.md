# Hotel API - Flask REST API with Comprehensive Filtering

## 🏨 Project Overview

A robust Flask-based REST API that loads hotel data from a CSV file and provides comprehensive filtering and sorting capabilities. This API is designed for hotel booking platforms, travel agencies, and hospitality management systems.

## ✨ Key Features

### 🔍 **Comprehensive Filtering**
- **Location-based filtering** with case-insensitive text search
- **Date range filtering** for check-in and check-out dates
- **Star rating filtering** with min/max range support (1-5 stars)
- **Guest rating filtering** with decimal precision (0.0-5.0)
- **Amenities filtering** with comma-separated list support
- **Price range filtering** with min/max values
- **Guest capacity filtering** for adults and children

### 📊 **Advanced Sorting**
- **Default sorting** by guest rating in descending order
- **Custom sorting** by any field in ascending/descending order
- **Flexible endpoints** for basic and advanced filtering

### 🛠 **Technical Features**
- **RESTful API design** with JSON responses
- **Error handling** with appropriate HTTP status codes
- **Automatic data loading** from CSV files
- **Sample data generation** for testing
- **Comprehensive documentation** with examples
- **Test suite** for validation

## 🚀 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API documentation and examples |
| `/api/hotels` | GET | Get all hotels with basic filtering |
| `/api/hotels/advanced` | GET | Advanced filtering with custom sorting |
| `/api/hotels/<id>` | GET | Get specific hotel by ID |
| `/api/locations` | GET | Get all available locations |
| `/api/amenities` | GET | Get all available amenities |
| `/api/stats` | GET | Get hotel statistics |

## 📁 Project Structure

```
hotel_api/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Hotel_Dataset.csv      # Hotel data source
├── test_api.py           # API test suite
├── README.md             # Comprehensive documentation
├── .gitignore            # Git ignore rules
└── PROJECT_DESCRIPTION.md # This file
```

## 🛠 Technology Stack

- **Backend**: Flask (Python)
- **Data Processing**: Pandas
- **Data Storage**: CSV files
- **Testing**: Requests library
- **Documentation**: Markdown

## 📊 Data Schema

The API works with hotel data containing the following fields:
- `hotel_id`: Unique identifier
- `hotel_name`: Hotel name
- `location`: City/location
- `check_in_date`: Available check-in date
- `check_out_date`: Available check-out date
- `stars`: Star rating (1-5)
- `guest_rating`: Guest rating (0.0-5.0)
- `amenities`: Comma-separated amenities list
- `price_per_night`: Price per night in local currency
- `max_adults`: Maximum number of adults
- `max_children`: Maximum number of children

## 🎯 Use Cases

- **Hotel Booking Platforms**: Filter and search hotels based on various criteria
- **Travel Agencies**: Find hotels matching specific requirements
- **Hospitality Management**: Manage and query hotel inventory
- **Data Analysis**: Analyze hotel data and statistics
- **API Integration**: Serve as backend for hotel search applications

## 🔧 Installation & Setup

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run the API**: `python3 app.py`
4. **Access the API**: `http://localhost:5001`
5. **Run tests**: `python3 test_api.py`

## 📈 Performance

- **100+ hotels** loaded from CSV
- **10+ locations** supported
- **36+ amenities** available
- **Real-time filtering** and sorting
- **JSON responses** for easy integration

## 🤝 Contributing

This project is open for contributions. Please feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Flask and Python** 