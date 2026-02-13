"""
Migration Configuration
Configure your database connections and migration settings here
"""

# SQLite Database Configuration
SQLITE_CONFIG = {
    'database_path': 'transactions_db',  # Path to your SQLite database
    'alternative_paths': [
        'risk_management.db',
        '../transactions_db',
        'risk_engine/risk_management.db',
        '../risk_management.db'
    ]
}

# MySQL Database Configuration
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',  # Your MySQL password
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_0900_ai_ci'
}

# Target Database Configuration
TARGET_CONFIG = {
    'database_name': 'wekeza_risk_management',
    'create_if_not_exists': True,
    'drop_if_exists': False,  # Set to True to recreate database
    'batch_size': 1000  # Number of rows to insert at once
}

# Table Mapping (if you want to rename tables)
TABLE_MAPPING = {
    # 'old_table_name': 'new_table_name'
    # Example: 'analyst_cases': 'risk_cases'
}

# Tables to exclude from migration
EXCLUDE_TABLES = [
    'sqlite_sequence',  # SQLite system table
    # Add any other tables you want to skip
]

# Custom SQL to run after migration
POST_MIGRATION_SQL = [
    # Example: "ALTER TABLE analyst_cases ADD INDEX idx_risk_score (risk_score);",
    # "CREATE VIEW high_risk_cases AS SELECT * FROM analyst_cases WHERE risk_level = 'HIGH';",
]