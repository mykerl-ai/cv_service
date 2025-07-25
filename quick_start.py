#!/usr/bin/env python3
"""
Quick Start Script for CV Tailoring Service

This script provides a simple way to test the CV tailoring service
with minimal setup and sample data.
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

def check_setup():
    """Check if the environment is properly set up"""
    print("🔍 Checking setup...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OpenAI API key not found")
        print("Please set your API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    # Check if required files exist
    required_files = [
        "src/core/cv_analyzer.py",
        "src/core/job_analyzer.py", 
        "src/core/cv_optimizer.py",
        "src/core/cv_generator.py",
        "sample_personal_info.json",
        "sample_job_description.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ Setup looks good!")
    return True


def quick_demo():
    """Run a quick demonstration"""
    print("\n🚀 Starting Quick Demo...")
    
    try:
        from generate_tailored_cv import CVTailoringService
        
        # Initialize service
        api_key = os.getenv("OPENAI_API_KEY")
        service = CVTailoringService(api_key)
        
        # Load sample data
        print("📄 Loading sample data...")
        
        with open("sample_personal_info.json", "r") as f:
            personal_info = json.load(f)
        
        with open("sample_job_description.txt", "r") as f:
            job_description = f.read()
        
        # Generate CV from scratch
        print("🎯 Generating tailored CV...")
        results = service.generate_cv_from_scratch(
            personal_info=personal_info,
            job_description=job_description,
            output_path="demo_cv.pdf",
            template_style="modern"
        )
        
        # Display results
        if results["success"]:
            print("\n🎉 Demo completed successfully!")
            print(f"📄 Generated CV: {results['output_file']}")
            print(f"📊 Optimization score: {results['optimization_score']:.1f}%")
            print(f"🎯 Job: {results['job_title']} at {results['company_name']}")
            
            print("\n📋 Next steps:")
            print("1. Open the generated PDF to see your tailored CV")
            print("2. Try different templates: --template professional or --template creative")
            print("3. Use your own data: --cv-file your_cv.pdf or --personal-info your_info.json")
            print("4. Get detailed analysis: --include-analysis")
            
        else:
            print(f"\n❌ Demo failed: {results['error']}")
            return False
            
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        return False
    
    return True


def show_usage_examples():
    """Show usage examples"""
    print("\n📚 Usage Examples:")
    print("=" * 50)
    
    print("\n1. Generate CV from scratch:")
    print("python generate_tailored_cv.py \\")
    print("  --from-scratch \\")
    print("  --personal-info sample_personal_info.json \\")
    print("  --job-description \"$(cat sample_job_description.txt)\" \\")
    print("  --output my_cv.pdf \\")
    print("  --template modern")
    
    print("\n2. Tailor existing CV:")
    print("python generate_tailored_cv.py \\")
    print("  --cv-file your_cv.pdf \\")
    print("  --job-description \"Job description text...\" \\")
    print("  --output tailored_cv.pdf \\")
    print("  --template professional \\")
    print("  --include-analysis")
    
    print("\n3. Run example script:")
    print("python example_usage.py")
    
    print("\n4. Get help:")
    print("python generate_tailored_cv.py --help")


def main():
    """Main function"""
    print("🎯 CV Tailoring Service - Quick Start")
    print("=" * 50)
    
    # Check setup
    if not check_setup():
        print("\n❌ Setup incomplete. Please fix the issues above and try again.")
        return
    
    # Run demo
    if quick_demo():
        show_usage_examples()
    else:
        print("\n❌ Demo failed. Please check the error messages above.")


if __name__ == "__main__":
    main() 