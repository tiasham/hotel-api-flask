# Railway Deployment Guide

## 🚀 Deploying Hotel API to Railway

This guide will help you deploy the Flask Hotel API to Railway successfully.

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be on GitHub (already done)
3. **Railway CLI** (optional): `npm install -g @railway/cli`

## 🔧 Deployment Steps

### Method 1: Deploy from GitHub (Recommended)

1. **Connect to Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `tiasham/hotel-api-flask`

2. **Configure Environment**:
   - Railway will automatically detect it's a Python project
   - The `railway.json` file will configure the deployment
   - No additional environment variables needed

3. **Deploy**:
   - Click "Deploy" and wait for the build to complete
   - Railway will use the `Procfile` to start the application

### Method 2: Using Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

## 🛠 Configuration Files Added

### 1. `Procfile`
```
web: python app.py
```
- Tells Railway how to start the application

### 2. `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app.py",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```
- Configures Railway deployment settings
- Sets up health checks and restart policies

### 3. `runtime.txt`
```
python-3.9.18
```
- Specifies Python version for Railway

### 4. `requirements.txt` (Updated)
```
Flask==2.2.5
pandas==1.5.3
numpy==1.24.3
Werkzeug==2.2.3
requests==2.28.2
gunicorn==20.1.0
```
- Compatible versions for Railway deployment
- Added gunicorn for production WSGI server

### 5. `Dockerfile` (Alternative)
- Containerized deployment option
- Can be used if NIXPACKS fails

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. **Dependency Installation Fails**
**Error**: `pip install` fails with exit code 2

**Solution**: 
- Updated `requirements.txt` with compatible versions
- Added `gunicorn` for production deployment
- Specified Python 3.9.18 in `runtime.txt`

#### 2. **Port Configuration Issues**
**Error**: Application not accessible

**Solution**:
- Updated `app.py` to use `PORT` environment variable
- Railway automatically sets the `PORT` environment variable

#### 3. **Build Timeout**
**Error**: Build takes too long and times out

**Solution**:
- Optimized `requirements.txt` with lighter versions
- Added `railway.json` with proper build configuration

#### 4. **Health Check Failures**
**Error**: Health check fails after deployment

**Solution**:
- Added health check configuration in `railway.json`
- Set health check path to `/` (API documentation endpoint)

## 🚀 Deployment Verification

After successful deployment:

1. **Check the URL**: Railway will provide a public URL
2. **Test the API**: Visit the URL to see the API documentation
3. **Test Endpoints**:
   ```bash
   # Test API documentation
   curl https://your-railway-url.railway.app/
   
   # Test hotels endpoint
   curl https://your-railway-url.railway.app/api/hotels
   
   # Test filtering
   curl https://your-railway-url.railway.app/api/hotels?location=Mumbai
   ```

## 📊 Monitoring

Railway provides:
- **Logs**: View application logs in real-time
- **Metrics**: Monitor CPU, memory, and network usage
- **Deployments**: Track deployment history and rollbacks

## 🔄 Continuous Deployment

Railway automatically deploys when you push to the main branch:
1. Push changes to GitHub
2. Railway detects the changes
3. Automatic deployment starts
4. New version goes live

## 🛡️ Environment Variables

If you need to add environment variables:
1. Go to your Railway project
2. Click on "Variables" tab
3. Add any required environment variables

## 📝 Notes

- **Free Tier**: Railway offers a generous free tier
- **Custom Domain**: You can add custom domains in Railway settings
- **SSL**: Automatic SSL certificates provided
- **Scaling**: Easy to scale up/down based on traffic

## 🆘 Support

If deployment still fails:
1. Check Railway logs for specific error messages
2. Verify all files are committed to GitHub
3. Try the Dockerfile deployment method
4. Contact Railway support if needed

---

**Your Hotel API should now deploy successfully on Railway!** 🎉 