"""
Main FastAPI application for the CV writer service
"""
import os
import logging
import tempfile
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .routes import router
from ..core.cv_analyzer import CVAnalyzer
from ..core.job_analyzer import JobAnalyzer
from ..core.cv_optimizer import CVOptimizer
from ..core.cv_generator import CVGenerator
from ..utils.file_processor import FileProcessor
from ..models.cv_data import CVData
from ..models.job_data import JobAnalysisResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Smart CV Writer Service",
    description="AI-powered CV optimization service that tailors CVs to specific job descriptions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")


class OptimizeCVRequest(BaseModel):
    """Request model for CV optimization"""
    job_description: str
    output_format: str = "pdf"
    template_style: str = "modern"
    include_original: bool = False


class AnalyzeJobRequest(BaseModel):
    """Request model for job analysis"""
    job_description: str


class OptimizationResponse(BaseModel):
    """Response model for CV optimization"""
    success: bool
    optimization_score: float
    improvements_made: list
    skill_gaps_identified: list
    output_file_path: str
    processing_time: float
    error_message: Optional[str] = None


class JobAnalysisResponse(BaseModel):
    """Response model for job analysis"""
    success: bool
    job_title: str
    company_name: str
    required_skills: list
    preferred_skills: list
    experience_requirements: dict
    education_requirements: dict
    suggestions: list
    processing_time: float
    error_message: Optional[str] = None


# Initialize services
def get_services():
    """Get initialized services"""
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    return {
        "cv_analyzer": CVAnalyzer(api_key),
        "job_analyzer": JobAnalyzer(api_key),
        "cv_optimizer": CVOptimizer(api_key),
        "cv_generator": CVGenerator(),
        "file_processor": FileProcessor()
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Smart CV Writer Service",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}


@app.post("/api/v1/optimize-cv", response_model=OptimizationResponse)
async def optimize_cv(
    cv_file: UploadFile = File(...),
    job_description: str = None,
    output_format: str = "pdf",
    template_style: str = "modern",
    services: dict = Depends(get_services)
):
    """
    Optimize a CV for a specific job description
    
    - **cv_file**: CV file (PDF, DOCX, or TXT)
    - **job_description**: Job description text
    - **output_format**: Output format (pdf, docx, txt)
    - **template_style**: Template style (modern, professional, creative)
    """
    try:
        # Validate file
        if not cv_file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Validate output format
        if output_format not in ["pdf", "docx", "txt"]:
            raise HTTPException(status_code=400, detail="Invalid output format")
        
        # Validate template style
        if template_style not in ["modern", "professional", "creative"]:
            raise HTTPException(status_code=400, detail="Invalid template style")
        
        # Process CV file
        cv_analyzer = services["cv_analyzer"]
        file_processor = services["file_processor"]
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(cv_file.filename).suffix) as temp_file:
            content = await cv_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Parse CV
            cv_data = cv_analyzer.parse_cv(temp_file_path)
            
            # Analyze job description
            job_analyzer = services["job_analyzer"]
            job_analysis = job_analyzer.analyze_job_description(job_description)
            
            # Optimize CV
            cv_optimizer = services["cv_optimizer"]
            optimization_result = cv_optimizer.optimize_cv(cv_data, job_analysis)
            
            # Generate output file
            cv_generator = services["cv_generator"]
            cv_generator.template_style = template_style
            
            output_filename = f"optimized_cv_{job_analysis.job_description.title.replace(' ', '_')}.{output_format}"
            output_path = os.path.join(tempfile.gettempdir(), output_filename)
            
            if output_format == "pdf":
                cv_generator.generate_pdf(optimization_result.optimized_cv, output_path)
            elif output_format == "docx":
                cv_generator.generate_docx(optimization_result.optimized_cv, output_path)
            else:  # txt
                cv_generator.generate_text(optimization_result.optimized_cv, output_path)
            
            return OptimizationResponse(
                success=True,
                optimization_score=optimization_result.optimization_score,
                improvements_made=optimization_result.improvements_made,
                skill_gaps_identified=optimization_result.skill_gaps_identified,
                output_file_path=output_path,
                processing_time=optimization_result.processing_time
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except Exception as e:
        logger.error(f"Error optimizing CV: {str(e)}")
        return OptimizationResponse(
            success=False,
            optimization_score=0.0,
            improvements_made=[],
            skill_gaps_identified=[],
            output_file_path="",
            processing_time=0.0,
            error_message=str(e)
        )


@app.post("/api/v1/analyze-job", response_model=JobAnalysisResponse)
async def analyze_job(
    request: AnalyzeJobRequest,
    services: dict = Depends(get_services)
):
    """
    Analyze a job description and extract requirements
    
    - **job_description**: Job description text
    """
    try:
        job_analyzer = services["job_analyzer"]
        job_analysis = job_analyzer.analyze_job_description(request.job_description)
        
        return JobAnalysisResponse(
            success=True,
            job_title=job_analysis.job_description.title,
            company_name=job_analysis.job_description.company.name,
            required_skills=[skill.skill_name for skill in job_analysis.job_description.required_skills],
            preferred_skills=[skill.skill_name for skill in job_analysis.job_description.preferred_skills],
            experience_requirements={
                "years_required": job_analysis.job_description.experience_requirements.years_required,
                "role_type": job_analysis.job_description.experience_requirements.role_type
            },
            education_requirements={
                "degree_level": job_analysis.job_description.education_requirements.degree_level,
                "required": job_analysis.job_description.education_requirements.required
            },
            suggestions=job_analysis.suggestions,
            processing_time=job_analysis.processing_time
        )
    
    except Exception as e:
        logger.error(f"Error analyzing job: {str(e)}")
        return JobAnalysisResponse(
            success=False,
            job_title="",
            company_name="",
            required_skills=[],
            preferred_skills=[],
            experience_requirements={},
            education_requirements={},
            suggestions=[],
            processing_time=0.0,
            error_message=str(e)
        )


@app.get("/api/v1/download/{filename}")
async def download_file(filename: str):
    """Download generated CV file"""
    file_path = os.path.join(tempfile.gettempdir(), filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )


@app.get("/api/v1/templates")
async def get_templates():
    """Get available CV templates"""
    return {
        "templates": [
            {
                "name": "modern",
                "description": "Clean and modern design with blue accent colors",
                "font_family": "Helvetica",
                "suitable_for": ["technology", "startups", "creative industries"]
            },
            {
                "name": "professional",
                "description": "Traditional professional design with conservative styling",
                "font_family": "Times-Roman",
                "suitable_for": ["finance", "consulting", "corporate"]
            },
            {
                "name": "creative",
                "description": "Bold and creative design with purple accent colors",
                "font_family": "Helvetica",
                "suitable_for": ["design", "marketing", "advertising"]
            }
        ]
    }


@app.get("/api/v1/formats")
async def get_formats():
    """Get available output formats"""
    return {
        "formats": [
            {
                "name": "pdf",
                "description": "Portable Document Format - best for printing and sharing",
                "recommended": True
            },
            {
                "name": "docx",
                "description": "Microsoft Word format - editable and widely compatible",
                "recommended": False
            },
            {
                "name": "txt",
                "description": "Plain text format - ATS-friendly and simple",
                "recommended": False
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    # Run the application
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    ) 