import sqlite3
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
from config import Config
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.config = Config()
        self.engine = create_engine(self.config.database_url)
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database with required tables"""
        try:
            with self.engine.connect() as conn:
                if self.config.is_production:
                    # PostgreSQL schema
                    self._create_postgresql_schema(conn)
                else:
                    # SQLite schema (for local development)
                    self._create_sqlite_schema(conn)
                
                logger.info("Database tables initialized successfully")
                
                # Insert sample data if tables are empty
                self._insert_sample_data(conn)
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def _create_postgresql_schema(self, conn):
        """Create PostgreSQL schema"""
        # Create analyst cases table
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS analyst_cases (
            case_id SERIAL PRIMARY KEY,
            transaction_id VARCHAR(50) UNIQUE NOT NULL,
            customer_id VARCHAR(50),
            amount DECIMAL(15,2),
            currency VARCHAR(3) DEFAULT 'KES',
            merchant_name VARCHAR(255),
            transaction_type VARCHAR(50),
            risk_score FLOAT,
            risk_level VARCHAR(20) DEFAULT 'LOW',
            status VARCHAR(20) DEFAULT 'ASSIGNED',
            analyst_id VARCHAR(50),
            analyst_comment TEXT,
            flagged_reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            closed_at TIMESTAMP
        )
        """))
        
        # Create risk metrics table
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS risk_metrics (
            metric_id SERIAL PRIMARY KEY,
            metric_type VARCHAR(50),
            metric_name VARCHAR(100),
            metric_value DECIMAL(15,4),
            threshold_value DECIMAL(15,4),
            status VARCHAR(20),
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """))
        
        # Create transaction history table
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS transaction_history (
            id SERIAL PRIMARY KEY,
            transaction_id VARCHAR(50) UNIQUE NOT NULL,
            customer_id VARCHAR(50),
            account_number VARCHAR(20),
            amount DECIMAL(15,2),
            currency VARCHAR(3) DEFAULT 'KES',
            transaction_type VARCHAR(50),
            merchant_name VARCHAR(255),
            merchant_category VARCHAR(100),
            location VARCHAR(100),
            channel VARCHAR(50),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) DEFAULT 'PENDING'
        )
        """))
        
        # Create indexes for better performance
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_transaction_status ON transaction_history(status)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_transaction_timestamp ON transaction_history(timestamp)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_case_status ON analyst_cases(status)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_case_risk_level ON analyst_cases(risk_level)"))
        
        conn.commit()
    
    def _create_sqlite_schema(self, conn):
        """Create SQLite schema (for local development)"""
        # Create analyst cases table
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS analyst_cases (
            case_id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id VARCHAR(50) UNIQUE NOT NULL,
            customer_id VARCHAR(50),
            amount DECIMAL(15,2),
            currency VARCHAR(3) DEFAULT 'KES',
            merchant_name VARCHAR(255),
            transaction_type VARCHAR(50),
            risk_score FLOAT,
            risk_level VARCHAR(20) DEFAULT 'LOW',
            status VARCHAR(20) DEFAULT 'ASSIGNED',
            analyst_id VARCHAR(50),
            analyst_comment TEXT,
            flagged_reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            closed_at TIMESTAMP
        )
        """))
        
        # Create risk metrics table
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS risk_metrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_type VARCHAR(50),
            metric_name VARCHAR(100),
            metric_value DECIMAL(15,4),
            threshold_value DECIMAL(15,4),
            status VARCHAR(20),
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """))
        
        # Create transaction history table
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS transaction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id VARCHAR(50) UNIQUE NOT NULL,
            customer_id VARCHAR(50),
            account_number VARCHAR(20),
            amount DECIMAL(15,2),
            currency VARCHAR(3) DEFAULT 'KES',
            transaction_type VARCHAR(50),
            merchant_name VARCHAR(255),
            merchant_category VARCHAR(100),
            location VARCHAR(100),
            channel VARCHAR(50),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) DEFAULT 'PENDING'
        )
        """))
        
        conn.commit()
    
    def _insert_sample_data(self, conn):
        """Insert sample data for testing"""
        try:
            # Check if we already have data
            result = conn.execute(text("SELECT COUNT(*) FROM transaction_history")).fetchone()
            if result[0] > 0:
                return  # Data already exists
            
            # Insert sample transactions
            sample_transactions = [
                ('TXN_001', 'CUST_12345', '1234567890', 50000.00, 'KES', 'TRANSFER', 'TechSoft Ltd', 'SOFTWARE', 'Nairobi', 'MOBILE', 'PENDING'),
                ('TXN_002', 'CUST_67890', '0987654321', 2500000.00, 'KES', 'PAYMENT', 'Unknown Shell Co', 'UNKNOWN', 'Mombasa', 'ONLINE', 'PENDING'),
                ('TXN_003', 'CUST_11111', '1111111111', 75000.00, 'KES', 'WITHDRAWAL', 'ATM Network', 'CASH', 'Kisumu', 'ATM', 'PENDING'),
                ('TXN_004', 'CUST_22222', '2222222222', 15000000.00, 'KES', 'TRANSFER', 'Suspicious Entity', 'HIGH_RISK', 'Unknown', 'MOBILE', 'PENDING')
            ]
            
            for txn in sample_transactions:
                if self.config.is_production:
                    # PostgreSQL syntax
                    conn.execute(text("""
                        INSERT INTO transaction_history 
                        (transaction_id, customer_id, account_number, amount, currency, transaction_type, 
                         merchant_name, merchant_category, location, channel, status)
                        VALUES (:txn_id, :cust_id, :acc_num, :amount, :currency, :txn_type, 
                                :merchant, :category, :location, :channel, :status)
                        ON CONFLICT (transaction_id) DO NOTHING
                    """), {
                        'txn_id': txn[0], 'cust_id': txn[1], 'acc_num': txn[2], 'amount': txn[3],
                        'currency': txn[4], 'txn_type': txn[5], 'merchant': txn[6], 'category': txn[7],
                        'location': txn[8], 'channel': txn[9], 'status': txn[10]
                    })
                else:
                    # SQLite syntax
                    conn.execute(text("""
                        INSERT OR IGNORE INTO transaction_history 
                        (transaction_id, customer_id, account_number, amount, currency, transaction_type, 
                         merchant_name, merchant_category, location, channel, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """), txn)
            
            # Insert sample risk metrics
            sample_metrics = [
                ('CREDIT', 'Portfolio Default Rate', 0.05, 0.10, 'OK'),
                ('LIQUIDITY', 'Liquidity Coverage Ratio', 1.25, 1.00, 'OK'),
                ('MARKET', 'Value at Risk (1-day)', 2500000.00, 5000000.00, 'OK'),
                ('OPERATIONAL', 'System Uptime', 0.999, 0.995, 'OK')
            ]
            
            for metric in sample_metrics:
                if self.config.is_production:
                    conn.execute(text("""
                        INSERT INTO risk_metrics 
                        (metric_type, metric_name, metric_value, threshold_value, status)
                        VALUES (:type, :name, :value, :threshold, :status)
                    """), {
                        'type': metric[0], 'name': metric[1], 'value': metric[2],
                        'threshold': metric[3], 'status': metric[4]
                    })
                else:
                    conn.execute(text("""
                        INSERT INTO risk_metrics 
                        (metric_type, metric_name, metric_value, threshold_value, status)
                        VALUES (?, ?, ?, ?, ?)
                    """), metric)
            
            conn.commit()
            logger.info("Sample data inserted successfully")
            
        except Exception as e:
            logger.error(f"Error inserting sample data: {e}")
    
    def get_connection(self):
        """Get a database connection"""
        if self.config.is_production:
            return psycopg2.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                database=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD
            )
        else:
            return sqlite3.connect(self.config.DB_NAME)
    
    def fetch_pending_transactions(self, limit=None):
        """Fetch transactions that haven't been processed yet"""
        query = """
        SELECT th.* FROM transaction_history th
        LEFT JOIN analyst_cases ac ON th.transaction_id = ac.transaction_id
        WHERE th.status = 'PENDING' AND ac.transaction_id IS NULL
        ORDER BY th.timestamp DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        
        try:
            df = pd.read_sql(query, self.engine)
            logger.info(f"Fetched {len(df)} pending transactions")
            return df
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            return pd.DataFrame()
    
    def create_analyst_case(self, transaction_data, risk_score, risk_level, flagged_reason):
        """Create a new case for analyst review"""
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            if self.config.is_production:
                # PostgreSQL syntax
                cur.execute("""
                    INSERT INTO analyst_cases 
                    (transaction_id, customer_id, amount, currency, merchant_name, 
                     transaction_type, risk_score, risk_level, flagged_reason, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'ASSIGNED')
                    RETURNING case_id
                """, (
                    transaction_data['transaction_id'],
                    transaction_data['customer_id'],
                    transaction_data['amount'],
                    transaction_data.get('currency', 'KES'),
                    transaction_data.get('merchant_name', ''),
                    transaction_data.get('transaction_type', ''),
                    risk_score,
                    risk_level,
                    flagged_reason
                ))
                case_id = cur.fetchone()[0]
            else:
                # SQLite syntax
                cur.execute("""
                    INSERT INTO analyst_cases 
                    (transaction_id, customer_id, amount, currency, merchant_name, 
                     transaction_type, risk_score, risk_level, flagged_reason, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'ASSIGNED')
                """, (
                    transaction_data['transaction_id'],
                    transaction_data['customer_id'],
                    transaction_data['amount'],
                    transaction_data.get('currency', 'KES'),
                    transaction_data.get('merchant_name', ''),
                    transaction_data.get('transaction_type', ''),
                    risk_score,
                    risk_level,
                    flagged_reason
                ))
                case_id = cur.lastrowid
            
            conn.commit()
            logger.info(f"Created analyst case {case_id} for transaction {transaction_data['transaction_id']}")
            return case_id
        except Exception as e:
            logger.error(f"Error creating analyst case: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def update_transaction_status(self, transaction_id, status):
        """Update transaction status (APPROVED, REJECTED, BLOCKED)"""
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            if self.config.is_production:
                cur.execute("""
                    UPDATE transaction_history 
                    SET status = %s 
                    WHERE transaction_id = %s
                """, (status, transaction_id))
            else:
                cur.execute("""
                    UPDATE transaction_history 
                    SET status = ? 
                    WHERE transaction_id = ?
                """, (status, transaction_id))
            
            conn.commit()
            logger.info(f"Updated transaction {transaction_id} status to {status}")
        except Exception as e:
            logger.error(f"Error updating transaction status: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def get_portfolio_metrics(self):
        """Calculate portfolio-level risk metrics"""
        try:
            # Calculate current portfolio statistics
            if self.config.is_production:
                query = """
                SELECT 
                    COUNT(*) as total_transactions,
                    AVG(amount) as avg_amount,
                    SUM(CASE WHEN amount > 10000000 THEN 1 ELSE 0 END) as high_value_count,
                    COUNT(DISTINCT customer_id) as unique_customers
                FROM transaction_history 
                WHERE timestamp >= CURRENT_DATE - INTERVAL '1 day'
                """
            else:
                query = """
                SELECT 
                    COUNT(*) as total_transactions,
                    AVG(amount) as avg_amount,
                    SUM(CASE WHEN amount > 10000000 THEN 1 ELSE 0 END) as high_value_count,
                    COUNT(DISTINCT customer_id) as unique_customers
                FROM transaction_history 
                WHERE datetime(timestamp) >= datetime('now', '-1 day')
                """
            
            df = pd.read_sql(query, self.engine)
            return df.iloc[0].to_dict()
        except Exception as e:
            logger.error(f"Error calculating portfolio metrics: {e}")
            return {}
    
    def log_risk_metric(self, metric_type, metric_name, value, threshold, status):
        """Log a risk metric to the database"""
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            if self.config.is_production:
                cur.execute("""
                    INSERT INTO risk_metrics 
                    (metric_type, metric_name, metric_value, threshold_value, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (metric_type, metric_name, value, threshold, status))
            else:
                cur.execute("""
                    INSERT INTO risk_metrics 
                    (metric_type, metric_name, metric_value, threshold_value, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (metric_type, metric_name, value, threshold, status))
            
            conn.commit()
        except Exception as e:
            logger.error(f"Error logging risk metric: {e}")
            conn.rollback()
        finally:
            conn.close()