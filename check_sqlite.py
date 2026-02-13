#!/usr/bin/env python3
"""
Check SQLite database structure
"""
import sqlite3
import os

def check_sqlite_database():
    db_path = 'transactions_db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📂 SQLite Database: {db_path}")
        print(f"📋 Found {len(tables)} tables:")
        
        for table in tables:
            table_name = table[0]
            print(f"\n🔹 Table: {table_name}")
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("   Columns:")
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                is_pk = "PK" if col[5] else ""
                print(f"   - {col_name}: {col_type} {is_pk}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   📊 Rows: {count}")
        
        conn.close()
        print(f"\n✅ Database analysis complete!")
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")

if __name__ == "__main__":
    check_sqlite_database()