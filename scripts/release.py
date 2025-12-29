#!/usr/bin/env python3
"""
Release script for Equity Bank Risk Management System
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def get_current_version():
    """Get current version from VERSION file"""
    try:
        with open("VERSION", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"

def update_version(new_version):
    """Update version in VERSION file"""
    with open("VERSION", "w") as f:
        f.write(new_version)
    print(f"✅ Updated version to {new_version}")

def update_changelog(version, changes):
    """Update CHANGELOG.md with new version"""
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Read current changelog
    try:
        with open("CHANGELOG.md", "r") as f:
            content = f.read()
    except FileNotFoundError:
        content = "# Changelog\n\n"
    
    # Find insertion point (after the header)
    lines = content.split('\n')
    header_end = 0
    for i, line in enumerate(lines):
        if line.startswith('## ['):
            header_end = i
            break
    
    # Insert new version
    new_entry = f"""## [{version}] - {date}

### Changed
{changes}

"""
    
    if header_end > 0:
        lines.insert(header_end, new_entry)
    else:
        # No previous versions, add after header
        for i, line in enumerate(lines):
            if line.strip() == "":
                lines.insert(i + 1, new_entry)
                break
    
    # Write back
    with open("CHANGELOG.md", "w") as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Updated CHANGELOG.md")

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    
    # Quick tests
    result = run_command("python test_system.py --quick", "Running quick tests")
    if result is None:
        return False
    
    # Generate test data
    result = run_command("python test_data/generate_sample_data.py --count 100", "Generating test data")
    if result is None:
        return False
    
    # Test risk engine
    result = run_command("python risk_engine/main.py --once", "Testing risk engine")
    if result is None:
        return False
    
    print("✅ All tests passed")
    return True

def create_git_tag(version):
    """Create and push git tag"""
    tag_name = f"v{version}"
    
    # Create tag
    result = run_command(f"git tag -a {tag_name} -m 'Release {version}'", f"Creating tag {tag_name}")
    if result is None:
        return False
    
    # Push tag
    result = run_command(f"git push origin {tag_name}", f"Pushing tag {tag_name}")
    if result is None:
        return False
    
    return True

def build_package():
    """Build Python package"""
    print("📦 Building package...")
    
    # Clean previous builds
    run_command("rm -rf build/ dist/ *.egg-info/", "Cleaning previous builds")
    
    # Build package
    result = run_command("python -m build", "Building package")
    if result is None:
        return False
    
    # Check package
    result = run_command("twine check dist/*", "Checking package")
    if result is None:
        return False
    
    print("✅ Package built successfully")
    return True

def main():
    """Main release function"""
    parser = argparse.ArgumentParser(description="Release Equity Bank Risk Management System")
    parser.add_argument("version", help="New version number (e.g., 1.0.1)")
    parser.add_argument("--changes", help="Description of changes", default="Bug fixes and improvements")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--skip-build", action="store_true", help="Skip building package")
    parser.add_argument("--skip-git", action="store_true", help="Skip git operations")
    
    args = parser.parse_args()
    
    current_version = get_current_version()
    new_version = args.version
    
    print(f"🚀 Releasing Equity Bank Risk Management System")
    print(f"📊 Current version: {current_version}")
    print(f"🎯 New version: {new_version}")
    print("=" * 50)
    
    # Confirm release
    confirm = input(f"Are you sure you want to release version {new_version}? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ Release cancelled")
        return
    
    # Run tests
    if not args.skip_tests:
        if not run_tests():
            print("❌ Tests failed. Release cancelled.")
            return
    
    # Update version
    update_version(new_version)
    
    # Update changelog
    update_changelog(new_version, args.changes)
    
    # Git operations
    if not args.skip_git:
        # Add changes
        run_command("git add VERSION CHANGELOG.md", "Adding version changes")
        
        # Commit changes
        run_command(f"git commit -m 'Release version {new_version}'", "Committing changes")
        
        # Create and push tag
        if not create_git_tag(new_version):
            print("❌ Failed to create git tag")
            return
    
    # Build package
    if not args.skip_build:
        if not build_package():
            print("❌ Failed to build package")
            return
    
    print("🎉 Release completed successfully!")
    print(f"📦 Version {new_version} is ready")
    print("\nNext steps:")
    print("1. Push changes to GitHub: git push origin main")
    print("2. Create GitHub release with tag v" + new_version)
    print("3. Upload package to PyPI: twine upload dist/*")

if __name__ == "__main__":
    main()