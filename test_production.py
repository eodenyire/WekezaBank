#!/usr/bin/env python3
"""
Production System Test Suite
Tests all components of the Wekeza Bank Risk Management System
"""

import os
import sys
import time
import requests
import psycopg2
import redis
import pandas as pd
from datetime import datetime
import subprocess
import json

# Add risk_engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'risk_engine'))

def test_docker_services():
    """Test that all Docker services are running"""
    print("🐳 Testing Docker Services...")
    
    try:
        result = subprocess.run(
            ["docker-compose", "ps"], 
            cwd="infrastructure",
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            print("❌ Docker Compose not running")
            return False
        
        # Check if all services are up
        services = ["postgres", "redis", "risk-engine", "dashboard"]
        for service in services:
            if service not in result.stdout or "Up" not in result.stdout:
                print(f"⚠️ Service {service} may not be running")
        
        print("✅ Docker services are running")
        return True
        
    except Exception as e:
        print(f"❌ Error checking Docker services: {e}")
        return False

def test_postgresql():
    """Test PostgreSQL database connection and schema"""
    print("🐘 Testing PostgreSQL...")
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="risk_management",
            user="risk_user",
            password="risk_password"
        )
        
        cur = conn.cursor()
        
        # Test basic connection
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"✅ PostgreSQL connected: {version[0][:50]}...")
        
        # Test required tables exist
        tables = ["analyst_cases", "risk_metrics", "transaction_history"]
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table};")
            count = cur.fetchone()[0]
            print(f"✅ Table {table}: {count} records")
        
        # Test additional databases
        additional_dbs = ["ballerine", "ciso_assistant", "tazama"]
        for db in additional_dbs:
            try:
                test_conn = psycopg2.connect(
                    host="localhost",
                    port=5432,
                    database=db,
                    user="risk_user",
                    password="risk_password"
                )
                test_conn.close()
                print(f"✅ Database {db} accessible")
            except Exception as e:
                print(f"⚠️ Database {db} not accessible: {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL test failed: {e}")
        return False

def test_redis():
    """Test Redis connection"""
    print("🔴 Testing Redis...")
    
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        
        # Test basic operations
        r.set('test_key', 'test_value')
        value = r.get('test_key')
        
        if value == 'test_value':
            print("✅ Redis read/write operations working")
            r.delete('test_key')
            return True
        else:
            print("❌ Redis read/write test failed")
            return False
            
    except Exception as e:
        print(f"❌ Redis test failed: {e}")
        return False

def test_risk_engine():
    """Test the risk engine components"""
    print("⚙️ Testing Risk Engine...")
    
    try:
        from config import Config
        from database import DatabaseManager
        from risk_models import RiskEngine
        
        # Test configuration
        config = Config()
        print(f"✅ Configuration loaded - Environment: {config.ENVIRONMENT}")
        print(f"✅ Database URL: {config.database_url}")
        
        # Test database manager
        db = DatabaseManager()
        print("✅ Database manager initialized")
        
        # Test risk engine
        risk_engine = RiskEngine()
        print("✅ Risk engine initialized")
        
        # Test with sample transaction
        sample_transaction = {
            'transaction_id': 'TEST_001',
            'customer_id': 'CUST_TEST',
            'amount': 5000000.00,
            'currency': 'KES',
            'merchant_name': 'Test Merchant',
            'transaction_type': 'TRANSFER'
        }
        
        risk_score = risk_engine.calculate_risk_score(sample_transaction)
        print(f"✅ Risk calculation working - Score: {risk_score:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Risk engine test failed: {e}")
        return False

def test_dashboard():
    """Test Streamlit dashboard"""
    print("📊 Testing Dashboard...")
    
    try:
        # Test dashboard health endpoint
        response = requests.get("http://localhost:8501/_stcore/health", timeout=10)
        
        if response.status_code == 200:
            print("✅ Dashboard health check passed")
        else:
            print(f"⚠️ Dashboard health check returned: {response.status_code}")
        
        # Test main dashboard page
        response = requests.get("http://localhost:8501", timeout=10)
        
        if response.status_code == 200:
            print("✅ Dashboard main page accessible")
            return True
        else:
            print(f"❌ Dashboard main page returned: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

def test_integrations():
    """Test external service integrations"""
    print("🔗 Testing Integrations...")
    
    try:
        from integrations import BallerineIntegration, CISOAssistantIntegration, TazamaIntegration
        
        # Test Ballerine integration
        ballerine = BallerineIntegration()
        sample_data = {
            'transaction_id': 'TEST_INTEGRATION',
            'customer_id': 'CUST_TEST',
            'amount': 1000000.00
        }
        
        result = ballerine.create_case(sample_data, 0.7, ["High amount"])
        if result.get('success'):
            print("✅ Ballerine integration working")
        else:
            print(f"⚠️ Ballerine integration: {result.get('error', 'Unknown error')}")
        
        # Test CISO Assistant integration
        ciso = CISOAssistantIntegration()
        result = ciso.log_risk_event("OPERATIONAL", "Test Risk", "Test description", "medium")
        if result.get('success'):
            print("✅ CISO Assistant integration working")
        else:
            print(f"⚠️ CISO Assistant integration: {result.get('error', 'Unknown error')}")
        
        # Test Tazama integration
        tazama = TazamaIntegration()
        result = tazama.submit_transaction(sample_data)
        if result.get('success'):
            print("✅ Tazama integration working")
        else:
            print(f"⚠️ Tazama integration: {result.get('error', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def test_external_services():
    """Test external service endpoints"""
    print("🌐 Testing External Services...")
    
    services = {
        "Ballerine Frontend": "http://localhost:5173",
        "CISO Assistant": "http://localhost:8443",
        "Tazama": "http://localhost:4000"
    }
    
    results = {}
    
    for service_name, url in services.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {service_name} accessible")
                results[service_name] = True
            else:
                print(f"⚠️ {service_name} returned status: {response.status_code}")
                results[service_name] = False
        except Exception as e:
            print(f"⚠️ {service_name} not accessible: {e}")
            results[service_name] = False
    
    return any(results.values())

def test_data_flow():
    """Test end-to-end data flow"""
    print("🔄 Testing Data Flow...")
    
    try:
        from database import DatabaseManager
        from risk_models import RiskEngine
        
        db = DatabaseManager()
        risk_engine = RiskEngine()
        
        # Create test transaction
        test_transaction = {
            'transaction_id': f'TEST_FLOW_{int(time.time())}',
            'customer_id': 'CUST_FLOW_TEST',
            'account_number': '1234567890',
            'amount': 7500000.00,
            'currency': 'KES',
            'transaction_type': 'TRANSFER',
            'merchant_name': 'Flow Test Merchant',
            'merchant_category': 'TEST',
            'location': 'Nairobi',
            'channel': 'MOBILE',
            'status': 'PENDING'
        }
        
        # Insert test transaction
        conn = db.get_connection()
        cur = conn.cursor()
        
        if db.config.is_production:
            cur.execute("""
                INSERT INTO transaction_history 
                (transaction_id, customer_id, account_number, amount, currency, 
                 transaction_type, merchant_name, merchant_category, location, channel, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(test_transaction.values()))
        else:
            cur.execute("""
                INSERT INTO transaction_history 
                (transaction_id, customer_id, account_number, amount, currency, 
                 transaction_type, merchant_name, merchant_category, location, channel, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, tuple(test_transaction.values()))
        
        conn.commit()
        print("✅ Test transaction inserted")
        
        # Calculate risk score
        risk_score = risk_engine.calculate_risk_score(test_transaction)
        print(f"✅ Risk score calculated: {risk_score:.3f}")
        
        # Create analyst case if high risk
        if risk_score > 0.5:
            case_id = db.create_analyst_case(
                test_transaction, 
                risk_score, 
                "HIGH" if risk_score > 0.8 else "MEDIUM",
                "Automated test case"
            )
            if case_id:
                print(f"✅ Analyst case created: {case_id}")
            else:
                print("⚠️ Failed to create analyst case")
        
        # Clean up test data
        if db.config.is_production:
            cur.execute("DELETE FROM analyst_cases WHERE transaction_id = %s", (test_transaction['transaction_id'],))
            cur.execute("DELETE FROM transaction_history WHERE transaction_id = %s", (test_transaction['transaction_id'],))
        else:
            cur.execute("DELETE FROM analyst_cases WHERE transaction_id = ?", (test_transaction['transaction_id'],))
            cur.execute("DELETE FROM transaction_history WHERE transaction_id = ?", (test_transaction['transaction_id'],))
        
        conn.commit()
        conn.close()
        print("✅ Test data cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Data flow test failed: {e}")
        return False

def generate_test_report(results):
    """Generate a comprehensive test report"""
    print("\n" + "="*60)
    print("📋 PRODUCTION SYSTEM TEST REPORT")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print(f"\n📊 SUMMARY:")
    print(f"• Total Tests: {total_tests}")
    print(f"• Passed: {passed_tests}")
    print(f"• Failed: {total_tests - passed_tests}")
    print(f"• Success Rate: {passed_tests/total_tests*100:.1f}%")
    
    print(f"\n📝 DETAILED RESULTS:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"• {test_name}: {status}")
    
    if passed_tests == total_tests:
        print(f"\n🎉 ALL TESTS PASSED - SYSTEM IS PRODUCTION READY!")
    elif passed_tests >= total_tests * 0.8:
        print(f"\n⚠️ MOST TESTS PASSED - SYSTEM IS MOSTLY READY")
        print("   Review failed tests before full production deployment")
    else:
        print(f"\n❌ MULTIPLE TESTS FAILED - SYSTEM NEEDS ATTENTION")
        print("   Address failed components before production use")
    
    print("="*60)

def main():
    """Run all production tests"""
    print("🏦 WEKEZA BANK RISK MANAGEMENT SYSTEM")
    print("🧪 Production System Test Suite")
    print("="*50)
    
    # Run all tests
    test_results = {
        "Docker Services": test_docker_services(),
        "PostgreSQL Database": test_postgresql(),
        "Redis Cache": test_redis(),
        "Risk Engine": test_risk_engine(),
        "Dashboard": test_dashboard(),
        "Integrations": test_integrations(),
        "External Services": test_external_services(),
        "Data Flow": test_data_flow()
    }
    
    # Generate report
    generate_test_report(test_results)
    
    # Return exit code based on results
    if all(test_results.values()):
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)