#!/bin/bash
set -e

# This script creates multiple databases for the different services
# It's called by the PostgreSQL Docker container during initialization

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create additional databases for the integrated services
    CREATE DATABASE ballerine;
    CREATE DATABASE ciso_assistant;
    CREATE DATABASE tazama;
    
    -- Grant all privileges to the risk_user
    GRANT ALL PRIVILEGES ON DATABASE ballerine TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE ciso_assistant TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE tazama TO $POSTGRES_USER;
    
    -- Connect to each database and set up basic schemas
    
    -- Ballerine database setup
    \c ballerine;
    CREATE SCHEMA IF NOT EXISTS ballerine;
    GRANT ALL ON SCHEMA ballerine TO $POSTGRES_USER;
    
    -- CISO Assistant database setup  
    \c ciso_assistant;
    CREATE SCHEMA IF NOT EXISTS ciso_assistant;
    GRANT ALL ON SCHEMA ciso_assistant TO $POSTGRES_USER;
    
    -- Tazama database setup
    \c tazama;
    CREATE SCHEMA IF NOT EXISTS tazama;
    GRANT ALL ON SCHEMA tazama TO $POSTGRES_USER;
    
    -- Create basic tables for Tazama (transaction monitoring)
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        transaction_id VARCHAR(50) UNIQUE NOT NULL,
        amount DECIMAL(15,2),
        currency VARCHAR(3) DEFAULT 'USD',
        debtor_account VARCHAR(50),
        creditor_account VARCHAR(50),
        transaction_type VARCHAR(50),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) DEFAULT 'PENDING'
    );
    
    CREATE TABLE IF NOT EXISTS alerts (
        id SERIAL PRIMARY KEY,
        transaction_id VARCHAR(50) REFERENCES transactions(transaction_id),
        rule_id VARCHAR(50),
        alert_type VARCHAR(50),
        severity VARCHAR(20),
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) DEFAULT 'OPEN'
    );
    
    -- Create indexes
    CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp);
    CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);
    CREATE INDEX IF NOT EXISTS idx_alerts_transaction_id ON alerts(transaction_id);
    CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status);
    
EOSQL

echo "Multiple databases created successfully!"