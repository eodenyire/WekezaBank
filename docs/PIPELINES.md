# ETL Pipeline Configuration for Wekeza Bank Analytics

## Overview
This document describes the ETL (Extract, Transform, Load) pipeline configurations for the Wekeza Bank Analytics framework.

## Pipeline Types

### 1. Daily Transaction Pipeline
**Frequency**: Daily at 2 AM  
**Purpose**: Process daily transaction data

```yaml
name: daily_transactions
schedule: "0 2 * * *"
steps:
  - extract:
      source: transaction_database
      query: "SELECT * FROM transactions WHERE date = CURRENT_DATE - 1"
  - transform:
      - validate_schema
      - clean_data
      - detect_anomalies
      - flag_fraud
  - load:
      destination: analytics_warehouse
      table: processed_transactions
  - analyze:
      - transaction_summary
      - spending_patterns
      - merchant_analysis
```

### 2. Weekly Customer Analytics Pipeline
**Frequency**: Weekly on Monday at 3 AM  
**Purpose**: Update customer analytics and segmentation

```yaml
name: weekly_customer_analytics
schedule: "0 3 * * 1"
steps:
  - extract:
      sources:
        - customers
        - transactions
        - accounts
  - transform:
      - calculate_rfm
      - segment_customers
      - calculate_clv
      - assess_churn_risk
  - load:
      destination: analytics_warehouse
      tables:
        - customer_segments
        - customer_metrics
  - notify:
      type: email
      recipients: analytics-team@wekeza.com
```

### 3. Monthly Financial Reporting Pipeline
**Frequency**: First day of each month at 4 AM  
**Purpose**: Generate monthly financial reports

```yaml
name: monthly_financial_report
schedule: "0 4 1 * *"
steps:
  - extract:
      sources:
        - transactions
        - accounts
        - customers
      period: previous_month
  - transform:
      - calculate_kpis
      - revenue_analysis
      - profitability_metrics
      - portfolio_analysis
  - analyze:
      - generate_insights
      - create_visualizations
  - report:
      format: [pdf, json]
      destination: reports/monthly/
  - notify:
      type: email
      recipients: finance-team@wekeza.com
      attachments: monthly_report.pdf
```

### 4. Real-time Fraud Detection Pipeline
**Frequency**: Continuous  
**Purpose**: Monitor transactions for fraud in real-time

```yaml
name: realtime_fraud_detection
mode: streaming
steps:
  - subscribe:
      source: transaction_stream
  - validate:
      - schema_validation
      - basic_checks
  - analyze:
      - anomaly_detection
      - fraud_scoring
      - velocity_check
  - alert:
      condition: fraud_score > 0.7
      channels:
        - slack: #fraud-alerts
        - email: fraud-team@wekeza.com
        - sms: [emergency_contacts]
  - store:
      destination: fraud_investigations
```

## Pipeline Configuration

### Environment Variables
```bash
# Database connections
DB_HOST=localhost
DB_PORT=5432
DB_NAME=wekeza_bank
DB_USER=analytics_user
DB_PASSWORD=secure_password

# Analytics settings
ANALYTICS_THRESHOLD_FRAUD=0.7
ANALYTICS_THRESHOLD_CHURN=0.5
ANALYTICS_SEGMENTS=5

# Notifications
SMTP_HOST=smtp.wekeza.com
SMTP_PORT=587
ALERT_EMAIL=alerts@wekeza.com
```

### Data Sources
1. **Transaction Database**: PostgreSQL
2. **Customer Database**: PostgreSQL
3. **Account Database**: PostgreSQL
4. **Transaction Stream**: Kafka topic `transactions`

### Data Destinations
1. **Analytics Warehouse**: PostgreSQL/Snowflake
2. **Reports**: S3/Local filesystem
3. **Dashboards**: Tableau/PowerBI

## Pipeline Execution

### Using Prefect
```python
from prefect import flow, task
from wekeza_analytics.workflows import AnalyticsWorkflow

@task
def extract_data():
    # Extract data logic
    pass

@task
def run_analytics(data):
    workflow = AnalyticsWorkflow()
    return workflow.run_full_analysis(**data)

@task
def generate_report(results):
    # Generate report logic
    pass

@flow
def daily_analytics_flow():
    data = extract_data()
    results = run_analytics(data)
    generate_report(results)

if __name__ == "__main__":
    daily_analytics_flow()
```

### Using Airflow
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def run_analytics():
    from wekeza_analytics.workflows import AnalyticsWorkflow
    # Analytics logic
    pass

with DAG(
    'daily_analytics',
    start_date=datetime(2024, 1, 1),
    schedule='@daily'
) as dag:
    
    analytics_task = PythonOperator(
        task_id='run_analytics',
        python_callable=run_analytics
    )
```

## Monitoring and Alerts

### Metrics to Monitor
- Pipeline execution time
- Data volume processed
- Error rates
- Alert frequency
- Resource utilization

### Alert Conditions
- Pipeline failure
- Data quality issues
- Fraud detection
- High churn risk
- System errors

## Data Quality Checks

### Transaction Data
- Non-null transaction IDs
- Valid date formats
- Positive amounts
- Valid customer IDs
- Valid transaction types

### Customer Data
- Unique customer IDs
- Valid email formats
- Credit scores in range [300, 850]
- Non-negative incomes

### Account Data
- Unique account IDs
- Non-negative balances
- Valid account types
- Valid status values

## Scaling Considerations

### For Large Datasets
- Use batch processing for historical data
- Implement incremental loading
- Use parallel processing where possible
- Consider data partitioning by date/customer
- Implement caching for frequently accessed data

### For Real-time Processing
- Use stream processing frameworks (Kafka, Flink)
- Implement micro-batching
- Use in-memory processing where appropriate
- Implement circuit breakers for fault tolerance

## Backup and Recovery

### Data Backup
- Daily backups of analytics results
- Weekly backups of raw data
- Monthly archival to cold storage

### Recovery Procedures
- Point-in-time recovery for databases
- Pipeline replay capability
- Data validation after recovery

## Security

### Data Protection
- Encryption at rest and in transit
- Access control for sensitive data
- Data masking for PII
- Audit logging for all operations

### Compliance
- GDPR compliance for customer data
- PCI DSS compliance for transaction data
- SOC 2 compliance for security controls
