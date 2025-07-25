# CV Tailoring Service - Deployment Guide

This guide explains how to deploy the CV Tailoring Service on Render.

## 🚀 Quick Deploy on Render

### Option 1: Deploy from GitHub (Recommended)

1. **Fork/Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd cv_writer_service
   ```

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial deployment setup"
   git push origin main
   ```

3. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository
   - Configure the service:
     - **Name**: `cv-tailoring-service`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
     - **Plan**: `Starter` (or your preferred plan)

4. **Set Environment Variables**
   - Go to your service settings
   - Add environment variables:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     HOST=0.0.0.0
     PORT=8000
     DEBUG=false
     MAX_FILE_SIZE=10485760
     LOG_LEVEL=INFO
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for the build to complete
   - Your service will be available at `https://your-service-name.onrender.com`

### Option 2: Deploy using render.yaml

1. **Push your code to GitHub** (including the `render.yaml` file)

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect and use the `render.yaml` configuration

3. **Set Environment Variables**
   - Add your `OPENAI_API_KEY` in the service settings

## 🔧 Configuration

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

- **Runtime**: Python 3.11
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

## 🔒 Security Considerations

1. **API Key Security**
   - Never commit your OpenAI API key to version control
   - Use environment variables in production
   - Rotate your API key regularly

2. **File Upload Security**
   - File size limits are enforced
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