#!/usr/bin/env python3
"""
Verify Story 1.1: Repository Structure & Python Environment

This script checks that all requirements for Story 1.1 are met.
Run with: python scripts/verify_setup.py
"""

import os
import sys
from pathlib import Path


def check_directory(path: Path, name: str) -> bool:
    """Check if a directory exists."""
    exists = path.exists() and path.is_dir()
    status = "✅" if exists else "❌"
    print(f"{status} {name}: {path}")
    return exists


def check_file(path: Path, name: str) -> bool:
    """Check if a file exists."""
    exists = path.exists() and path.is_file()
    status = "✅" if exists else "❌"
    print(f"{status} {name}: {path}")
    return exists


def check_python_version() -> bool:
    """Check if Python version is 3.11+."""
    version = sys.version_info
    meets_requirement = version.major == 3 and version.minor >= 11
    status = "✅" if meets_requirement else "❌"
    print(f"{status} Python Version: {version.major}.{version.minor}.{version.micro} (requires 3.11+)")
    return meets_requirement


def check_dependencies() -> bool:
    """Check if required Python packages are installed."""
    required_packages = [
        'contentful',
        'frontmatter',
        'yaml',
        'requests',
        'pytest',
        'dotenv'
    ]
    
    all_installed = True
    print("\n📦 Checking Python Dependencies:")
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (not installed)")
            all_installed = False
    
    return all_installed


def main():
    """Main verification function."""
    print("=" * 70)
    print("Story 1.1: Repository Structure & Python Environment Verification")
    print("=" * 70)
    
    project_root = Path(__file__).parent.parent
    checks_passed = []
    
    # Check Python version
    print("\n🐍 Python Environment:")
    checks_passed.append(check_python_version())
    
    # Check directory structure
    print("\n📁 Directory Structure:")
    required_dirs = [
        (project_root / "scripts", "scripts/"),
        (project_root / "tests", "tests/"),
        (project_root / "_posts", "_posts/"),
        (project_root / "_posts" / "en", "_posts/en/"),
        (project_root / "_posts" / "es", "_posts/es/"),
        (project_root / "_data", "_data/"),
        (project_root / "_layouts", "_layouts/"),
        (project_root / "_includes", "_includes/"),
        (project_root / "_sass", "_sass/"),
        (project_root / "assets", "assets/"),
        (project_root / ".github" / "workflows", ".github/workflows/"),
    ]
    
    for path, name in required_dirs:
        checks_passed.append(check_directory(path, name))
    
    # Check required files
    print("\n📄 Required Files:")
    required_files = [
        (project_root / ".gitignore", ".gitignore"),
        (project_root / "scripts" / "requirements.txt", "scripts/requirements.txt"),
        (project_root / ".env.example", ".env.example"),
        (project_root / "_config.yml", "_config.yml"),
    ]
    
    for path, name in required_files:
        checks_passed.append(check_file(path, name))
    
    # Check .env (should exist but not required for this check)
    env_file = project_root / ".env"
    if env_file.exists():
        print(f"✅ .env file exists (credentials configured)")
    else:
        print(f"⚠️  .env file not found (copy from .env.example and add credentials)")
    
    # Check dependencies
    checks_passed.append(check_dependencies())
    
    # Check virtual environment
    print("\n🔧 Virtual Environment:")
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    if in_venv:
        print(f"✅ Running in virtual environment: {sys.prefix}")
    else:
        print(f"⚠️  Not running in virtual environment (recommended but not required)")
    
    # Summary
    print("\n" + "=" * 70)
    total_checks = len(checks_passed)
    passed_checks = sum(checks_passed)
    
    if passed_checks == total_checks:
        print(f"✅ ALL CHECKS PASSED ({passed_checks}/{total_checks})")
        print("\n🎉 Story 1.1 is COMPLETE!")
        print("\nNext step: Story 1.2 - Contentful Client with Caching")
        return 0
    else:
        print(f"❌ SOME CHECKS FAILED ({passed_checks}/{total_checks} passed)")
        print("\n⚠️  Please fix the issues above before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
