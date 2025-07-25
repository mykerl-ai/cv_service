#!/usr/bin/env python3
"""
Test script to verify CV Tailoring Service deployment
"""

import requests
import json
import os
from pathlib import Path

def test_deployment(base_url: str):
    """Test the deployed service"""
    print(f"🧪 Testing deployment at: {base_url}")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: Templates endpoint
    print("\n3. Testing templates endpoint...")
    try:
        response = requests.get(f"{base_url}/api/v1/templates", timeout=10)
        if response.status_code == 200:
            print("✅ Templates endpoint working")
            templates = response.json()
            print(f"   Available templates: {len(templates.get('templates', []))}")
        else:
            print(f"❌ Templates endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Templates endpoint error: {e}")
    
    # Test 4: Formats endpoint
    print("\n4. Testing formats endpoint...")
    try:
        response = requests.get(f"{base_url}/api/v1/formats", timeout=10)
        if response.status_code == 200:
            print("✅ Formats endpoint working")
            formats = response.json()
            print(f"   Available formats: {len(formats.get('formats', []))}")
        else:
            print(f"❌ Formats endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Formats endpoint error: {e}")
    
    # Test 5: Job analysis (without API key)
    print("\n5. Testing job analysis (will fail without API key)...")
    try:
        test_job = {
            "job_description": "Senior Software Engineer position requiring Python and JavaScript experience."
        }
        response = requests.post(
            f"{base_url}/api/v1/analyze-job",
            json=test_job,
            timeout=30
        )
        if response.status_code == 500:
            print("✅ Job analysis endpoint responding (expected error without API key)")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Job analysis endpoint error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Deployment test completed!")
    print("\n📋 Next steps:")
    print("1. Set your OPENAI_API_KEY environment variable in Render")
    print("2. Test with actual CV files and job descriptions")
    print("3. Check the API documentation at /docs")
    
    return True

def main():
    """Main function"""
    print("🚀 CV Tailoring Service - Deployment Test")
    print("=" * 50)
    
    # Get base URL from user or environment
    base_url = os.getenv("CV_SERVICE_URL")
    if not base_url:
        base_url = input("Enter your service URL (e.g., https://your-service.onrender.com): ").strip()
    
    if not base_url:
        print("❌ No service URL provided")
        return
    
    # Remove trailing slash
    base_url = base_url.rstrip('/')
    
    # Run tests
    test_deployment(base_url)

if __name__ == "__main__":
    main() 