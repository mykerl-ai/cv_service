#!/usr/bin/env python3
"""
Web UI for CV Tailoring Service
A simple FastAPI application with HTML interface for uploading and tailoring CVs
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from typing import Optional

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent / "src"))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from generate_tailored_cv import CVTailoringService

# Initialize FastAPI app
app = FastAPI(
    title="CV Tailoring Service",
    description="AI-powered CV optimization service",
    version="1.0.0"
)

# Load sample job description
SAMPLE_JOB_DESCRIPTION = ""
try:
    with open("sample_job_description.txt", "r", encoding="utf-8") as f:
        SAMPLE_JOB_DESCRIPTION = f.read()
except FileNotFoundError:
    SAMPLE_JOB_DESCRIPTION = """
    Senior Software Engineer - Full Stack Development
    
    Company: TechInnovate Solutions
    Location: San Francisco, CA (Hybrid)
    
    We are seeking a talented Senior Software Engineer to join our engineering team. 
    You will be responsible for designing, developing, and maintaining scalable web applications using modern technologies.
    
    Required Skills:
    - 5+ years of experience in software development
    - Strong proficiency in Python, JavaScript, and TypeScript
    - Experience with React, Node.js, and modern frontend frameworks
    - Knowledge of microservices architecture and RESTful APIs
    - Experience with cloud platforms (AWS, Azure, or GCP)
    - Proficiency in database design and SQL (PostgreSQL, MySQL)
    - Experience with Docker and containerization
    - Strong understanding of Git and version control
    - Knowledge of CI/CD pipelines and DevOps practices
    - Experience with agile development methodologies
    """

# Initialize CV Tailoring Service
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Warning: OPENAI_API_KEY not found in environment variables")
    service = None
else:
    service = CVTailoringService(api_key)

# HTML template for the main page
MAIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV Tailoring Service</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .main-content {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .upload-section {
            margin-bottom: 30px;
        }
        
        .upload-section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.8rem;
        }
        
        .file-upload {
            border: 3px dashed #3498db;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            background: #f8f9fa;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .file-upload:hover {
            border-color: #2980b9;
            background: #e3f2fd;
        }
        
        .file-upload input[type="file"] {
            display: none;
        }
        
        .file-upload label {
            font-size: 1.2rem;
            color: #3498db;
            cursor: pointer;
            display: block;
        }
        
        .file-upload p {
            margin-top: 10px;
            color: #7f8c8d;
        }
        
        .job-description {
            margin-bottom: 30px;
        }
        
        .job-description h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .job-description textarea {
            width: 100%;
            height: 200px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
        }
        
        .job-description textarea:focus {
            outline: none;
            border-color: #3498db;
        }
        
        .options {
            margin-bottom: 30px;
        }
        
        .options h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .option-group {
            display: flex;
            gap: 20px;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .option-group label {
            font-weight: 600;
            min-width: 120px;
        }
        
        .option-group select {
            padding: 8px 12px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 14px;
        }
        
        .option-group select:focus {
            outline: none;
            border-color: #3498db;
        }
        
        .submit-btn {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(52, 152, 219, 0.3);
        }
        
        .submit-btn:disabled {
            background: #bdc3c7;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result {
            display: none;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .result.show {
            display: block;
        }
        
        .result h3 {
            color: #27ae60;
            margin-bottom: 15px;
        }
        
        .result-item {
            margin-bottom: 10px;
        }
        
        .result-item strong {
            color: #2c3e50;
        }
        
        .download-btn {
            background: #27ae60;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin-top: 10px;
        }
        
        .download-btn:hover {
            background: #229954;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
            display: none;
        }
        
        .error.show {
            display: block;
        }
        
        .footer {
            text-align: center;
            color: white;
            opacity: 0.8;
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 CV Tailoring Service</h1>
            <p>AI-powered CV optimization for your dream job</p>
        </div>
        
        <div class="main-content">
            <form id="cvForm" enctype="multipart/form-data">
                <div class="upload-section">
                    <h2>📄 Upload Your CV</h2>
                    <div class="file-upload" onclick="document.getElementById('cvFile').click()">
                        <input type="file" id="cvFile" name="cv_file" accept=".pdf,.docx,.txt" required>
                        <label for="cvFile">
                            <strong>📁 Click to upload CV</strong><br>
                            <span>or drag and drop here</span>
                        </label>
                        <p>Supported formats: PDF, DOCX, TXT (Max 10MB)</p>
                    </div>
                    <div id="fileInfo" style="margin-top: 10px; display: none;">
                        <strong>Selected file:</strong> <span id="fileName"></span>
                    </div>
                </div>
                
                <div class="job-description">
                    <h3>🎯 Job Description</h3>
                    <textarea name="job_description" id="jobDescription" placeholder="Paste the job description here..." required>""" + SAMPLE_JOB_DESCRIPTION + """</textarea>
                </div>
                
                <div class="options">
                    <h3>⚙️ Options</h3>
                    <div class="option-group">
                        <label for="template">Template Style:</label>
                        <select name="template" id="template">
                            <option value="modern">Modern</option>
                            <option value="professional">Professional</option>
                            <option value="creative">Creative</option>
                        </select>
                    </div>
                    <div class="option-group">
                        <label for="include_analysis">Include Analysis:</label>
                        <select name="include_analysis" id="include_analysis">
                            <option value="true">Yes</option>
                            <option value="false">No</option>
                        </select>
                    </div>
                </div>
                
                <button type="submit" class="submit-btn" id="submitBtn">
                    🚀 Generate Tailored CV
                </button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Processing your CV... This may take a few minutes.</p>
            </div>
            
            <div class="result" id="result">
                <h3>✅ CV Generated Successfully!</h3>
                <div class="result-item">
                    <strong>Optimization Score:</strong> <span id="optimizationScore"></span>
                </div>
                <div class="result-item">
                    <strong>Job Title:</strong> <span id="jobTitle"></span>
                </div>
                <div class="result-item">
                    <strong>Company:</strong> <span id="companyName"></span>
                </div>
                <div class="result-item">
                    <strong>Processing Time:</strong> <span id="processingTime"></span>
                </div>
                <div class="result-item" id="improvementsSection" style="display: none;">
                    <strong>Improvements Made:</strong>
                    <ul id="improvementsList"></ul>
                </div>
                <div class="result-item" id="skillGapsSection" style="display: none;">
                    <strong>Skill Gaps Identified:</strong>
                    <ul id="skillGapsList"></ul>
                </div>
                <a href="#" class="download-btn" id="downloadBtn">📥 Download Tailored CV</a>
            </div>
            
            <div class="error" id="error">
                <strong>Error:</strong> <span id="errorMessage"></span>
            </div>
        </div>
        
        <div class="footer">
            <p>Powered by OpenAI • CV Tailoring Service v1.0</p>
        </div>
    </div>
    
    <script>
        // File upload handling
        document.getElementById('cvFile').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                document.getElementById('fileName').textContent = file.name;
                document.getElementById('fileInfo').style.display = 'block';
            }
        });
        
        // Drag and drop functionality
        const fileUpload = document.querySelector('.file-upload');
        
        fileUpload.addEventListener('dragover', function(e) {
            e.preventDefault();
            fileUpload.style.borderColor = '#2980b9';
            fileUpload.style.background = '#e3f2fd';
        });
        
        fileUpload.addEventListener('dragleave', function(e) {
            e.preventDefault();
            fileUpload.style.borderColor = '#3498db';
            fileUpload.style.background = '#f8f9fa';
        });
        
        fileUpload.addEventListener('drop', function(e) {
            e.preventDefault();
            fileUpload.style.borderColor = '#3498db';
            fileUpload.style.background = '#f8f9fa';
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                document.getElementById('cvFile').files = files;
                document.getElementById('fileName').textContent = files[0].name;
                document.getElementById('fileInfo').style.display = 'block';
            }
        });
        
        // Form submission
        document.getElementById('cvForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData();
            const cvFile = document.getElementById('cvFile').files[0];
            const jobDescription = document.getElementById('jobDescription').value;
            const template = document.getElementById('template').value;
            const includeAnalysis = document.getElementById('include_analysis').value;
            
            if (!cvFile) {
                showError('Please select a CV file');
                return;
            }
            
            if (!jobDescription.trim()) {
                showError('Please enter a job description');
                return;
            }
            
            formData.append('cv_file', cvFile);
            formData.append('job_description', jobDescription);
            formData.append('template', template);
            formData.append('include_analysis', includeAnalysis);
            
            // Show loading
            showLoading(true);
            hideError();
            hideResult();
            
            try {
                const response = await fetch('/tailor-cv', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    showResult(result);
                } else {
                    showError(result.detail || 'An error occurred');
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            } finally {
                showLoading(false);
            }
        });
        
        function showLoading(show) {
            const loading = document.getElementById('loading');
            const submitBtn = document.getElementById('submitBtn');
            
            if (show) {
                loading.classList.add('show');
                submitBtn.disabled = true;
                submitBtn.textContent = '⏳ Processing...';
            } else {
                loading.classList.remove('show');
                submitBtn.disabled = false;
                submitBtn.textContent = '🚀 Generate Tailored CV';
            }
        }
        
        function showResult(result) {
            const resultDiv = document.getElementById('result');
            const downloadBtn = document.getElementById('downloadBtn');
            
            document.getElementById('optimizationScore').textContent = result.optimization_score + '%';
            document.getElementById('jobTitle').textContent = result.job_title;
            document.getElementById('companyName').textContent = result.company_name;
            document.getElementById('processingTime').textContent = result.processing_time + ' seconds';
            
            // Show improvements if available
            if (result.improvements_made && result.improvements_made.length > 0) {
                const improvementsList = document.getElementById('improvementsList');
                improvementsList.innerHTML = '';
                result.improvements_made.forEach(improvement => {
                    const li = document.createElement('li');
                    li.textContent = improvement;
                    improvementsList.appendChild(li);
                });
                document.getElementById('improvementsSection').style.display = 'block';
            } else {
                document.getElementById('improvementsSection').style.display = 'none';
            }
            
            // Show skill gaps if available
            if (result.skill_gaps_identified && result.skill_gaps_identified.length > 0) {
                const skillGapsList = document.getElementById('skillGapsList');
                skillGapsList.innerHTML = '';
                result.skill_gaps_identified.forEach(gap => {
                    const li = document.createElement('li');
                    li.textContent = gap;
                    skillGapsList.appendChild(li);
                });
                document.getElementById('skillGapsSection').style.display = 'block';
            } else {
                document.getElementById('skillGapsSection').style.display = 'none';
            }
            
            // Set download link
            downloadBtn.href = '/download/' + result.output_file.split('/').pop();
            
            resultDiv.classList.add('show');
        }
        
        function hideResult() {
            document.getElementById('result').classList.remove('show');
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('error');
            document.getElementById('errorMessage').textContent = message;
            errorDiv.classList.add('show');
        }
        
        function hideError() {
            document.getElementById('error').classList.remove('show');
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    """Main page with the CV upload form"""
    return MAIN_HTML

@app.post("/tailor-cv")
async def tailor_cv(
    cv_file: UploadFile = File(...),
    job_description: str = Form(...),
    template: str = Form("modern"),
    include_analysis: str = Form("true")
):
    """Process CV upload and generate tailored CV"""
    if not service:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(cv_file.filename).suffix) as temp_file:
            content = await cv_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Generate output filename
        output_filename = f"tailored_cv_{int(os.path.getmtime(temp_file_path))}.pdf"
        output_path = os.path.join(tempfile.gettempdir(), output_filename)
        
        # Process CV
        results = service.generate_tailored_cv(
            cv_file_path=temp_file_path,
            job_description=job_description,
            output_path=output_path,
            template_style=template,
            include_analysis=include_analysis.lower() == "true"
        )
        
        # Clean up temporary input file
        os.unlink(temp_file_path)
        
        if results["success"]:
            return {
                "success": True,
                "output_file": results["output_file"],
                "optimization_score": results["optimization_score"],
                "job_title": results["job_title"],
                "company_name": results["company_name"],
                "processing_time": results["processing_time"],
                "improvements_made": results.get("improvements_made", []),
                "skill_gaps_identified": results.get("skill_gaps_identified", [])
            }
        else:
            raise HTTPException(status_code=500, detail=results["error"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated CV file"""
    file_path = os.path.join(tempfile.gettempdir(), filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/pdf'
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "cv_tailoring_web_ui"}

if __name__ == "__main__":
    print("🚀 Starting CV Tailoring Web UI...")
    print("📱 Open your browser and go to: http://localhost:8000")
    print("🔑 Make sure your OpenAI API key is set in the .env file")
    
    uvicorn.run(
        "web_ui:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 