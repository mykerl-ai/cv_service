#!/usr/bin/env python3
"""
Setup script to create .env file for CV Tailoring Service
"""

import os
from pathlib import Path

def create_env_file():
    """Create .env file with user input"""
    print("🔧 CV Tailoring Service - Environment Setup")
    print("=" * 50)
    
    # Check if .env already exists
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️  .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    # Get OpenAI API key
    print("\n📝 Please enter your OpenAI API key:")
    print("You can find it at: https://platform.openai.com/api-keys")
    api_key = input("OpenAI API Key: ").strip()
    
    if not api_key:
        print("❌ API key is required!")
        return
    
    # Create .env content
    env_content = f"""# OpenAI API Configuration
OPENAI_API_KEY={api_key}

# Optional: Service Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Optional: File Processing Limits
MAX_FILE_SIZE=10485760  # 10MB in bytes

# Optional: Logging
LOG_LEVEL=INFO
"""
    
    # Write .env file
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"\n✅ .env file created successfully!")
        print(f"📄 File location: {env_file.absolute()}")
        print("\n🔒 Security note: Make sure to add .env to your .gitignore file")
        
        # Check if .gitignore exists and add .env if needed
        gitignore_file = Path(".gitignore")
        if gitignore_file.exists():
            with open(gitignore_file, 'r') as f:
                content = f.read()
            if ".env" not in content:
                with open(gitignore_file, 'a') as f:
                    f.write("\n# Environment variables\n.env\n")
                print("✅ Added .env to .gitignore")
        else:
            with open(gitignore_file, 'w') as f:
                f.write("# Environment variables\n.env\n")
            print("✅ Created .gitignore and added .env")
        
        print("\n🚀 You're ready to go! Run:")
        print("   python quick_start.py")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def check_env_setup():
    """Check if environment is properly set up"""
    print("🔍 Checking environment setup...")
    
    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("Run: python setup_env.py")
        return False
    
    # Check if python-dotenv is installed
    try:
        import dotenv
        print("✅ python-dotenv is installed")
    except ImportError:
        print("⚠️  python-dotenv not installed (optional)")
        print("Install with: pip install python-dotenv")
    
    # Check if OpenAI API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ OpenAI API key is configured")
        return True
    else:
        print("❌ OpenAI API key not found in .env file")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_env_setup()
    else:
        create_env_file() 