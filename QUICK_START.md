# Quick Start Guide - Enhanced Retell Server

Get your enhanced hotel booking server running in minutes!

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install flask pandas requests
```

### Step 2: Start the Server
```bash
python run_enhanced_server.py
```

### Step 3: Test the Server
```bash
python test_enhanced_retell_server.py
```

That's it! Your server is now running at `http://localhost:5001`

## 📋 What You Get

✅ **15 Luxury Hotels** - Real hotel names across Mumbai, Delhi, Bangalore  
✅ **8 Powerful Tools** - Search, book, manage, and more  
✅ **Real-time Availability** - Check dates and book instantly  
✅ **Full Validation** - Dates, emails, capacity, and business rules  
✅ **Persistent Bookings** - Your bookings survive server restarts  

## 🔗 Quick API Test

Test the server is working:
```bash
curl http://localhost:5001/health
```

## 🛠️ Available Tools

| Tool | Description | Example Use |
|------|-------------|-------------|
| `searchHotels` | Find hotels with filters | Search Mumbai hotels with pool |
| `getHotelDetails` | Get detailed hotel info | View availability for 30 days |
| `createBooking` | Book a hotel room | Make a reservation |
| `getBooking` | View booking details | Check reservation status |
| `cancelBooking` | Cancel a booking | Cancel within 24 hours |
| `getLocations` | List all cities | Show available locations |
| `getAmenities` | List all amenities | Show available features |
| `getRoomTypes` | List room types | Show Deluxe, Suite, Presidential |

## 📊 Sample Data Included

- **Taj Palace Mumbai** - Luxury sea view hotel
- **Oberoi Delhi** - Historic luxury hotel  
- **ITC Gardenia Bangalore** - Garden-themed luxury
- **Four Seasons Mumbai** - Modern luxury in Worli
- **The Leela Palace Delhi** - Diplomatic enclave luxury
- And 10 more luxury hotels...

## 🎯 Perfect for Retell

This server is specifically designed for Retell voice agents:
- ✅ Voice-friendly responses
- ✅ Proper tool schemas
- ✅ Real-time availability
- ✅ Natural language error messages
- ✅ Instant booking confirmations

## 🔧 Configuration

### Change Port
```bash
export PORT=8080
python run_enhanced_server.py
```

### Environment Variables
- `PORT` - Server port (default: 5001)

## 📁 Files Created

- `Hotel_Dataset.csv` - Hotel data (auto-generated)
- `bookings.json` - Booking storage (auto-created)

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5001
lsof -ti:5001 | xargs kill -9
```

### Dependencies Missing
```bash
pip install flask pandas requests
```

### Server Won't Start
```bash
# Check Python version
python --version  # Should be 3.7+

# Check if files exist
ls -la retell_specific_server.py
```

## 📞 Need Help?

1. Check the full documentation: `README_ENHANCED_RETELL.md`
2. Run the test suite: `python test_enhanced_retell_server.py`
3. Check server logs for error messages

---

**Ready to go!** Your enhanced Retell server is now running and ready for voice agent integration. 🎉 