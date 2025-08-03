# 🏨 Hotel Search MCP Server for Retell

This guide explains how to set up and use the Hotel Search MCP (Model Context Protocol) server with Retell.

## 🎯 What This Does

The MCP server provides hotel search functionality that Retell agents can use during conversations to:
- Search for hotels based on customer preferences
- Get available locations and amenities
- Return filtered results in real-time

## 🚀 Quick Setup

### 1. Deploy to Railway

The MCP server is already deployed at:
```
https://hotel-api-flask-production.up.railway.app
```

### 2. Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mcp/search` | POST | Search hotels with criteria |
| `/mcp/locations` | GET | Get available locations |
| `/mcp/amenities` | GET | Get available amenities |
| `/mcp/health` | GET | Health check |

### 3. Retell Configuration

#### Option A: HTTP API Integration (Recommended)

In Retell, add a new **HTTP API** tool with these settings:

**Base URL:**
```
https://hotel-api-flask-production.up.railway.app
```

**Endpoints to configure:**

1. **Search Hotels**
   - **Path:** `/mcp/search`
   - **Method:** POST
   - **Parameters:**
     ```
     location: {{location}}
     check_in_date: {{check_in_date}}
     check_out_date: {{check_out_date}}
     adults: {{adults}}
     children: {{children}}
     amenities: {{amenities}}
     min_price: {{min_price}}
     max_price: {{max_price}}
     min_stars: {{min_stars}}
     min_rating: {{min_rating}}
     ```

2. **Get Locations**
   - **Path:** `/mcp/locations`
   - **Method:** GET
   - **Parameters:** None

3. **Get Amenities**
   - **Path:** `/mcp/amenities`
   - **Method:** GET
   - **Parameters:** None

#### Option B: MCP Server Integration

If Retell supports direct MCP server connections:

1. **MCP Configuration:**
   ```json
   {
     "mcpServers": {
       "hotel-search": {
         "command": "python3",
         "args": ["mcp_server.py"],
         "env": {
           "PYTHONPATH": "."
         }
       }
     }
   }
   ```

2. **Server URL:** Use the Railway deployment URL

## 🔧 How It Works

### Search Request Example

**Customer says:** "I need a hotel in Mumbai for August 15-20, 2 adults, 1 child, with a pool, under 5000 rupees per night"

**Retell calls:** `POST /mcp/search`
```json
{
  "location": "Mumbai",
  "check_in_date": "2024-08-15",
  "check_out_date": "2024-08-20",
  "adults": 2,
  "children": 1,
  "amenities": "Pool",
  "max_price": 5000
}
```

**Response:**
```json
{
  "success": true,
  "total_matches": 3,
  "hotels": [
    {
      "hotel_id": "HOTEL_001",
      "name": "Mumbai Hotel 1",
      "location": "Mumbai",
      "stars": 4,
      "guest_rating": 4.5,
      "price_per_night": 4500,
      "amenities": "Pool,Gym,WiFi"
    }
  ],
  "message": "Found 3 hotels matching your criteria"
}
```

### Available Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location` | string | Yes | City or location |
| `check_in_date` | string | Yes | Check-in date (YYYY-MM-DD) |
| `check_out_date` | string | Yes | Check-out date (YYYY-MM-DD) |
| `adults` | integer | Yes | Number of adults |
| `children` | integer | No | Number of children |
| `amenities` | string | No | Comma-separated amenities |
| `min_price` | number | No | Minimum price per night |
| `max_price` | number | No | Maximum price per night |
| `min_stars` | integer | No | Minimum star rating (1-5) |
| `max_stars` | integer | No | Maximum star rating (1-5) |
| `min_rating` | number | No | Minimum guest rating (0.0-5.0) |
| `max_rating` | number | No | Maximum guest rating (0.0-5.0) |

## 🧪 Testing

### Test the MCP Server

```bash
# Test locally
python3 test_mcp_server.py

# Test deployed server
curl https://hotel-api-flask-production.up.railway.app/mcp/health
```

### Test Search Endpoint

```bash
curl -X POST https://hotel-api-flask-production.up.railway.app/mcp/search \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Mumbai",
    "check_in_date": "2024-08-15",
    "check_out_date": "2024-08-20",
    "adults": 2,
    "children": 1,
    "amenities": "Pool,Gym",
    "max_price": 5000,
    "min_stars": 4
  }'
```

## 📋 Retell Agent Workflow

1. **Customer asks for hotel recommendations**
2. **Agent collects information** (location, dates, guests, preferences)
3. **Agent calls MCP server** with collected parameters
4. **MCP server returns filtered hotel results**
5. **Agent presents results** to customer in natural language

## 🎯 Example Conversation

**Customer:** "I'm looking for a hotel in Delhi for next weekend, just me and my wife, we'd like a gym and restaurant, budget around 3000-6000 rupees per night"

**Agent:** "I'll help you find hotels in Delhi for next weekend. Let me search for options with a gym and restaurant within your budget."

*[Agent calls MCP server]*

**Agent:** "I found 5 great hotels in Delhi that match your criteria:

1. **Delhi Hotel 15** - 4 stars, ₹4,500/night, Gym, Restaurant, WiFi
2. **Delhi Hotel 23** - 5 stars, ₹5,800/night, Gym, Restaurant, Spa, Pool
3. **Delhi Hotel 7** - 4 stars, ₹3,200/night, Gym, Restaurant, Parking

All hotels have excellent guest ratings and are available for your dates. Would you like me to provide more details about any of these options?"

## 🔧 Troubleshooting

### Common Issues

1. **Server not responding**
   - Check Railway deployment status
   - Verify the URL is correct

2. **No results returned**
   - Check if parameters are valid
   - Verify CSV data exists

3. **Retell integration issues**
   - Ensure HTTP API is configured correctly
   - Check parameter mapping

### Support

If you encounter issues:
1. Check the health endpoint: `/mcp/health`
2. Review Railway logs
3. Test endpoints manually with curl

## 🚀 Next Steps

1. **Configure Retell** with the HTTP API endpoints
2. **Test the integration** with sample conversations
3. **Customize the agent** to handle hotel search requests
4. **Monitor performance** and adjust as needed

The MCP server is now ready to provide hotel search functionality to your Retell agents! 🎉 