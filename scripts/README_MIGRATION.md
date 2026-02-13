# 🔄 SQLite to MySQL Migration Service

This service migrates your SQLite database data to MySQL, preserving table structures and data integrity.

## 🎯 What It Does

- **Extracts** all data from your SQLite database
- **Creates** corresponding MySQL tables with proper schemas
- **Migrates** all data with type conversion
- **Preserves** primary keys, indexes, and relationships
- **Handles** large datasets with batch processing

## 🚀 Quick Start

### Option 1: Windows Batch Script (Easiest)
```cmd
# Just double-click or run:
scripts\migrate.bat
```

### Option 2: Python Script
```bash
# Install dependencies
pip install pandas mysql-connector-python sqlalchemy

# Run migration
cd scripts
python quick_migrate.py
```

### Option 3: Advanced Migration
```bash
# For custom configurations
python sqlite_to_mysql_migration.py
```

## ⚙️ Configuration

Edit `scripts/migration_config.py` to customize:

```python
# MySQL Connection
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',  # Change this!
}

# Target Database
TARGET_CONFIG = {
    'database_name': 'wekeza_risk_management',
    'batch_size': 1000
}
```

## 📋 Prerequisites

### MySQL Setup
1. **Install MySQL Server**
   ```bash
   # Windows: Download from https://dev.mysql.com/downloads/mysql/
   # Ubuntu: sudo apt install mysql-server
   # macOS: brew install mysql
   ```

2. **Start MySQL Service**
   ```bash
   # Windows: Start MySQL service from Services
   # Linux: sudo systemctl start mysql
   # macOS: brew services start mysql
   ```

3. **Create MySQL User** (Optional)
   ```sql
   CREATE USER 'risk_user'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT ALL PRIVILEGES ON *.* TO 'risk_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Python Dependencies
```bash
pip install pandas mysql-connector-python sqlalchemy
```

## 🗂️ What Gets Migrated

The service will migrate these tables from your SQLite database:

| SQLite Table | MySQL Table | Description |
|--------------|-------------|-------------|
| `analyst_cases` | `analyst_cases` | Risk analysis cases |
| `risk_metrics` | `risk_metrics` | Portfolio risk metrics |
| `transaction_history` | `transaction_history` | Transaction records |

## 🔧 Data Type Mapping

| SQLite Type | MySQL Type | Notes |
|-------------|------------|-------|
| `INTEGER` | `INT` | Auto-increment for primary keys |
| `TEXT` | `TEXT` | Variable length text |
| `VARCHAR(n)` | `VARCHAR(n)` | Fixed length preserved |
| `DECIMAL(m,n)` | `DECIMAL(m,n)` | Precision preserved |
| `REAL/FLOAT` | `DECIMAL(15,4)` | For financial accuracy |
| `TIMESTAMP` | `TIMESTAMP` | With CURRENT_TIMESTAMP default |

## 📊 Migration Process

1. **Discovery**: Scans SQLite database for tables
2. **Schema Analysis**: Extracts column definitions and constraints
3. **MySQL Setup**: Creates target database and tables
4. **Data Transfer**: Migrates data in batches for performance
5. **Verification**: Confirms row counts match

## 🔍 Monitoring Migration

The migration provides real-time feedback:

```
🚀 Quick SQLite to MySQL Migration
========================================
📂 Found SQLite database: risk_management.db
✅ Connected to SQLite
✅ Connected to MySQL and created database: wekeza_risk_management
📋 Found 3 tables to migrate: ['analyst_cases', 'risk_metrics', 'transaction_history']

📊 Migrating table: analyst_cases
   📈 Found 150 rows
   ✅ Created MySQL table structure
   ✅ Inserted 150 rows

📊 Migrating table: risk_metrics
   📈 Found 25 rows
   ✅ Created MySQL table structure
   ✅ Inserted 25 rows

📊 Migrating table: transaction_history
   📈 Found 50000 rows
   ✅ Created MySQL table structure
   ✅ Inserted 50000 rows

========================================
🎉 Migration completed!
✅ Successfully migrated: 3/3 tables
🔗 MySQL Database: wekeza_risk_management
🔗 Connection: mysql://root@127.0.0.1:3306/wekeza_risk_management
```

## 🔗 Using Migrated Data

After migration, connect to your MySQL database:

### Python Connection
```python
import mysql.connector

conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='your_password',
    database='wekeza_risk_management'
)

# Query data
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM transaction_history")
count = cursor.fetchone()[0]
print(f"Total transactions: {count}")
```

### MySQL Workbench
- **Host**: 127.0.0.1
- **Port**: 3306
- **Username**: root
- **Password**: your_password
- **Database**: wekeza_risk_management

## 🛠️ Troubleshooting

### Common Issues

**MySQL Connection Failed**
```bash
# Check if MySQL is running
mysql -u root -p

# On Windows, check Services for MySQL
# On Linux: sudo systemctl status mysql
```

**Permission Denied**
```sql
-- Grant permissions to user
GRANT ALL PRIVILEGES ON wekeza_risk_management.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

**Large Dataset Issues**
```python
# Increase batch size in migration_config.py
TARGET_CONFIG = {
    'batch_size': 5000  # Increase from 1000
}
```

**SQLite Database Not Found**
```python
# Check paths in migration_config.py
SQLITE_CONFIG = {
    'database_path': 'path/to/your/database.db',
    'alternative_paths': [
        'risk_management.db',
        'transactions_db',
        '../risk_management.db'
    ]
}
```

## 📈 Performance Tips

1. **Batch Size**: Adjust based on available memory
2. **Indexes**: Add indexes after migration for better performance
3. **InnoDB**: Uses InnoDB engine for better performance and ACID compliance
4. **UTF8MB4**: Full Unicode support including emojis

## 🔒 Security Considerations

1. **Change Default Passwords**: Never use 'root'/'root' in production
2. **Create Dedicated User**: Create a specific user for the application
3. **Network Security**: Restrict MySQL access to localhost if possible
4. **Backup**: Always backup before migration

## 📝 Post-Migration Steps

1. **Verify Data Integrity**
   ```sql
   SELECT COUNT(*) FROM analyst_cases;
   SELECT COUNT(*) FROM risk_metrics;
   SELECT COUNT(*) FROM transaction_history;
   ```

2. **Add Indexes** (Optional)
   ```sql
   ALTER TABLE transaction_history ADD INDEX idx_customer_id (customer_id);
   ALTER TABLE transaction_history ADD INDEX idx_timestamp (timestamp);
   ALTER TABLE analyst_cases ADD INDEX idx_risk_level (risk_level);
   ```

3. **Update Application Configuration**
   ```python
   # Update your config.py to use MySQL
   DB_HOST = '127.0.0.1'
   DB_PORT = 3306
   DB_NAME = 'wekeza_risk_management'
   DB_USER = 'root'
   DB_PASSWORD = 'your_password'
   ```

---

**🎉 Your SQLite data is now ready in MySQL for production use!**