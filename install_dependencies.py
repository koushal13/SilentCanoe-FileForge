#!/usr/bin/env python3
"""
SilentCanoe FileForge - Dependency Installation Script
Automatically installs all required dependencies for the application.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package using pip."""
    try:
        print(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Main installation function."""
    print("🚀 SilentCanoe FileForge - Dependency Installer")
    print("=" * 50)
    
    # Core dependencies
    dependencies = [
        # Image processing
        "Pillow>=10.0.0",
        "pillow-heif>=0.13.0",
        
        # Document processing
        "PyPDF2>=3.0.0",
        "beautifulsoup4>=4.12.0",
        "reportlab>=4.0.0",
        
        # Optional enhancements
        "python-docx>=1.1.0",
        "markdown>=3.5.0",
        "html2text>=2020.1.16"
    ]
    
    successful = 0
    failed = 0
    
    print("Installing core dependencies...")
    print("-" * 30)
    
    for package in dependencies:
        if install_package(package):
            successful += 1
        else:
            failed += 1
    
    print("\n" + "=" * 50)
    print("📊 Installation Summary:")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All dependencies installed successfully!")
        print("🚀 You can now run: python fileforge_converter.py")
    else:
        print(f"\n⚠️ {failed} package(s) failed to install.")
        print("📋 The application may still work with reduced functionality.")
        print("💡 Try installing failed packages manually.")
    
    print("\n🔧 Manual installation commands:")
    print("pip install -r requirements.txt")
    print("python fileforge_converter.py")

if __name__ == "__main__":
    main()