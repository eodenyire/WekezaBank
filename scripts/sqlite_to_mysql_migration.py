#!/usr/bin/env python3
"""
SQLite to MySQL Migration Service
Migrates data from SQLite database to MySQL with proper schema creation
"""

import sqlite3
import mysql.connector
import pandas as pd
import logging
from datetime import datetime
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'risk_engine'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SQLiteToMySQLMigrator:
    """Handles migration from SQLite to MySQL"""
    
    def __init__(self, sqlite_db_path, mysql_config):
        """
        Initialize migrator
        
        Args:
            sqlite_db_path (str): Path to SQLite database file
            mysql_config (dict): MySQL connection configuration
        """
        self.sqlite_db_path = sqlite_db_path
        self.mysql_config = mysql_config
        self.sqlite_conn = None
        self.mysql_conn = None
        
    def connect_sqlite(self):
        """Connect to SQLite database"""
        try:
            self.sqlite_conn = sqlite3.connect(self.sqlite_db_path)
            logger.info(f"Connected to SQLite database: {self.sqlite_db_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to SQLite: {e}")
            return False
    
    def connect_mysql(self):
        """Connect to MySQL database"""
        try:
            self.mysql_conn = mysql.connector.connect(**self.mysql_config)
            logger.info(f"Connected to MySQL database: {self.mysql_config['host']}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MySQL: {e}")
            return False
    
    def get_sqlite_tables(self):
        """Get list of tables from SQLite database"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            logger.info(f"Found {len(tables)} tables in SQLite: {tables}")
            return tables
        except Exception as e:
            logger.error(f"Error getting SQLite tables: {e}")
            return []
    
    def get_table_schema(self, table_name):
        """Get schema information for a SQLite table"""
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            schema = []
            for col in columns:
                col_info = {
                    'name': col[1],
                    'type': col[2],
                    'not_null': col[3],
                    'default': col[4],
                    'primary_key': col[5]
                }
                schema.append(col_info)
            
            logger.info(f"Retrieved schema for table {table_name}: {len(schema)} columns")
            return schema
        except Exception as e:
            logger.error(f"Error getting schema for {table_name}: {e}")
            return []
    
    def sqlite_to_mysql_type(self, sqlite_type):
        """Convert SQLite data type to MySQL data type"""
        type_mapping = {
            'INTEGER': 'INT',
            'TEXT': 'TEXT',
            'REAL': 'DECIMAL(15,4)',
            'BLOB': 'BLOB',
            'NUMERIC': 'DECIMAL(15,4)',
            'VARCHAR(50)': 'VARCHAR(50)',
            'VARCHAR(255)': 'VARCHAR(255)',
            'VARCHAR(100)': 'VARCHAR(100)',
            'VARCHAR(20)': 'VARCHAR(20)',
            'DECIMAL(15,2)': 'DECIMAL(15,2)',
            'DECIMAL(15,4)': 'DECIMAL(15,4)',
            'FLOAT': 'FLOAT',
            'TIMESTAMP': 'TIMESTAMP',
            'DATETIME': 'DATETIME'
        }
        
        # Handle specific patterns
        if 'VARCHAR' in sqlite_type.upper():
            return sqlite_type
        elif 'DECIMAL' in sqlite_type.upper():
            return sqlite_type
        elif sqlite_type.upper() in type_mapping:
            return type_mapping[sqlite_type.upper()]
        else:
            # Default mapping
            if 'INT' in sqlite_type.upper():
                return 'INT'
            elif 'TEXT' in sqlite_type.upper() or 'CHAR' in sqlite_type.upper():
                return 'TEXT'
            elif 'REAL' in sqlite_type.upper() or 'FLOAT' in sqlite_type.upper():
                return 'DECIMAL(15,4)'
            else:
                return 'TEXT'  # Default fallback
    
    def create_mysql_table(self, table_name, schema):
        """Create MySQL table based on SQLite schema"""
        try:
            cursor = self.mysql_conn.cursor()
            
            # Build CREATE TABLE statement
            columns = []
            primary_keys = []
            
            for col in schema:
                mysql_type = self.sqlite_to_mysql_type(col['type'])
                
                # Handle special cases
                if col['name'].lower() in ['id', 'case_id', 'metric_id'] and col['primary_key']:
                    mysql_type = 'INT AUTO_INCREMENT'
                
                col_def = f"`{col['name']}` {mysql_type}"
                
                if col['not_null'] and not col['primary_key']:
                    col_def += " NOT NULL"
                
                if col['default'] is not None and col['default'] != '':
                    if col['default'].upper() in ['CURRENT_TIMESTAMP', 'NOW()']:
                        col_def += " DEFAULT CURRENT_TIMESTAMP"
                    elif col['default'].startswith("'") and col['default'].endswith("'"):
                        col_def += f" DEFAULT {col['default']}"
                    else:
                        col_def += f" DEFAULT '{col['default']}'"
                
                columns.append(col_def)
                
                if col['primary_key']:
                    primary_keys.append(f"`{col['name']}`")
            
            # Add primary key constraint
            if primary_keys:
                columns.append(f"PRIMARY KEY ({', '.join(primary_keys)})")
            
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS `{table_name}` (
                {',\n    '.join(columns)}
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """
            
            cursor.execute(create_sql)
            self.mysql_conn.commit()
            logger.info(f"Created MySQL table: {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating MySQL table {table_name}: {e}")
            return False
    
    def migrate_table_data(self, table_name):
        """Migrate data from SQLite table to MySQL table"""
        try:
            # Read data from SQLite
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.sqlite_conn)
            
            if df.empty:
                logger.info(f"No data to migrate for table {table_name}")
                return True
            
            logger.info(f"Migrating {len(df)} rows from {table_name}")
            
            # Prepare MySQL cursor
            cursor = self.mysql_conn.cursor()
            
            # Get column names
            columns = df.columns.tolist()
            placeholders = ', '.join(['%s'] * len(columns))
            column_names = ', '.join([f"`{col}`" for col in columns])
            
            # Insert data in batches
            batch_size = 1000
            total_rows = len(df)
            
            for i in range(0, total_rows, batch_size):
                batch = df.iloc[i:i+batch_size]
                
                # Convert DataFrame to list of tuples
                data = []
                for _, row in batch.iterrows():
                    # Handle None values and data type conversions
                    row_data = []
                    for value in row:
                        if pd.isna(value):
                            row_data.append(None)
                        elif isinstance(value, (int, float, str)):
                            row_data.append(value)
                        else:
                            row_data.append(str(value))
                    data.append(tuple(row_data))
                
                # Insert batch
                insert_sql = f"""
                INSERT INTO `{table_name}` ({column_names}) 
                VALUES ({placeholders})
                """
                
                cursor.executemany(insert_sql, data)
                self.mysql_conn.commit()
                
                logger.info(f"Migrated batch {i//batch_size + 1}: {len(batch)} rows")
            
            logger.info(f"Successfully migrated all data for table {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error migrating data for {table_name}: {e}")
            return False
    
    def create_database(self, database_name):
        """Create MySQL database if it doesn't exist"""
        try:
            cursor = self.mysql_conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci")
            cursor.execute(f"USE `{database_name}`")
            self.mysql_conn.commit()
            logger.info(f"Created/selected database: {database_name}")
            return True
        except Exception as e:
            logger.error(f"Error creating database {database_name}: {e}")
            return False
    
    def migrate_all(self, target_database):
        """Migrate all tables from SQLite to MySQL"""
        try:
            # Connect to databases
            if not self.connect_sqlite():
                return False
            
            if not self.connect_mysql():
                return False
            
            # Create target database
            if not self.create_database(target_database):
                return False
            
            # Get all tables
            tables = self.get_sqlite_tables()
            
            if not tables:
                logger.warning("No tables found in SQLite database")
                return False
            
            # Migrate each table
            success_count = 0
            for table in tables:
                logger.info(f"Processing table: {table}")
                
                # Get schema
                schema = self.get_table_schema(table)
                if not schema:
                    logger.warning(f"Skipping table {table} - no schema found")
                    continue
                
                # Create MySQL table
                if not self.create_mysql_table(table, schema):
                    logger.warning(f"Failed to create MySQL table {table}")
                    continue
                
                # Migrate data
                if self.migrate_table_data(table):
                    success_count += 1
                    logger.info(f"✅ Successfully migrated table: {table}")
                else:
                    logger.warning(f"❌ Failed to migrate data for table: {table}")
            
            logger.info(f"Migration completed: {success_count}/{len(tables)} tables migrated successfully")
            return success_count == len(tables)
            
        except Exception as e:
            logger.error(f"Error during migration: {e}")
            return False
        
        finally:
            # Close connections
            if self.sqlite_conn:
                self.sqlite_conn.close()
            if self.mysql_conn:
                self.mysql_conn.close()

def main():
    """Main migration function"""
    print("🔄 SQLite to MySQL Migration Service")
    print("=" * 50)
    
    # Configuration
    sqlite_db_path = "risk_management.db"  # Default SQLite database
    
    # Check if SQLite database exists
    if not os.path.exists(sqlite_db_path):
        # Try alternative paths
        alternative_paths = [
            "transactions_db",
            "../risk_management.db",
            "risk_engine/risk_management.db"
        ]
        
        for path in alternative_paths:
            if os.path.exists(path):
                sqlite_db_path = path
                break
        else:
            logger.error(f"SQLite database not found. Checked paths: {[sqlite_db_path] + alternative_paths}")
            return False
    
    # MySQL configuration
    mysql_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',  # Change this to your MySQL password
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_0900_ai_ci'
    }
    
    target_database = 'wekeza_risk_management'
    
    print(f"📂 Source SQLite: {sqlite_db_path}")
    print(f"🎯 Target MySQL: {mysql_config['host']}:{mysql_config['port']}/{target_database}")
    print(f"👤 MySQL User: {mysql_config['user']}")
    
    # Confirm before proceeding
    response = input("\n🤔 Proceed with migration? (y/N): ")
    if response.lower() != 'y':
        print("Migration cancelled.")
        return False
    
    # Create migrator and run migration
    migrator = SQLiteToMySQLMigrator(sqlite_db_path, mysql_config)
    
    print("\n🚀 Starting migration...")
    success = migrator.migrate_all(target_database)
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print(f"✅ All data migrated to MySQL database: {target_database}")
        print(f"🔗 Connection string: mysql://{mysql_config['user']}@{mysql_config['host']}:{mysql_config['port']}/{target_database}")
    else:
        print("\n❌ Migration completed with errors. Check migration.log for details.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)