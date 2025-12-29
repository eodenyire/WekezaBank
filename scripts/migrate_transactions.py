#!/usr/bin/env python3
"""
Simple Transaction Migration
Migrate transaction_history table with small batches
"""

import sqlite3
import mysql.connector
import pandas as pd
import os
import sys

def migrate_transactions():
    """Migrate transaction_history table in small batches"""
    print("🚀 Transaction History Migration")
    print("=" * 40)
    
    # Connect to SQLite
    sqlite_path = "../transactions_db"
    if not os.path.exists(sqlite_path):
        print(f"❌ SQLite database not found: {sqlite_path}")
        return False
    
    try:
        sqlite_conn = sqlite3.connect(sqlite_path)
        print("✅ Connected to SQLite")
    except Exception as e:
        print(f"❌ SQLite connection failed: {e}")
        return False
    
    # Connect to MySQL
    try:
        mysql_conn = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            database='wekeza_risk_management'
        )
        print("✅ Connected to MySQL")
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        return False
    
    # Check current state
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute("SELECT COUNT(*) FROM transaction_history")
    current_count = mysql_cursor.fetchone()[0]
    print(f"📊 Current MySQL rows: {current_count}")
    
    # Get total SQLite rows
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute("SELECT COUNT(*) FROM transaction_history")
    total_rows = sqlite_cursor.fetchone()[0]
    print(f"📊 SQLite rows to migrate: {total_rows}")
    
    if current_count >= total_rows:
        print("✅ Data already migrated!")
        return True
    
    # Clear existing data and start fresh
    if current_count > 0:
        print("🧹 Clearing existing data...")
        mysql_cursor.execute("DELETE FROM transaction_history")
        mysql_conn.commit()
    
    # Migrate in very small batches
    batch_size = 25  # Very small batches to avoid packet size issues
    offset = 0
    total_inserted = 0
    
    print(f"🔄 Starting migration in batches of {batch_size}...")
    
    while offset < total_rows:
        try:
            # Read small batch from SQLite
            query = f"""
            SELECT id, transaction_id, customer_id, account_number, amount, currency,
                   transaction_type, merchant_name, merchant_category, location, 
                   channel, timestamp, status
            FROM transaction_history 
            LIMIT {batch_size} OFFSET {offset}
            """
            
            df_batch = pd.read_sql_query(query, sqlite_conn)
            
            if df_batch.empty:
                break
            
            # Insert each row individually to avoid packet size issues
            insert_sql = """
            INSERT INTO transaction_history 
            (id, transaction_id, customer_id, account_number, amount, currency,
             transaction_type, merchant_name, merchant_category, location, 
             channel, timestamp, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
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
            offset += batch_size
            
            # Progress update
            progress = (offset / total_rows) * 100
            print(f"   📈 Progress: {progress:.1f}% ({total_inserted:,} / {total_rows:,} rows)")
            
        except Exception as e:
            print(f"❌ Error at offset {offset}: {e}")
            # Try to continue with next batch
            offset += batch_size
            continue
    
    # Final verification
    mysql_cursor.execute("SELECT COUNT(*) FROM transaction_history")
    final_count = mysql_cursor.fetchone()[0]
    
    print(f"\n🎉 Migration completed!")
    print(f"✅ Final count: {final_count:,} rows")
    print(f"📊 Success rate: {(final_count/total_rows)*100:.1f}%")
    
    # Close connections
    sqlite_conn.close()
    mysql_conn.close()
    
    return final_count > 0

if __name__ == "__main__":
    success = migrate_transactions()
    sys.exit(0 if success else 1)