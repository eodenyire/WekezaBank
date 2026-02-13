#!/usr/bin/env python3
"""
Test MySQL connection
"""
import mysql.connector
import sys

def test_mysql_connection():
    try:
        print("🔌 Testing MySQL connection...")
        
        # Connection config
        config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root'
        }
        
        # Test connection
        conn = mysql.connector.connect(**config)
        
        if conn.is_connected():
            print("✅ MySQL connection successful!")
            
            # Get MySQL version
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📊 MySQL Version: {version[0]}")
            
            # Show databases
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print(f"📂 Available databases:")
            for db in databases:
                print(f"   - {db[0]}")
            
            conn.close()
            return True
        else:
            print("❌ MySQL connection failed")
            return False
            
    except mysql.connector.Error as e:
        print(f"❌ MySQL connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_mysql_connection()
    sys.exit(0 if success else 1)