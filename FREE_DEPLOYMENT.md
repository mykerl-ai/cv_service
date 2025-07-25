# 🆓 Free Deployment Guide - No Payment Required

This guide shows you how to deploy your CV Tailoring Service for free on various platforms.

## 🚀 Option 1: Render Free Tier

### Step 1: Manual Deploy (No Blueprint)
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service" (NOT Blueprint)
3. Connect your GitHub repository: `https://github.com/mykerl-ai/cv_service.git`
4. Configure manually:
   - **Name**: `cv-tailoring-service`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free` (select this option)

### Step 2: Set Environment Variables
In your service settings, add:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 3: Deploy
Click "Create Web Service" - this will deploy for free!

## 🚂 Option 2: Railway (Free Tier)

### Step 1: Deploy to Railway
1. Go to [Railway](https://railway.app/)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository: `mykerl-ai/cv_service`
5. Railway will auto-detect the configuration

### Step 2: Set Environment Variables
In Railway dashboard:
1. Go to your project
2. Click "Variables" tab
3. Add: `OPENAI_API_KEY=your_openai_api_key_here`

### Step 3: Deploy
Railway will automatically deploy your service for free!

## 🌐 Option 3: Fly.io (Free Tier)

### Step 1: Install Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Or download from: https://fly.io/docs/hands-on/install-flyctl/
```

### Step 2: Create Fly App
```bash
fly auth signup
fly launch
# Follow the prompts, select "No" for database
```

### Step 3: Deploy
```bash
fly deploy
```

## 🐳 Option 4: Render Free Tier (Alternative Method)

If the blueprint method asks for payment, try this:

### Step 1: Create Service Manually
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. **Important**: Make sure to select "Free" plan (not Starter)

### Step 2: Configure Service
- **Name**: `cv-tailoring-service`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Set Environment Variables
Add your OpenAI API key in the environment variables section.

## 📋 Free Tier Limitations

### Render Free Tier
- ✅ 750 hours/month (enough for 24/7 usage)
- ✅ 512MB RAM
- ✅ Shared CPU
- ✅ Automatic deploys
- ⚠️ Service sleeps after 15 minutes of inactivity
- ⚠️ Cold start takes 30-60 seconds

### Railway Free Tier
- ✅ $5 credit monthly
- ✅ 500 hours/month
- ✅ 512MB RAM
- ✅ Automatic deploys
- ⚠️ Service may sleep after inactivity

### Fly.io Free Tier
- ✅ 3 shared-cpu-1x 256mb VMs
- ✅ 3GB persistent volume storage
- ✅ 160GB outbound data transfer
- ✅ Global edge deployment

## 🔧 Troubleshooting Free Deployments

### If Render asks for payment:
1. Make sure you're selecting "Free" plan, not "Starter"
2. Try the manual deployment method above
3. Check if you have any existing paid services

### If service doesn't start:
1. Check the build logs for errors
2. Verify environment variables are set
3. Ensure the start command is correct

### If service sleeps:
1. This is normal for free tiers
2. First request will take 30-60 seconds
3. Subsequent requests will be faster

## 🎯 Recommended: Render Free Tier

For your CV service, I recommend **Render Free Tier** because:
- ✅ Most generous free tier
- ✅ Easy deployment
- ✅ Good performance
- ✅ Automatic HTTPS
- ✅ Custom domains supported

## 🚀 Quick Start Commands

After deploying, test your service:

```bash
# Test health check
curl https://your-service-name.onrender.com/health

# Test API docs
open https://your-service-name.onrender.com/docs
```

## 💡 Pro Tips for Free Deployment

1. **Optimize for cold starts**: Your service will sleep after inactivity
2. **Monitor usage**: Stay within free tier limits
3. **Use environment variables**: Never commit API keys
4. **Test thoroughly**: Free tiers may have different behavior than paid

Your service will be fully functional on any of these free platforms! 🎉 