#!/usr/bin/env python3
"""
API Client for CV Tailoring Service

This client can be used to test the deployed service on Render.
"""

import requests
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


class CVTailoringClient:
    """Client for interacting with the CV Tailoring Service API"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the client
        
        Args:
            base_url: Base URL of the deployed service (e.g., https://your-service.onrender.com)
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the service is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "unhealthy"}
    
    def get_templates(self) -> Dict[str, Any]:
        """Get available CV templates"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/templates")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def get_formats(self) -> Dict[str, Any]:
        """Get available output formats"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/formats")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def analyze_job(self, job_description: str) -> Dict[str, Any]:
        """
        Analyze a job description
        
        Args:
            job_description: Job description text
            
        Returns:
            Analysis results
        """
        try:
            data = {"job_description": job_description}
            response = self.session.post(
                f"{self.base_url}/api/v1/analyze-job",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def optimize_cv(
        self,
        cv_file_path: str,
        job_description: str,
        output_format: str = "pdf",
        template_style: str = "modern"
    ) -> Dict[str, Any]:
        """
        Optimize a CV for a job description
        
        Args:
            cv_file_path: Path to the CV file
            job_description: Job description text
            output_format: Output format (pdf, docx, txt)
            template_style: Template style (modern, professional, creative)
            
        Returns:
            Optimization results
        """
        try:
            # Check if file exists
            if not os.path.exists(cv_file_path):
                return {"error": f"File not found: {cv_file_path}"}
            
            # Prepare the request
            with open(cv_file_path, 'rb') as f:
                files = {'cv_file': (os.path.basename(cv_file_path), f, 'application/octet-stream')}
                data = {
                    'job_description': job_description,
                    'output_format': output_format,
                    'template_style': template_style
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/v1/optimize-cv",
                    files=files,
                    data=data
                )
                response.raise_for_status()
                return response.json()
                
        except requests.RequestException as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def download_file(self, filename: str, output_path: str) -> bool:
        """
        Download a generated file
        
        Args:
            filename: Name of the file to download
            output_path: Local path to save the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.session.get(f"{self.base_url}/api/v1/download/{filename}")
            response.raise_for_status()
            
            # Save the file
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return True
            
        except requests.RequestException as e:
            print(f"Error downloading file: {e}")
            return False
    
    def get_api_docs(self) -> str:
        """Get the API documentation URL"""
        return f"{self.base_url}/docs"


def main():
    """Example usage of the API client"""
    
    # Configuration
    BASE_URL = os.getenv("CV_SERVICE_URL", "http://localhost:8000")
    
    print("🚀 CV Tailoring Service API Client")
    print("=" * 50)
    
    # Initialize client
    client = CVTailoringClient(BASE_URL)
    
    # Health check
    print("🔍 Checking service health...")
    health = client.health_check()
    if "error" in health:
        print(f"❌ Service is not healthy: {health['error']}")
        return
    else:
        print("✅ Service is healthy!")
    
    # Get available templates
    print("\n📋 Getting available templates...")
    templates = client.get_templates()
    if "error" not in templates:
        print("Available templates:")
        for template in templates.get("templates", []):
            print(f"  • {template['name']}: {template['description']}")
    
    # Get available formats
    print("\n📄 Getting available formats...")
    formats = client.get_formats()
    if "error" not in formats:
        print("Available formats:")
        for fmt in formats.get("formats", []):
            print(f"  • {fmt['name']}: {fmt['description']}")
    
    # Example job description
    job_description = """
    Senior Software Engineer - Full Stack Development
    
    We are looking for a Senior Software Engineer to join our team. 
    Requirements include:
    - 5+ years of experience in Python, JavaScript, and React
    - Experience with cloud platforms (AWS, Azure, or GCP)
    - Knowledge of databases (PostgreSQL, MongoDB)
    - Experience with CI/CD pipelines
    - Strong problem-solving skills
    """
    
    # Analyze job
    print("\n🎯 Analyzing job description...")
    analysis = client.analyze_job(job_description)
    if "error" not in analysis:
        print(f"Job Title: {analysis.get('job_title', 'N/A')}")
        print(f"Company: {analysis.get('company_name', 'N/A')}")
        print(f"Required Skills: {', '.join(analysis.get('required_skills', []))}")
        print(f"Preferred Skills: {', '.join(analysis.get('preferred_skills', []))}")
    else:
        print(f"❌ Error analyzing job: {analysis['error']}")
    
    # Example CV optimization (if CV file exists)
    cv_file = "sample_cv.pdf"  # Replace with actual CV file path
    if os.path.exists(cv_file):
        print(f"\n📝 Optimizing CV: {cv_file}")
        result = client.optimize_cv(
            cv_file_path=cv_file,
            job_description=job_description,
            output_format="pdf",
            template_style="modern"
        )
        
        if "error" not in result:
            print(f"✅ Optimization successful!")
            print(f"Optimization Score: {result.get('optimization_score', 'N/A')}%")
            print(f"Output File: {result.get('output_file_path', 'N/A')}")
            
            # Download the optimized CV
            if result.get('output_file_path'):
                filename = os.path.basename(result['output_file_path'])
                output_path = f"optimized_{filename}"
                if client.download_file(filename, output_path):
                    print(f"📥 Downloaded optimized CV to: {output_path}")
                else:
                    print("❌ Failed to download optimized CV")
        else:
            print(f"❌ Error optimizing CV: {result['error']}")
    else:
        print(f"\n⚠️  CV file not found: {cv_file}")
        print("   To test CV optimization, place a CV file in the current directory")
    
    # API documentation
    print(f"\n📚 API Documentation: {client.get_api_docs()}")
    print("\n🎉 API client test completed!")


if __name__ == "__main__":
    main() 