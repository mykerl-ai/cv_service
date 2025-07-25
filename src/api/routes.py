"""
API routes for the CV writer service
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class SuggestionRequest(BaseModel):
    """Request model for getting optimization suggestions"""
    cv_data: dict
    job_analysis: dict


class SuggestionResponse(BaseModel):
    """Response model for optimization suggestions"""
    suggestions: List[str]
    priority: str  # high, medium, low
    category: str  # skills, experience, summary, formatting


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "cv_writer"}


@router.post("/suggestions", response_model=SuggestionResponse)
async def get_optimization_suggestions(request: SuggestionRequest):
    """
    Get optimization suggestions for CV improvement
    
    - **cv_data**: Parsed CV data
    - **job_analysis**: Job analysis results
    """
    try:
        # This would implement suggestion logic based on CV and job analysis
        suggestions = [
            "Consider adding more quantified achievements",
            "Highlight relevant technical skills",
            "Optimize summary for job requirements"
        ]
        
        return SuggestionResponse(
            suggestions=suggestions,
            priority="medium",
            category="general"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/supported-formats")
async def get_supported_formats():
    """Get supported input and output formats"""
    return {
        "input_formats": [
            {
                "format": "pdf",
                "description": "Portable Document Format",
                "supported": True
            },
            {
                "format": "docx",
                "description": "Microsoft Word Document",
                "supported": True
            },
            {
                "format": "txt",
                "description": "Plain Text",
                "supported": True
            }
        ],
        "output_formats": [
            {
                "format": "pdf",
                "description": "Portable Document Format",
                "recommended": True
            },
            {
                "format": "docx",
                "description": "Microsoft Word Document",
                "recommended": False
            },
            {
                "format": "txt",
                "description": "Plain Text",
                "recommended": False
            }
        ]
    }


@router.get("/templates")
async def get_available_templates():
    """Get available CV templates"""
    return {
        "templates": [
            {
                "id": "modern",
                "name": "Modern Professional",
                "description": "Clean and contemporary design",
                "suitable_for": ["technology", "startups", "creative"],
                "features": ["ATS-friendly", "Clean layout", "Professional colors"]
            },
            {
                "id": "professional",
                "name": "Traditional Professional",
                "description": "Classic business format",
                "suitable_for": ["finance", "consulting", "corporate"],
                "features": ["Conservative design", "Traditional layout", "Business colors"]
            },
            {
                "id": "creative",
                "name": "Creative Modern",
                "description": "Bold and innovative design",
                "suitable_for": ["design", "marketing", "advertising"],
                "features": ["Creative layout", "Bold colors", "Unique styling"]
            }
        ]
    }


@router.get("/optimization-tips")
async def get_optimization_tips():
    """Get general CV optimization tips"""
    return {
        "tips": [
            {
                "category": "content",
                "tips": [
                    "Use action verbs to start bullet points",
                    "Quantify achievements with numbers and percentages",
                    "Tailor skills to match job requirements",
                    "Keep summary concise and impactful"
                ]
            },
            {
                "category": "formatting",
                "tips": [
                    "Use consistent formatting throughout",
                    "Keep it to 1-2 pages maximum",
                    "Use standard fonts (Arial, Times New Roman)",
                    "Ensure proper spacing and margins"
                ]
            },
            {
                "category": "ats",
                "tips": [
                    "Include relevant keywords from job description",
                    "Avoid graphics and complex formatting",
                    "Use standard section headings",
                    "Save as PDF for best compatibility"
                ]
            }
        ]
    }


@router.get("/skill-categories")
async def get_skill_categories():
    """Get predefined skill categories"""
    return {
        "categories": [
            {
                "name": "Programming Languages",
                "skills": ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin"]
            },
            {
                "name": "Web Technologies",
                "skills": ["HTML", "CSS", "React", "Vue.js", "Angular", "Node.js", "Django", "Flask", "Express"]
            },
            {
                "name": "Databases",
                "skills": ["SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "DynamoDB"]
            },
            {
                "name": "Cloud & DevOps",
                "skills": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Jenkins", "GitLab CI"]
            },
            {
                "name": "Data Science",
                "skills": ["Python", "R", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Tableau"]
            },
            {
                "name": "Soft Skills",
                "skills": ["Leadership", "Communication", "Problem Solving", "Teamwork", "Time Management", "Adaptability"]
            }
        ]
    }


@router.get("/industry-keywords")
async def get_industry_keywords():
    """Get industry-specific keywords"""
    return {
        "industries": [
            {
                "name": "Technology",
                "keywords": ["agile", "scrum", "sprint", "ci/cd", "microservices", "api", "cloud", "devops"]
            },
            {
                "name": "Finance",
                "keywords": ["risk management", "compliance", "regulatory", "financial modeling", "portfolio", "trading"]
            },
            {
                "name": "Healthcare",
                "keywords": ["hipaa", "clinical", "patient care", "medical", "healthcare", "compliance"]
            },
            {
                "name": "Marketing",
                "keywords": ["campaign", "analytics", "seo", "sem", "social media", "brand", "conversion"]
            }
        ]
    }


@router.get("/action-verbs")
async def get_action_verbs():
    """Get action verbs for CV bullet points"""
    return {
        "verbs": [
            {
                "category": "Leadership",
                "verbs": ["led", "managed", "directed", "supervised", "coordinated", "orchestrated"]
            },
            {
                "category": "Achievement",
                "verbs": ["achieved", "accomplished", "delivered", "exceeded", "improved", "optimized"]
            },
            {
                "category": "Development",
                "verbs": ["developed", "created", "built", "designed", "implemented", "architected"]
            },
            {
                "category": "Analysis",
                "verbs": ["analyzed", "researched", "investigated", "evaluated", "assessed", "examined"]
            },
            {
                "category": "Communication",
                "verbs": ["presented", "communicated", "collaborated", "facilitated", "negotiated", "advised"]
            }
        ]
    }


@router.get("/metrics")
async def get_optimization_metrics():
    """Get optimization metrics and scoring information"""
    return {
        "metrics": [
            {
                "name": "skill_match_score",
                "description": "Percentage of required skills matched",
                "weight": 0.4,
                "calculation": "Number of matched skills / Total required skills"
            },
            {
                "name": "experience_relevance_score",
                "description": "Relevance of work experience to job requirements",
                "weight": 0.3,
                "calculation": "Average relevance score of job experiences"
            },
            {
                "name": "keyword_match_score",
                "description": "Keyword density and distribution",
                "weight": 0.2,
                "calculation": "Number of matched keywords / Total job keywords"
            },
            {
                "name": "summary_optimization_score",
                "description": "Summary relevance and impact",
                "weight": 0.1,
                "calculation": "Keyword and skill matches in summary"
            }
        ],
        "scoring": {
            "excellent": "90-100",
            "good": "80-89",
            "average": "70-79",
            "needs_improvement": "60-69",
            "poor": "Below 60"
        }
    } 