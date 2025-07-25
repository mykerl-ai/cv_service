#!/usr/bin/env python3
"""
CV Tailoring Script - Generate tailored CV in PDF format using OpenAI

This script uses the existing CV writer service to:
1. Parse an existing CV
2. Analyze a job description
3. Optimize the CV for the specific job
4. Generate a tailored PDF CV

Usage:
    python generate_tailored_cv.py --cv-file path/to/cv.pdf --job-description "job description text" --output output_cv.pdf
"""

import os
import sys
import argparse
import logging
import tempfile
from pathlib import Path
from typing import Optional
import json

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, continue without it
    pass

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.cv_analyzer import CVAnalyzer
from src.core.job_analyzer import JobAnalyzer
from src.core.cv_optimizer import CVOptimizer
from src.core.cv_generator import CVGenerator
from src.utils.file_processor import FileProcessor
from src.models.cv_data import CVData
from src.models.job_data import JobAnalysisResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CVTailoringService:
    """Main service for CV tailoring"""
    
    def __init__(self, openai_api_key: str):
        """Initialize the CV tailoring service"""
        self.openai_api_key = openai_api_key
        
        # Initialize components
        self.cv_analyzer = CVAnalyzer(openai_api_key)
        self.job_analyzer = JobAnalyzer(openai_api_key)
        self.cv_optimizer = CVOptimizer(openai_api_key)
        self.cv_generator = CVGenerator()
        self.file_processor = FileProcessor()
    
    def generate_tailored_cv(
        self,
        cv_file_path: str,
        job_description: str,
        output_path: str,
        template_style: str = "modern",
        include_analysis: bool = True
    ) -> dict:
        """
        Generate a tailored CV in PDF format
        
        Args:
            cv_file_path: Path to the input CV file
            job_description: Job description text
            output_path: Path for the output PDF
            template_style: CV template style (modern, professional, creative)
            include_analysis: Whether to include analysis report
            
        Returns:
            Dictionary with results and metadata
        """
        try:
            logger.info("Starting CV tailoring process...")
            
            # Step 1: Validate input file
            logger.info("Validating input CV file...")
            is_valid, error_message = self.file_processor.validate_file(cv_file_path)
            if not is_valid:
                raise ValueError(f"Invalid CV file: {error_message}")
            
            # Step 2: Parse CV
            logger.info("Parsing CV file...")
            cv_data = self.cv_analyzer.parse_cv(cv_file_path)
            logger.info(f"Parsed CV for: {cv_data.contact_info.full_name}")
            
            # Step 3: Analyze job description
            logger.info("Analyzing job description...")
            job_analysis = self.job_analyzer.analyze_job_description(job_description)
            logger.info(f"Analyzed job: {job_analysis.job_description.title} at {job_analysis.job_description.company.name}")
            
            # Step 4: Optimize CV
            logger.info("Optimizing CV for job requirements...")
            optimization_result = self.cv_optimizer.optimize_cv(cv_data, job_analysis)
            logger.info(f"Optimization score: {optimization_result.optimization_score:.1f}%")
            
            # Step 5: Generate PDF
            logger.info("Generating PDF CV...")
            self.cv_generator.template_style = template_style
            pdf_path = self.cv_generator.generate_pdf(optimization_result.optimized_cv, output_path)
            
            # Step 6: Prepare results
            results = {
                "success": True,
                "output_file": pdf_path,
                "optimization_score": optimization_result.optimization_score,
                "improvements_made": optimization_result.improvements_made,
                "skill_gaps_identified": optimization_result.skill_gaps_identified,
                "processing_time": optimization_result.processing_time,
                "job_title": job_analysis.job_description.title,
                "company_name": job_analysis.job_description.company.name,
                "template_style": template_style
            }
            
            # Include detailed analysis if requested
            if include_analysis:
                results["detailed_analysis"] = {
                    "cv_strengths": self.cv_analyzer.analyze_cv_strengths(cv_data),
                    "job_requirements": {
                        "required_skills": [s.skill_name for s in job_analysis.job_description.required_skills],
                        "preferred_skills": [s.skill_name for s in job_analysis.job_description.preferred_skills],
                        "experience_level": job_analysis.job_description.experience_level,
                        "keywords": job_analysis.job_description.keywords
                    },
                    "keyword_matches": optimization_result.keyword_matches,
                    "suggestions": job_analysis.suggestions
                }
            
            logger.info("CV tailoring completed successfully!")
            return results
            
        except Exception as e:
            logger.error(f"Error in CV tailoring process: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "output_file": None
            }
    
    def generate_cv_from_scratch(
        self,
        personal_info: dict,
        job_description: str,
        output_path: str,
        template_style: str = "modern"
    ) -> dict:
        """
        Generate a CV from scratch using personal information and job description
        
        Args:
            personal_info: Dictionary with personal information
            job_description: Job description text
            output_path: Path for the output PDF
            template_style: CV template style
            
        Returns:
            Dictionary with results
        """
        try:
            logger.info("Generating CV from scratch...")
            
            # Create CV data from personal info
            cv_data = self._create_cv_from_personal_info(personal_info)
            
            # Analyze job description
            job_analysis = self.job_analyzer.analyze_job_description(job_description)
            
            # Optimize CV
            optimization_result = self.cv_optimizer.optimize_cv(cv_data, job_analysis)
            
            # Generate PDF
            self.cv_generator.template_style = template_style
            pdf_path = self.cv_generator.generate_pdf(optimization_result.optimized_cv, output_path)
            
            return {
                "success": True,
                "output_file": pdf_path,
                "optimization_score": optimization_result.optimization_score,
                "job_title": job_analysis.job_description.title,
                "company_name": job_analysis.job_description.company.name
            }
            
        except Exception as e:
            logger.error(f"Error generating CV from scratch: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "output_file": None
            }
    
    def _create_cv_from_personal_info(self, personal_info: dict) -> CVData:
        """Create CV data from personal information"""
        from src.models.cv_data import ContactInfo, Skill, EmploymentDetail, Education
        
        cv_data = CVData()
        
        # Contact info
        cv_data.contact_info = ContactInfo(
            full_name=personal_info.get("full_name", ""),
            email=personal_info.get("email", ""),
            phone=personal_info.get("phone", ""),
            location=personal_info.get("location", ""),
            linkedin=personal_info.get("linkedin", ""),
            github=personal_info.get("github", ""),
            portfolio=personal_info.get("portfolio", "")
        )
        
        # Summary
        cv_data.summary = personal_info.get("summary", "")
        
        # Skills
        for skill_name in personal_info.get("technical_skills", []):
            skill = Skill(name=skill_name, category="technical", proficiency="intermediate")
            cv_data.technical_skills.append(skill)
        
        for skill_name in personal_info.get("soft_skills", []):
            skill = Skill(name=skill_name, category="soft", proficiency="intermediate")
            cv_data.soft_skills.append(skill)
        
        # Experience
        for exp in personal_info.get("experience", []):
            employment = EmploymentDetail(
                company=exp.get("company", ""),
                position=exp.get("position", ""),
                start_date=exp.get("start_date", ""),
                end_date=exp.get("end_date", ""),
                description=exp.get("description", []),
                achievements=exp.get("achievements", [])
            )
            cv_data.employment_history.append(employment)
        
        # Education
        for edu in personal_info.get("education", []):
            education = Education(
                institution=edu.get("institution", ""),
                degree=edu.get("degree", ""),
                field_of_study=edu.get("field_of_study", ""),
                graduation_date=edu.get("graduation_date", "")
            )
            cv_data.education.append(education)
        
        return cv_data


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="Generate tailored CV in PDF format")
    parser.add_argument("--cv-file", help="Path to input CV file (PDF, DOCX, TXT)")
    parser.add_argument("--job-description", required=True, help="Job description text")
    parser.add_argument("--output", required=True, help="Output PDF file path")
    parser.add_argument("--template", default="modern", choices=["modern", "professional", "creative"], 
                       help="CV template style")
    parser.add_argument("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--include-analysis", action="store_true", help="Include detailed analysis in output")
    parser.add_argument("--from-scratch", action="store_true", help="Generate CV from personal info instead of file")
    parser.add_argument("--personal-info", help="JSON file with personal information (for from-scratch mode)")
    
    args = parser.parse_args()
    
    # Get OpenAI API key
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OpenAI API key is required. Set OPENAI_API_KEY environment variable or use --api-key")
        sys.exit(1)
    
    # Initialize service
    service = CVTailoringService(api_key)
    
    try:
        if args.from_scratch:
            # Generate CV from scratch
            if not args.personal_info:
                print("Error: --personal-info is required when using --from-scratch")
                sys.exit(1)
            
            with open(args.personal_info, 'r') as f:
                personal_info = json.load(f)
            
            results = service.generate_cv_from_scratch(
                personal_info=personal_info,
                job_description=args.job_description,
                output_path=args.output,
                template_style=args.template
            )
        else:
            # Generate CV from existing file
            if not args.cv_file:
                print("Error: --cv-file is required when not using --from-scratch")
                sys.exit(1)
            
            results = service.generate_tailored_cv(
                cv_file_path=args.cv_file,
                job_description=args.job_description,
                output_path=args.output,
                template_style=args.template,
                include_analysis=args.include_analysis
            )
        
        # Display results
        if results["success"]:
            print(f"\n✅ CV generated successfully!")
            print(f"📄 Output file: {results['output_file']}")
            print(f"📊 Optimization score: {results['optimization_score']:.1f}%")
            print(f"🎯 Job: {results['job_title']} at {results['company_name']}")
            print(f"⏱️  Processing time: {results['processing_time']:.2f} seconds")
            
            if results.get("improvements_made"):
                print(f"\n🔧 Improvements made:")
                for improvement in results["improvements_made"]:
                    print(f"   • {improvement}")
            
            if results.get("skill_gaps_identified"):
                print(f"\n⚠️  Skill gaps identified:")
                for gap in results["skill_gaps_identified"]:
                    print(f"   • {gap}")
            
            if args.include_analysis and results.get("detailed_analysis"):
                print(f"\n📋 Detailed Analysis:")
                analysis = results["detailed_analysis"]
                print(f"   Required skills: {', '.join(analysis['job_requirements']['required_skills'])}")
                print(f"   Preferred skills: {', '.join(analysis['job_requirements']['preferred_skills'])}")
                print(f"   Experience level: {analysis['job_requirements']['experience_level']}")
                
        else:
            print(f"\n❌ Error generating CV: {results['error']}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 