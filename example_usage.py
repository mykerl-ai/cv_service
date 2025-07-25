#!/usr/bin/env python3
"""
Example usage of the CV Tailoring Service

This script demonstrates how to use the CV tailoring service to generate
tailored CVs in PDF format using OpenAI.
"""

import os
import sys
import json
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, continue without it
    pass

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent / "src"))

from generate_tailored_cv import CVTailoringService


def example_from_scratch():
    """Example: Generate CV from scratch using personal information"""
    print("=== Example: Generate CV from Scratch ===\n")
    
    # Your OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set your OpenAI API key as an environment variable:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Initialize the service
    service = CVTailoringService(api_key)
    
    # Sample personal information
    personal_info = {
        "full_name": "Sarah Johnson",
        "email": "sarah.johnson@email.com",
        "phone": "+1 (555) 987-6543",
        "location": "New York, NY",
        "linkedin": "linkedin.com/in/sarahjohnson",
        "github": "github.com/sarahjohnson",
        "portfolio": "sarahjohnson.dev",
        "summary": "Passionate data scientist with 4+ years of experience in machine learning, statistical analysis, and data engineering. Proven track record of delivering insights that drive business decisions and improve operational efficiency.",
        "technical_skills": [
            "Python", "R", "SQL", "Machine Learning", "Deep Learning",
            "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
            "AWS", "Docker", "Git", "Jupyter", "Tableau", "Power BI"
        ],
        "soft_skills": [
            "Data Analysis", "Problem Solving", "Communication",
            "Project Management", "Team Collaboration", "Critical Thinking"
        ],
        "experience": [
            {
                "company": "DataCorp Analytics",
                "position": "Senior Data Scientist",
                "start_date": "March 2021",
                "end_date": "Present",
                "description": [
                    "Lead machine learning projects for predictive analytics",
                    "Develop and deploy ML models in production environments",
                    "Collaborate with business stakeholders to define requirements"
                ],
                "achievements": [
                    "Improved prediction accuracy by 25% using ensemble methods",
                    "Reduced model training time by 40% through optimization",
                    "Led team of 3 data scientists in successful project delivery"
                ]
            },
            {
                "company": "TechStart Inc.",
                "position": "Data Analyst",
                "start_date": "June 2019",
                "end_date": "February 2021",
                "description": [
                    "Analyzed large datasets to extract actionable insights",
                    "Created dashboards and reports for stakeholders",
                    "Performed statistical analysis and hypothesis testing"
                ],
                "achievements": [
                    "Identified cost-saving opportunities worth $500K annually",
                    "Automated reporting processes saving 20 hours per week",
                    "Improved data quality by implementing validation rules"
                ]
            }
        ],
        "education": [
            {
                "institution": "University of Data Science",
                "degree": "Master of Science",
                "field_of_study": "Data Science",
                "graduation_date": "May 2019",
                "gpa": "3.9/4.0"
            },
            {
                "institution": "State University",
                "degree": "Bachelor of Science",
                "field_of_study": "Statistics",
                "graduation_date": "May 2017",
                "gpa": "3.8/4.0"
            }
        ]
    }
    
    # Sample job description
    job_description = """
    Senior Data Scientist - Machine Learning
    
    Company: AI Innovations Corp
    Location: New York, NY (Hybrid)
    
    We are seeking a Senior Data Scientist to join our AI team. You will be responsible for developing and deploying machine learning models, conducting advanced analytics, and driving data-driven insights.
    
    Key Responsibilities:
    - Develop and implement machine learning models for predictive analytics
    - Conduct statistical analysis and hypothesis testing
    - Collaborate with engineering teams to deploy ML models
    - Analyze large datasets to extract actionable insights
    - Present findings to stakeholders and business leaders
    
    Required Skills:
    - 4+ years of experience in data science or machine learning
    - Strong proficiency in Python, R, and SQL
    - Experience with machine learning frameworks (TensorFlow, PyTorch)
    - Knowledge of statistical analysis and hypothesis testing
    - Experience with data visualization tools (Tableau, Power BI)
    - Strong understanding of ML model deployment and production systems
    
    Preferred Skills:
    - Experience with deep learning and neural networks
    - Knowledge of cloud platforms (AWS, Azure, GCP)
    - Experience with big data technologies (Spark, Hadoop)
    - Background in A/B testing and experimental design
    """
    
    # Generate the CV
    print("Generating CV from scratch...")
    results = service.generate_cv_from_scratch(
        personal_info=personal_info,
        job_description=job_description,
        output_path="sarah_johnson_tailored_cv.pdf",
        template_style="modern"
    )
    
    # Display results
    if results["success"]:
        print(f"\n✅ CV generated successfully!")
        print(f"📄 Output file: {results['output_file']}")
        print(f"📊 Optimization score: {results['optimization_score']:.1f}%")
        print(f"🎯 Job: {results['job_title']} at {results['company_name']}")
    else:
        print(f"\n❌ Error: {results['error']}")


def example_with_existing_cv():
    """Example: Tailor an existing CV"""
    print("\n=== Example: Tailor Existing CV ===\n")
    
    # Your OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set your OpenAI API key as an environment variable:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Initialize the service
    service = CVTailoringService(api_key)
    
    # Check if sample CV file exists
    cv_file_path = "sample_cv.pdf"  # You would need to provide your own CV file
    if not os.path.exists(cv_file_path):
        print(f"CV file not found: {cv_file_path}")
        print("Please provide a CV file (PDF, DOCX, or TXT) to use this example.")
        return
    
    # Sample job description
    job_description = """
    Full Stack Developer - React & Node.js
    
    Company: WebTech Solutions
    Location: Remote
    
    We are looking for a Full Stack Developer to join our team. You will be responsible for building and maintaining web applications using modern technologies.
    
    Required Skills:
    - 3+ years of experience in full-stack development
    - Strong proficiency in JavaScript, React, and Node.js
    - Experience with databases (PostgreSQL, MongoDB)
    - Knowledge of RESTful APIs and GraphQL
    - Experience with cloud platforms (AWS, Azure)
    
    Preferred Skills:
    - Experience with TypeScript
    - Knowledge of Docker and containerization
    - Experience with CI/CD pipelines
    - Background in agile development
    """
    
    # Generate the tailored CV
    print("Tailoring existing CV...")
    results = service.generate_tailored_cv(
        cv_file_path=cv_file_path,
        job_description=job_description,
        output_path="tailored_cv.pdf",
        template_style="professional",
        include_analysis=True
    )
    
    # Display results
    if results["success"]:
        print(f"\n✅ CV tailored successfully!")
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
    else:
        print(f"\n❌ Error: {results['error']}")


def main():
    """Main function to run examples"""
    print("CV Tailoring Service - Example Usage")
    print("=" * 50)
    
    # Run examples
    example_from_scratch()
    example_with_existing_cv()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nTo use the command-line interface:")
    print("python generate_tailored_cv.py --help")


if __name__ == "__main__":
    main() 