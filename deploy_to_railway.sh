#!/bin/bash

echo "🚀 Deploying Enhanced Hotel Filtering API to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "npm install -g @railway/cli"
    echo "railway login"
    exit 1
fi

# Check if we're logged in to Railway
if ! railway whoami &> /dev/null; then
    echo "❌ Not logged in to Railway. Please run: railway login"
    exit 1
fi

echo "✅ Railway CLI found and logged in"

# Commit changes
echo "📝 Committing changes..."
git add .
git commit -m "Deploy enhanced hotel filtering API with voice agent webhook system"

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "🌐 Your enhanced API should be available at: https://hotel-api-flask-production.up.railway.app"
echo "🔍 Test the health endpoint: https://hotel-api-flask-production.up.railway.app/webhook/health"
echo "🏨 Test hotel search: https://hotel-api-flask-production.up.railway.app/webhook/hotels/search/advanced"
