#!/usr/bin/env python3
"""
Session 29: Environment Setup Verification Script
Checks all dependencies and configurations before starting the session
"""

import sys
import os
import subprocess
from pathlib import Path

def print_header(text):
    """Print section header"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)

def check_python_version():
    """Verify Python version"""
    print("\n🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} detected")
        print("   ⚠️  Python 3.10+ required")
        return False

def check_packages():
    """Verify required Python packages"""
    print("\n📦 Checking Python packages...")
    
    required_packages = [
        "openai",
        "promptlayer",
        "pandas",
        "numpy",
        "sklearn",
        "pytest",
        "loguru",
        "yaml"
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package:20s} - Installed")
        except ImportError:
            print(f"   ❌ {package:20s} - MISSING")
            all_installed = False
    
    return all_installed

def check_api_keys():
    """Verify API keys configuration"""
    print("\n🔑 Checking API keys...")
    
    # Load .env if it exists
    env_file = Path(".env")
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv()
        print("   ✅ .env file found")
    else:
        print("   ⚠️  .env file not found (using environment variables)")
    
    # Check OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY", "")
    if openai_key and openai_key.startswith("sk-"):
        print(f"   ✅ OpenAI API key configured: {openai_key[:10]}...{openai_key[-4:]}")
        openai_configured = True
    else:
        print("   ❌ OpenAI API key not configured")
        print("      Set in .env: OPENAI_API_KEY=sk-your-key-here")
        openai_configured = False
    
    # Check PromptLayer API key (optional)
    pl_key = os.getenv("PROMPTLAYER_API_KEY", "")
    if pl_key and pl_key.startswith("pl_"):
        print(f"   ✅ PromptLayer API key configured: {pl_key[:10]}...{pl_key[-4:]}")
    else:
        print("   ⚠️  PromptLayer API key not configured (optional)")
        print("      Get free key at: https://promptlayer.com")
    
    return openai_configured

def check_promptfoo():
    """Verify Promptfoo CLI installation"""
    print("\n🔧 Checking Promptfoo CLI...")
    
    try:
        result = subprocess.run(
            ["promptfoo", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✅ Promptfoo installed: version {version}")
            return True
        else:
            print("   ❌ Promptfoo not working properly")
            print("      Install: npm install -g promptfoo")
            return False
            
    except FileNotFoundError:
        print("   ❌ Promptfoo not found")
        print("      Install: npm install -g promptfoo")
        return False
    except subprocess.TimeoutExpired:
        print("   ⚠️  Promptfoo check timed out")
        return False
    except Exception as e:
        print(f"   ❌ Error checking Promptfoo: {str(e)}")
        return False

def check_directories():
    """Verify directory structure"""
    print("\n📁 Checking directory structure...")
    
    required_dirs = [
        "evaluation_outputs",
        "evaluation_outputs/static",
        "evaluation_outputs/dynamic",
        "evaluation_outputs/hybrid",
        "evaluation_outputs/ci_cd"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"   ✅ {dir_path}")
        else:
            print(f"   📝 Creating {dir_path}")
            path.mkdir(parents=True, exist_ok=True)
    
    return True

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🌐 Testing OpenAI API connection...")
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"   ✅ API connection successful")
        print(f"   📤 Test response: {result}")
        return True
        
    except Exception as e:
        print(f"   ❌ API connection failed: {str(e)}")
        print("      Check your OPENAI_API_KEY")
        return False

def main():
    """Run all verification checks"""
    print_header("SESSION 29: ENVIRONMENT SETUP VERIFICATION")
    
    checks = {
        "Python Version": check_python_version(),
        "Python Packages": check_packages(),
        "API Keys": check_api_keys(),
        "Promptfoo CLI": check_promptfoo(),
        "Directory Structure": check_directories()
    }
    
    # Only test API if key is configured
    if checks["API Keys"]:
        checks["OpenAI Connection"] = test_openai_connection()
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    print(f"\n📊 Checks passed: {passed}/{total}\n")
    
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"   {status} {check_name}")
    
    print("\n" + "="*80)
    
    if all(checks.values()):
        print("\n🎉 ALL CHECKS PASSED! You're ready to start Session 29!")
        print("\nNext steps:")
        print("   1. Open: Session_29_Advanced_LLM_Evaluation_CICD.ipynb")
        print("   2. Run: jupyter notebook")
        print("   3. Start learning!")
        print("\n" + "="*80)
        return 0
    else:
        print("\n⚠️  SOME CHECKS FAILED")
        print("\nPlease fix the issues above before starting the session.")
        print("\nNeed help? Check README.md or ask the instructor.")
        print("\n" + "="*80)
        return 1

if __name__ == "__main__":
    sys.exit(main())
