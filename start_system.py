#!/usr/bin/env python3
"""
Startup script for the Equity Bank Risk Management System

This script provides an easy way to start the various components of the system.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Print system banner"""
    print("=" * 60)
    print("🛡️  EQUITY BANK RISK MANAGEMENT SYSTEM")
    print("=" * 60)
    print("Powered by Open Source Components:")
    print("• Risk Engine (Python + SQLite)")
    print("• Streamlit Dashboard")
    print("• Ballerine Integration (Simulated)")
    print("• CISO Assistant Integration (Simulated)")
    print("• Tazama Fraud Detection (Simulated)")
    print("=" * 60)

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        import sqlalchemy
        import sklearn
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install -r risk_engine/requirements.txt")
        return False

def generate_sample_data():
    """Generate sample transaction data"""
    print("\n🔄 Generating sample transaction data...")
    try:
        result = subprocess.run([
            sys.executable, "test_data/generate_sample_data.py", "--count", "50"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Sample data generated successfully")
            return True
        else:
            print(f"❌ Error generating sample data: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error generating sample data: {e}")
        return False

def process_transactions():
    """Process transactions through the risk engine"""
    print("\n🔄 Processing transactions through risk engine...")
    try:
        result = subprocess.run([
            sys.executable, "risk_engine/main.py", "--once"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Transactions processed successfully")
            return True
        else:
            print(f"❌ Error processing transactions: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error processing transactions: {e}")
        return False

def start_dashboard():
    """Start the Streamlit dashboard"""
    print("\n🚀 Starting Streamlit dashboard...")
    print("📊 Dashboard will be available at: http://localhost:8501")
    print("🌐 Opening browser automatically...")
    
    try:
        # Start Streamlit in the background
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            "dashboard/app.py", "--server.port", "8501", "--server.headless", "true"
        ])
        
        # Wait a moment for Streamlit to start
        time.sleep(3)
        
        # Open browser
        webbrowser.open("http://localhost:8501")
        
        print("✅ Dashboard started successfully!")
        print("\n" + "=" * 60)
        print("🎉 SYSTEM IS READY!")
        print("=" * 60)
        print("📊 Dashboard: http://localhost:8501")
        print("🔍 Check the following pages:")
        print("   • Dashboard Overview - Key metrics and charts")
        print("   • Analyst Workbench - Review high-risk cases")
        print("   • Risk Register - Enterprise risk management")
        print("   • Transaction Monitor - Real-time monitoring")
        print("   • Deep Dive Analytics - Advanced analysis")
        print("=" * 60)
        print("⏹️  Press Ctrl+C to stop the dashboard")
        
        # Keep the process running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping dashboard...")
            process.terminate()
            print("✅ Dashboard stopped")
        
        return True
        
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return False

def run_tests():
    """Run system tests"""
    print("\n🧪 Running system tests...")
    try:
        result = subprocess.run([
            sys.executable, "test_system.py", "--quick"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print(f"⚠️ Some tests failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    """Main startup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Run tests
    if not run_tests():
        print("⚠️ Tests failed, but continuing anyway...")
    
    # Generate sample data
    if not generate_sample_data():
        print("⚠️ Sample data generation failed, but continuing anyway...")
    
    # Process transactions
    if not process_transactions():
        print("⚠️ Transaction processing failed, but continuing anyway...")
    
    # Start dashboard
    start_dashboard()

if __name__ == "__main__":
    main()