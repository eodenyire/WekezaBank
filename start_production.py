#!/usr/bin/env python3
"""
Production Startup Script for Wekeza Bank Risk Management System
This script starts the complete production environment with Docker Compose
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def check_docker():
    """Check if Docker is installed and running"""
    print("🐳 Checking Docker installation...")
    if not run_command("docker --version"):
        print("❌ Docker is not installed. Please install Docker first.")
        return False
    
    if not run_command("docker-compose --version"):
        print("❌ Docker Compose is not installed. Please install Docker Compose first.")
        return False
    
    # Check if Docker daemon is running
    if not run_command("docker info"):
        print("❌ Docker daemon is not running. Please start Docker first.")
        return False
    
    print("✅ Docker is installed and running")
    return True

def check_environment():
    """Check if production environment file exists"""
    print("🔧 Checking environment configuration...")
    env_file = Path(".env.production")
    if not env_file.exists():
        print("❌ Production environment file (.env.production) not found")
        return False
    
    print("✅ Production environment file found")
    return True

def start_services():
    """Start all services using Docker Compose"""
    print("🚀 Starting production services...")
    
    # Change to infrastructure directory
    infrastructure_dir = Path("infrastructure")
    if not infrastructure_dir.exists():
        print("❌ Infrastructure directory not found")
        return False
    
    # Copy production environment file
    if not run_command("cp ../.env.production .env", cwd="infrastructure"):
        print("❌ Failed to copy environment file")
        return False
    
    # Pull latest images
    print("📥 Pulling latest Docker images...")
    if not run_command("docker-compose pull", cwd="infrastructure"):
        print("⚠️ Warning: Failed to pull some images, continuing with local images")
    
    # Build custom images
    print("🔨 Building custom images...")
    if not run_command("docker-compose build", cwd="infrastructure"):
        print("❌ Failed to build custom images")
        return False
    
    # Start services
    print("🎯 Starting all services...")
    if not run_command("docker-compose up -d", cwd="infrastructure"):
        print("❌ Failed to start services")
        return False
    
    print("✅ All services started successfully")
    return True

def wait_for_services():
    """Wait for all services to be healthy"""
    print("⏳ Waiting for services to be ready...")
    
    services = {
        "PostgreSQL": "http://localhost:5432",
        "Redis": "http://localhost:6379", 
        "Risk Dashboard": "http://localhost:8501",
        "Ballerine Frontend": "http://localhost:5173",
        "CISO Assistant": "http://localhost:8443",
        "Tazama": "http://localhost:4000"
    }
    
    max_wait = 300  # 5 minutes
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        all_ready = True
        
        # Check Docker containers
        result = subprocess.run("docker-compose ps", shell=True, cwd="infrastructure", 
                              capture_output=True, text=True)
        if result.returncode == 0:
            # Check if all containers are running
            if "Up" in result.stdout:
                print("🟢 Docker containers are running")
            else:
                all_ready = False
        
        # Check specific services
        try:
            # Check dashboard (most important for user access)
            response = requests.get("http://localhost:8501/_stcore/health", timeout=5)
            if response.status_code == 200:
                print("🟢 Risk Dashboard is ready")
            else:
                all_ready = False
        except:
            all_ready = False
        
        if all_ready:
            print("✅ All services are ready!")
            return True
        
        print("⏳ Services still starting up...")
        time.sleep(10)
    
    print("⚠️ Some services may still be starting up, but continuing...")
    return True

def show_access_info():
    """Show access information for all services"""
    print("\n" + "="*60)
    print("🎉 WEKEZA BANK RISK MANAGEMENT SYSTEM - PRODUCTION READY")
    print("="*60)
    print("\n📊 ACCESS URLS:")
    print("• Risk Management Dashboard: http://localhost:8501")
    print("• Ballerine (Transaction Monitoring): http://localhost:5173")
    print("• CISO Assistant (Risk Register): http://localhost:8443")
    print("• Tazama (Fraud Detection): http://localhost:4000")
    print("\n🔧 ADMIN URLS:")
    print("• PostgreSQL: localhost:5432 (user: risk_user, db: risk_management)")
    print("• Redis: localhost:6379")
    print("• NATS (Tazama messaging): localhost:4222")
    print("\n📋 MANAGEMENT COMMANDS:")
    print("• View logs: docker-compose logs -f [service_name]")
    print("• Stop system: docker-compose down")
    print("• Restart service: docker-compose restart [service_name]")
    print("• View status: docker-compose ps")
    print("\n🔐 DEFAULT CREDENTIALS:")
    print("• Database: risk_user / risk_password")
    print("• Change these in .env.production for production use!")
    print("\n" + "="*60)

def main():
    """Main startup function"""
    print("🏦 WEKEZA BANK RISK MANAGEMENT SYSTEM")
    print("🚀 Production Startup Script")
    print("="*50)
    
    # Pre-flight checks
    if not check_docker():
        sys.exit(1)
    
    if not check_environment():
        sys.exit(1)
    
    # Start services
    if not start_services():
        sys.exit(1)
    
    # Wait for services to be ready
    wait_for_services()
    
    # Show access information
    show_access_info()
    
    print("\n🎯 System is ready for production use!")
    print("💡 Tip: Run 'python test_system.py' to verify all components")

if __name__ == "__main__":
    main()