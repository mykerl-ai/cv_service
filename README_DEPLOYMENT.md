# 🚀 Quick Deploy to Render

## Prerequisites
- GitHub repository with your code
- OpenAI API key
- Render account

## Deploy Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Deploy on Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml`

### 3. Set Environment Variables
In your service settings, add:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Test Deployment
```bash
python test_deployment.py
```

## API Endpoints
- **Health Check**: `GET /health`
- **API Docs**: `GET /docs`
- **Optimize CV**: `POST /api/v1/optimize-cv`
- **Analyze Job**: `POST /api/v1/analyze-job`

## Configuration
- **Runtime**: Python 3.11.0
- **Build**: `pip install -r requirements.txt`
- **Start**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

## Troubleshooting
- Check Render logs for build errors
- Verify environment variables are set
- Test locally first: `python src/api/main.py`

For detailed deployment guide, see `DEPLOYMENT_GUIDE.md` 