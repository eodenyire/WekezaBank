#!/usr/bin/env python3
"""
Large Data Migration Script
Handles large datasets with smaller batch sizes and MySQL optimization
"""

import sqlite3
import mysql.connector
import pandas as pd
import os
import sys
from migration_config import SQLITE_CONFIG, MYSQL_CONFIG, TARGET_CONFIG

def migrate_large_table(sqlite_conn, mysql_conn, table_name, batch_size=100):
    """Migrate large table in small batches"""
    try:
        print(f"📊 Migrating large table: {table_name}")
        
        # Get total row count
        cursor = sqlite_conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_rows = cursor.fetchone()[0]
        print(f"   📈 Total rows to migrate: {total_rows}")
        
        if total_rows == 0:
            print(f"   ⚠️ No data in table {table_name}")
            return True
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]
        
        # Prepare MySQL insert statement
        mysql_cursor = mysql_conn.cursor()
        placeholders = ', '.join(['%s'] * len(column_names))
        column_names_str = ', '.join([f"`{col}`" for col in column_names])
        insert_sql = f"INSERT INTO `{table_name}` ({column_names_str}) VALUES ({placeholders})"
        
        # Process in batches
        offset = 0
        batch_num = 1
        total_inserted = 0
        
        while offset < total_rows:
            print(f"   🔄 Processing batch {batch_num} (rows {offset+1}-{min(offset+batch_size, total_rows)})")
            
            # Read batch from SQLite
            batch_query = f"SELECT * FROM {table_name} LIMIT {batch_size} OFFSET {offset}"
            df_batch = pd.read_sql_query(batch_query, sqlite_conn)
            
            if df_batch.empty:
                break
            
            # Convert to list of tuples
            batch_data = []
            for _, row in df_batch.iterrows():
                row_data = []
                for value in row:
                    if pd.isna(value):
                        row_data.append(None)
                    else:
                        row_data.append(value)
                batch_data.append(tuple(row_data))
            
            # Insert batch
            mysql_cursor.executemany(insert_sql, batch_data)
            mysql_conn.commit()
            
            total_inserted += len(batch_data)
            print(f"   ✅ Inserted batch {batch_num}: {len(batch_data)} rows (Total: {total_inserted})")
            
            offset += batch_size
            batch_num += 1
        
        print(f"   🎉 Successfully migrated {total_inserted} rows for table {table_name}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error migrating {table_name}: {e}")
        return False

def main():
    """Main migration function for large datasets"""
    print("🚀 Large Data Migration - SQLite to MySQL")
    print("=" * 50)
    
    # Find SQLite database
    sqlite_path = None
    
    # Check current directory first
    if os.path.exists(f"../{SQLITE_CONFIG['database_path']}"):
        sqlite_path = f"../{SQLITE_CONFIG['database_path']}"
    elif os.path.exists(SQLITE_CONFIG['database_path']):
        sqlite_path = SQLITE_CONFIG['database_path']
    else:
        # Check alternative paths
        for path in SQLITE_CONFIG['alternative_paths']:
            if os.path.exists(f"../{path}"):
                sqlite_path = f"../{path}"
                break
            elif os.path.exists(path):
                sqlite_path = path
                break
    
    if not sqlite_path:
        print("❌ SQLite database not found!")
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
    try:
        mysql_conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = mysql_conn.cursor()
        
        # Create database
        db_name = TARGET_CONFIG['database_name']
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci")
        cursor.execute(f"USE `{db_name}`")
        
        # Optimize MySQL for large inserts
        cursor.execute("SET SESSION max_allowed_packet = 1073741824")  # 1GB
        cursor.execute("SET SESSION bulk_insert_buffer_size = 268435456")  # 256MB
        cursor.execute("SET SESSION innodb_buffer_pool_size = 268435456")  # 256MB
        
        mysql_conn.commit()
        print(f"✅ Connected to MySQL and optimized for large data")
        
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        return False
    
    # Check what tables need migration
    cursor = mysql_conn.cursor()
    cursor.execute("SHOW TABLES")
    existing_tables = [table[0] for table in cursor.fetchall()]
    
    print(f"📋 Existing tables in MySQL: {existing_tables}")
    
    # Focus on transaction_history if it's empty
    if 'transaction_history' in existing_tables:
        cursor.execute("SELECT COUNT(*) FROM transaction_history")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("🎯 Focusing on transaction_history table (currently empty)")
            success = migrate_large_table(sqlite_conn, mysql_conn, 'transaction_history', batch_size=50)
        else:
            print(f"✅ transaction_history already has {count} rows")
            success = True
    else:
        print("❌ transaction_history table not found in MySQL")
        success = False
    
    # Close connections
    sqlite_conn.close()
    mysql_conn.close()
    
    if success:
        print("\n🎉 Large data migration completed successfully!")
        return True
    else:
        print("\n❌ Large data migration failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)