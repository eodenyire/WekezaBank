-- Initialize databases for the risk management system

-- Create databases for each service
CREATE DATABASE ballerine;
CREATE DATABASE ciso_assistant;
CREATE DATABASE tazama;

-- Grant permissions to risk_user
GRANT ALL PRIVILEGES ON DATABASE ballerine TO risk_user;
GRANT ALL PRIVILEGES ON DATABASE ciso_assistant TO risk_user;
GRANT ALL PRIVILEGES ON DATABASE tazama TO risk_user;

-- The main risk_management database is created by default
-- Create tables in the main risk_management database

-- Create analyst cases table for transaction monitoring
CREATE TABLE IF NOT EXISTS analyst_cases (
    case_id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) UNIQUE NOT NULL,
    customer_id VARCHAR(50),
    amount DECIMAL(15,2),
    currency VARCHAR(3) DEFAULT 'KES',
    merchant_name VARCHAR(255),
    transaction_type VARCHAR(50),
    risk_score FLOAT,
    risk_level VARCHAR(20) DEFAULT 'LOW', -- LOW, MEDIUM, HIGH
    status VARCHAR(20) DEFAULT 'ASSIGNED', -- ASSIGNED, IN_PROGRESS, ESCALATED, CLOSED, BLOCKED
    analyst_id VARCHAR(50),
    analyst_comment TEXT,
    flagged_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP
);

-- Create risk metrics table for portfolio-level monitoring
CREATE TABLE IF NOT EXISTS risk_metrics (
    metric_id SERIAL PRIMARY KEY,
    metric_type VARCHAR(50), -- CREDIT, LIQUIDITY, MARKET, OPERATIONAL
    metric_name VARCHAR(100),
    metric_value DECIMAL(15,4),
    threshold_value DECIMAL(15,4),
    status VARCHAR(20), -- OK, WARNING, CRITICAL
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create transaction history table (simulated data warehouse)
CREATE TABLE IF NOT EXISTS transaction_history (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) UNIQUE NOT NULL,
    customer_id VARCHAR(50),
    account_number VARCHAR(20),
    amount DECIMAL(15,2),
    currency VARCHAR(3) DEFAULT 'KES',
    transaction_type VARCHAR(50), -- TRANSFER, PAYMENT, WITHDRAWAL, DEPOSIT
    merchant_name VARCHAR(255),
    merchant_category VARCHAR(100),
    location VARCHAR(100),
    channel VARCHAR(50), -- MOBILE, ATM, BRANCH, ONLINE
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'PENDING' -- PENDING, APPROVED, REJECTED, BLOCKED
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_analyst_cases_status ON analyst_cases(status);
CREATE INDEX IF NOT EXISTS idx_analyst_cases_risk_level ON analyst_cases(risk_level);
CREATE INDEX IF NOT EXISTS idx_analyst_cases_created ON analyst_cases(created_at);
CREATE INDEX IF NOT EXISTS idx_transaction_history_customer ON transaction_history(customer_id);
CREATE INDEX IF NOT EXISTS idx_transaction_history_timestamp ON transaction_history(timestamp);
CREATE INDEX IF NOT EXISTS idx_transaction_history_status ON transaction_history(status);
CREATE INDEX IF NOT EXISTS idx_risk_metrics_type ON risk_metrics(metric_type);
CREATE INDEX IF NOT EXISTS idx_risk_metrics_calculated ON risk_metrics(calculated_at);

-- Insert sample data for testing
INSERT INTO transaction_history (transaction_id, customer_id, account_number, amount, transaction_type, merchant_name, merchant_category, location, channel) VALUES
('TXN_001', 'CUST_12345', '1234567890', 50000.00, 'TRANSFER', 'TechSoft Ltd', 'SOFTWARE', 'Nairobi', 'MOBILE'),
('TXN_002', 'CUST_67890', '0987654321', 2500000.00, 'PAYMENT', 'Unknown Shell Co', 'UNKNOWN', 'Mombasa', 'ONLINE'),
('TXN_003', 'CUST_11111', '1111111111', 75000.00, 'WITHDRAWAL', 'ATM Network', 'CASH', 'Kisumu', 'ATM'),
('TXN_004', 'CUST_22222', '2222222222', 15000000.00, 'TRANSFER', 'Suspicious Entity', 'HIGH_RISK', 'Unknown', 'MOBILE')
ON CONFLICT (transaction_id) DO NOTHING;

-- Insert sample risk metrics
INSERT INTO risk_metrics (metric_type, metric_name, metric_value, threshold_value, status) VALUES
('CREDIT', 'Portfolio Default Rate', 0.05, 0.10, 'OK'),
('LIQUIDITY', 'Liquidity Coverage Ratio', 1.25, 1.00, 'OK'),
('MARKET', 'Value at Risk (1-day)', 2500000.00, 5000000.00, 'OK'),
('OPERATIONAL', 'System Uptime', 0.999, 0.995, 'OK')
ON CONFLICT DO NOTHING;