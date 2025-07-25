# CV Tailoring Service - Render Deployment Guide

This guide will walk you through deploying your CV Tailoring Service as a backend service on Render.

## 🚀 Quick Deploy Steps

### 1. Prepare Your Repository

Your repository is already well-structured for deployment with:
- ✅ `render.yaml` - Render configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `src/api/main.py` - FastAPI application
- ✅ `runtime.txt` - Python version specification
- ✅ `Procfile` - Process definition

### 2. Deploy on Render

#### Option A: Deploy using render.yaml (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Deploy on Render Dashboard**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect and use the `render.yaml` configuration

3. **Set Environment Variables**
   - In your service settings, add:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

#### Option B: Manual Deploy

1. **Create Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: `cv-tailoring-service`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Starter` (or your preferred plan)

3. **Set Environment Variables**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   HOST=0.0.0.0
   PORT=8000
   DEBUG=false
   MAX_FILE_SIZE=10485760
   LOG_LEVEL=INFO
   ```

## 🔧 Configuration Details

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | - | ✅ Yes |
| `HOST` | Host to bind to | `0.0.0.0` | No |
| `PORT` | Port to run on | `8000` | No |
| `DEBUG` | Enable debug mode | `false` | No |
| `MAX_FILE_SIZE` | Max file upload size (bytes) | `10485760` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

### Service Configuration

- **Runtime**: Python 3.11.0
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
- **Health Check**: `/health`

## 📡 API Endpoints

Once deployed, your service will be available at:
- **Base URL**: `https://your-service-name.onrender.com`
- **API Documentation**: `https://your-service-name.onrender.com/docs`
- **Health Check**: `https://your-service-name.onrender.com/health`

### Available Endpoints

- `POST /api/v1/optimize-cv` - Optimize CV for job description
- `POST /api/v1/analyze-job` - Analyze job description
- `GET /api/v1/download/{filename}` - Download generated CV
- `GET /api/v1/templates` - Get available CV templates
- `GET /api/v1/formats` - Get available output formats
- `GET /health` - Health check

## 🧪 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-service-name.onrender.com/health
```

### 2. Test API Documentation
Visit: `https://your-service-name.onrender.com/docs`

### 3. Test Job Analysis
```bash
curl -X POST "https://your-service-name.onrender.com/api/v1/analyze-job" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Senior Software Engineer position requiring Python, JavaScript, and React experience."
  }'
```

### 4. Test CV Optimization
```bash
curl -X POST "https://your-service-name.onrender.com/api/v1/optimize-cv" \
  -F "cv_file=@your_cv.pdf" \
  -F "job_description=Senior Software Engineer position..." \
  -F "output_format=pdf" \
  -F "template_style=modern"
```

## 🔒 Security Considerations

1. **API Key Security**
   - Never commit your OpenAI API key to version control
   - Use environment variables in production
   - Rotate your API key regularly

2. **File Upload Security**
   - File size limits are enforced (10MB max)
   - Only supported file types are accepted
   - Files are processed in temporary storage

3. **Rate Limiting**
   - Consider implementing rate limiting for production use
   - Monitor API usage to avoid OpenAI rate limits

## 🐛 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version compatibility
   - Check build logs for specific errors

2. **Runtime Errors**
   - Verify environment variables are set correctly
   - Check application logs in Render dashboard
   - Ensure OpenAI API key is valid

3. **File Upload Issues**
   - Check file size limits
   - Verify file format is supported
   - Check temporary storage permissions

### Logs and Monitoring

- View logs in the Render dashboard
- Monitor service health at `/health` endpoint
- Set up alerts for service downtime

## 📈 Scaling

### Render Plans

- **Starter**: Good for development and testing
- **Standard**: Better for production workloads
- **Pro**: For high-traffic applications

### Performance Optimization

1. **Caching**
   - Consider implementing Redis for caching
   - Cache job analysis results
   - Cache template configurations

2. **File Storage**
   - Use external storage (AWS S3, etc.) for generated files
   - Implement file cleanup policies
   - Consider CDN for file delivery

3. **Database**
   - Add database for user management
   - Store optimization history
   - Track usage analytics

## 🔄 CI/CD

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v1.0.0
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

## 📞 Support

For deployment issues:
1. Check Render documentation
2. Review application logs
3. Verify environment configuration
4. Test locally before deploying

For API issues:
1. Check API documentation at `/docs`
2. Verify request format
3. Check OpenAI API status
4. Review error messages in logs

## 🎉 Success!

Once deployed, your CV Tailoring Service will be available as a fully functional backend API that can:
- Analyze job descriptions
- Optimize CVs for specific positions
- Generate tailored PDF CVs
- Provide optimization suggestions
- Handle file uploads and downloads

Your service is now ready to be integrated into frontend applications or used directly via API calls! 