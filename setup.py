#!/usr/bin/env python3
"""
Setup script for MCQ Generator project
Automatically creates directory structure and setup files
"""

import os
import sys

def create_directory_structure():
    """Create the required directory structure"""
    directories = [
        'models',
        'services', 
        'static',
        'uploads',
        'outputs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Create __init__.py files for Python packages
    init_files = [
        'models/__init__.py',
        'services/__init__.py'
    ]
    
    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write("# This file makes the directory a Python package\n")
        print(f"✓ Created file: {init_file}")

def create_gitkeep_files():
    """Create .gitkeep files for empty directories"""
    gitkeep_dirs = ['uploads', 'outputs']
    
    for directory in gitkeep_dirs:
        gitkeep_path = os.path.join(directory, '.gitkeep')
        with open(gitkeep_path, 'w') as f:
            f.write("")
        print(f"✓ Created .gitkeep in: {directory}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python version {sys.version_info.major}.{sys.version_info.minor} is compatible")

def main():
    print("🚀 Setting up MCQ Generator project...\n")
    
    # Check Python version
    check_python_version()
    
    # Create directory structure
    print("\n📁 Creating directory structure...")
    create_directory_structure()
    
    # Create .gitkeep files
    print("\n📋 Creating .gitkeep files...")
    create_gitkeep_files()
    
    print("\n✅ Project setup complete!")
    print("\nNext steps:")
    print("1. Copy your .env.example to .env and add your Groq API key")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the application: python main.py")
    print("\n🎉 Happy coding!")

if __name__ == "__main__":
    main()