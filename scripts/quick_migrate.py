#!/usr/bin/env python3
"""
Quick Migration Script
Simple script to migrate SQLite data to MySQL with minimal configuration
"""

import sqlite3
import mysql.connector
import pandas as pd
import os
import sys
from migration_config import SQLITE_CONFIG, MYSQL_CONFIG, TARGET_CONFIG

def find_sqlite_database():
    """Find the SQLite database file"""
    # Check main path
    if os.path.exists(SQLITE_CONFIG['database_path']):
        return SQLITE_CONFIG['database_path']
    
    # Check alternative paths
    for path in SQLITE_CONFIG['alternative_paths']:
        if os.path.exists(path):
            return path
    
    return None

def connect_mysql():
    """Connect to MySQL and create database"""
    try:
        # Connect without database first
        conn = mysql.connector.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password']
        )
        
        cursor = conn.cursor()
        
        # Create database
        db_name = TARGET_CONFIG['database_name']
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci")
        cursor.execute(f"USE `{db_name}`")
        
        conn.commit()
        print(f"✅ Connected to MySQL and created/selected database: {db_name}")
        return conn
        
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        return None

def migrate_table(sqlite_conn, mysql_conn, table_name):
    """Migrate a single table"""
    try:
        print(f"📊 Migrating table: {table_name}")
        
        # Read all data from SQLite
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", sqlite_conn)
        
        if df.empty:
            print(f"   ⚠️ No data in table {table_name}")
            return True
        
        print(f"   📈 Found {len(df)} rows")
        
        # Get SQLite schema
        cursor = sqlite_conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        
        # Create MySQL table
        mysql_cursor = mysql_conn.cursor()
        
        # Drop table if exists (optional)
        mysql_cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        
        # Build CREATE TABLE statement
        create_sql = f"CREATE TABLE `{table_name}` ("
        column_defs = []
        
        for col in columns_info:
            col_name = col[1]
            col_type = col[2]
            is_pk = col[5]
            
            # Convert SQLite types to MySQL types
            if 'INT' in col_type.upper():
                mysql_type = 'INT AUTO_INCREMENT' if is_pk else 'INT'
            elif 'TEXT' in col_type.upper():
                mysql_type = 'TEXT'
            elif 'VARCHAR' in col_type.upper():
                mysql_type = col_type
            elif 'DECIMAL' in col_type.upper():
                mysql_type = col_type
            elif 'FLOAT' in col_type.upper() or 'REAL' in col_type.upper():
                mysql_type = 'DECIMAL(15,4)'
            elif 'TIMESTAMP' in col_type.upper() or 'DATETIME' in col_type.upper():
                mysql_type = 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
            else:
                mysql_type = 'TEXT'
            
            column_def = f"`{col_name}` {mysql_type}"
            if is_pk:
                column_def += " PRIMARY KEY"
            
            column_defs.append(column_def)
        
        create_sql += ", ".join(column_defs) + ")"
        
        mysql_cursor.execute(create_sql)
        print(f"   ✅ Created MySQL table structure")
        
        # Insert data
        columns = df.columns.tolist()
        placeholders = ', '.join(['%s'] * len(columns))
        column_names = ', '.join([f"`{col}`" for col in columns])
        
        insert_sql = f"INSERT INTO `{table_name}` ({column_names}) VALUES ({placeholders})"
        
        # Convert DataFrame to list of tuples
        data = []
        for _, row in df.iterrows():
            row_data = []
            for value in row:
                if pd.isna(value):
                    row_data.append(None)
                else:
                    row_data.append(value)
            data.append(tuple(row_data))
        
        mysql_cursor.executemany(insert_sql, data)
        mysql_conn.commit()
        
        print(f"   ✅ Inserted {len(data)} rows")
        return True
        
    except Exception as e:
        print(f"   ❌ Error migrating {table_name}: {e}")
        return False

def main():
    """Main migration function"""
    print("🚀 Quick SQLite to MySQL Migration")
    print("=" * 40)
    
    # Find SQLite database
    sqlite_path = find_sqlite_database()
    if not sqlite_path:
        print("❌ SQLite database not found!")
        print("   Checked paths:")
        for path in [SQLITE_CONFIG['database_path']] + SQLITE_CONFIG['alternative_paths']:
            print(f"   - {path}")
        return False
    
    print(f"📂 Found SQLite database: {sqlite_path}")
    
    # Connect to SQLite
    try:
        sqlite_conn = sqlite3.connect(sqlite_path)
        print("✅ Connected to SQLite")
    except Exception as e:
        print(f"❌ SQLite connection failed: {e}")
        return False
    
    # Connect to MySQL
    mysql_conn = connect_mysql()
    if not mysql_conn:
        return False
    
    # Get tables from SQLite
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    # Filter out system tables
    tables = [t for t in tables if not t.startswith('sqlite_')]
    
    print(f"📋 Found {len(tables)} tables to migrate: {tables}")
    
    # Migrate each table
    success_count = 0
    for table in tables:
        if migrate_table(sqlite_conn, mysql_conn, table):
            success_count += 1
    
    # Close connections
    sqlite_conn.close()
    mysql_conn.close()
    
    print("\n" + "=" * 40)
    print(f"🎉 Migration completed!")
    print(f"✅ Successfully migrated: {success_count}/{len(tables)} tables")
    
    if success_count == len(tables):
        print(f"🔗 MySQL Database: {TARGET_CONFIG['database_name']}")
        print(f"🔗 Connection: mysql://{MYSQL_CONFIG['user']}@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{TARGET_CONFIG['database_name']}")
        return True
    else:
        print("⚠️ Some tables failed to migrate. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)