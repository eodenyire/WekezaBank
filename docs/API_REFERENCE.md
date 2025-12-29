# Wekeza Bank Analytics API Reference

## Overview
This document provides detailed API reference for the Wekeza Bank Analytics Framework.

## Table of Contents
- [Customer Analytics](#customer-analytics)
- [Transaction Analytics](#transaction-analytics)
- [Financial Metrics](#financial-metrics)
- [Predictive Analytics](#predictive-analytics)
- [Workflows](#workflows)
- [Utilities](#utilities)

---

## Customer Analytics

### `CustomerAnalytics`

Main class for customer-related analytics.

#### Methods

##### `rfm_analysis(transactions_df, reference_date=None)`

Perform RFM (Recency, Frequency, Monetary) analysis on customer transactions.

**Parameters:**
- `transactions_df` (pd.DataFrame): Transaction data with columns: customer_id, transaction_date, transaction_id, amount
- `reference_date` (datetime, optional): Reference date for recency calculation. Defaults to current date.

**Returns:**
- pd.DataFrame: RFM scores and customer segments

**Example:**
```python
from wekeza_analytics.analytics import CustomerAnalytics

analytics = CustomerAnalytics()
rfm_results = analytics.rfm_analysis(transactions_df)
print(rfm_results[['customer_id', 'segment', 'rfm_score']])
```

##### `customer_segmentation(customers_df, n_clusters=4)`

Segment customers using K-means clustering.

**Parameters:**
- `customers_df` (pd.DataFrame): Customer data with features for clustering
- `n_clusters` (int): Number of segments to create

**Returns:**
- tuple: (segmented_df, segment_stats)

**Example:**
```python
segmented_customers, stats = analytics.customer_segmentation(customers_df, n_clusters=5)
print(f"Created {len(stats)} segments")
```

##### `calculate_customer_lifetime_value(transactions_df, customers_df, time_period_months=12)`

Calculate Customer Lifetime Value (CLV).

**Parameters:**
- `transactions_df` (pd.DataFrame): Transaction history
- `customers_df` (pd.DataFrame): Customer information
- `time_period_months` (int): Time period for CLV calculation

**Returns:**
- pd.DataFrame: CLV metrics per customer

**Example:**
```python
clv_results = analytics.calculate_customer_lifetime_value(
    transactions_df, 
    customers_df,
    time_period_months=24
)
```

##### `churn_risk_analysis(transactions_df, customers_df, inactive_days=90)`

Analyze customer churn risk.

**Parameters:**
- `transactions_df` (pd.DataFrame): Transaction history
- `customers_df` (pd.DataFrame): Customer information
- `inactive_days` (int): Days of inactivity to consider at-risk

**Returns:**
- pd.DataFrame: Churn risk scores and categories

---

## Transaction Analytics

### `TransactionAnalytics`

Main class for transaction-related analytics.

#### Methods

##### `transaction_summary(transactions_df, period='daily')`

Generate transaction summary statistics.

**Parameters:**
- `transactions_df` (pd.DataFrame): Transaction data
- `period` (str): Aggregation period ('daily', 'weekly', 'monthly')

**Returns:**
- pd.DataFrame: Aggregated transaction summaries

**Example:**
```python
from wekeza_analytics.analytics import TransactionAnalytics

analytics = TransactionAnalytics()
summary = analytics.transaction_summary(transactions_df, period='monthly')
```

##### `detect_anomalies(transactions_df, features=None)`

Detect anomalous transactions using machine learning.

**Parameters:**
- `transactions_df` (pd.DataFrame): Transaction data
- `features` (list, optional): Features for anomaly detection

**Returns:**
- pd.DataFrame: Transactions with anomaly flags and scores

##### `fraud_detection_analysis(transactions_df)`

Analyze fraud patterns.

**Parameters:**
- `transactions_df` (pd.DataFrame): Transaction data with fraud flags

**Returns:**
- dict: Fraud statistics and patterns

##### `spending_pattern_analysis(transactions_df, customer_id=None)`

Analyze spending patterns.

**Parameters:**
- `transactions_df` (pd.DataFrame): Transaction data
- `customer_id` (str, optional): Specific customer to analyze

**Returns:**
- dict: Spending pattern statistics

---

## Financial Metrics

### `FinancialMetrics`

Main class for financial KPIs and metrics.

#### Methods

##### `calculate_kpis(transactions_df, accounts_df, customers_df)`

Calculate comprehensive Key Performance Indicators.

**Parameters:**
- `transactions_df` (pd.DataFrame): Transaction data
- `accounts_df` (pd.DataFrame): Account data
- `customers_df` (pd.DataFrame): Customer data

**Returns:**
- dict: Comprehensive KPIs

**Example:**
```python
from wekeza_analytics.analytics import FinancialMetrics

metrics = FinancialMetrics()
kpis = metrics.calculate_kpis(transactions_df, accounts_df, customers_df)
print(f"Total Revenue: ${kpis['profitability']['total_revenue']:,.2f}")
```

##### `calculate_revenue_metrics(transactions_df, period='monthly')`

Calculate revenue metrics.

**Parameters:**
- `transactions_df` (pd.DataFrame): Transaction data
- `period` (str): Time period for aggregation

**Returns:**
- dict: Revenue metrics

##### `calculate_portfolio_metrics(accounts_df, transactions_df)`

Calculate portfolio performance metrics.

**Parameters:**
- `accounts_df` (pd.DataFrame): Account data
- `transactions_df` (pd.DataFrame): Transaction data

**Returns:**
- dict: Portfolio metrics

##### `calculate_liquidity_metrics(accounts_df)`

Calculate liquidity metrics.

**Parameters:**
- `accounts_df` (pd.DataFrame): Account data

**Returns:**
- dict: Liquidity metrics

---

## Predictive Analytics

### `PredictiveAnalytics`

Main class for predictive modeling and forecasting.

#### Methods

##### `calculate_credit_risk_score(customers_df, transactions_df=None)`

Calculate credit risk scores.

**Parameters:**
- `customers_df` (pd.DataFrame): Customer data
- `transactions_df` (pd.DataFrame, optional): Transaction history

**Returns:**
- pd.DataFrame: Risk scores and categories

**Example:**
```python
from wekeza_analytics.analytics import PredictiveAnalytics

analytics = PredictiveAnalytics()
risk_scores = analytics.calculate_credit_risk_score(customers_df, transactions_df)
high_risk = risk_scores[risk_scores['risk_category'] == 'High Risk']
```

##### `predict_customer_churn(customers_df, transactions_df, train_model=False)`

Predict customer churn probability.

**Parameters:**
- `customers_df` (pd.DataFrame): Customer data
- `transactions_df` (pd.DataFrame): Transaction history
- `train_model` (bool): Whether to train the model

**Returns:**
- pd.DataFrame: Churn predictions

##### `forecast_transaction_volume(transactions_df, periods=30)`

Forecast transaction volume.

**Parameters:**
- `transactions_df` (pd.DataFrame): Historical transaction data
- `periods` (int): Number of periods to forecast

**Returns:**
- pd.DataFrame: Forecasted values

##### `identify_high_value_customers(customers_df, transactions_df, top_n=100)`

Identify high-value customers.

**Parameters:**
- `customers_df` (pd.DataFrame): Customer data
- `transactions_df` (pd.DataFrame): Transaction history
- `top_n` (int): Number of top customers to return

**Returns:**
- pd.DataFrame: High-value customers

---

## Workflows

### `AnalyticsWorkflow`

Orchestrates analytics workflows.

#### Methods

##### `run_full_analysis(customers_df, transactions_df, accounts_df)`

Run comprehensive analytics workflow.

**Parameters:**
- `customers_df` (pd.DataFrame): Customer data
- `transactions_df` (pd.DataFrame): Transaction data
- `accounts_df` (pd.DataFrame): Account data

**Returns:**
- dict: Complete analysis results

**Example:**
```python
from wekeza_analytics.workflows import AnalyticsWorkflow

workflow = AnalyticsWorkflow()
results = workflow.run_full_analysis(customers_df, transactions_df, accounts_df)
```

##### `run_customer_workflow(customers_df, transactions_df)`

Run customer-focused workflow.

##### `run_transaction_workflow(transactions_df)`

Run transaction-focused workflow.

##### `run_financial_workflow(transactions_df, accounts_df, customers_df)`

Run financial metrics workflow.

##### `run_predictive_workflow(customers_df, transactions_df)`

Run predictive analytics workflow.

---

## Utilities

### `DataGenerator`

Generate sample data for testing.

#### Methods

##### `generate_customers(n_customers=1000)`

Generate sample customer data.

**Parameters:**
- `n_customers` (int): Number of customers to generate

**Returns:**
- pd.DataFrame: Customer data

**Example:**
```python
from wekeza_analytics.utils import DataGenerator

generator = DataGenerator(seed=42)
customers = generator.generate_customers(n_customers=500)
```

##### `generate_transactions(customers_df, avg_transactions_per_customer=50)`

Generate sample transaction data.

##### `generate_accounts(customers_df)`

Generate sample account data.

##### `generate_complete_dataset(n_customers=1000, avg_transactions_per_customer=50)`

Generate complete dataset.

**Returns:**
- dict: Dictionary with 'customers', 'transactions', 'accounts' DataFrames

---

### `AnalyticsVisualizer`

Create visualizations for analytics results.

#### Methods

##### `plot_customer_segments(rfm_df, save_path=None)`

Visualize customer segments.

**Parameters:**
- `rfm_df` (pd.DataFrame): RFM analysis results
- `save_path` (str, optional): Path to save the plot

**Example:**
```python
from wekeza_analytics.utils import AnalyticsVisualizer

visualizer = AnalyticsVisualizer()
visualizer.plot_customer_segments(rfm_df, save_path='segments.png')
```

##### `plot_transaction_trends(transactions_df, save_path=None)`

Visualize transaction trends.

##### `plot_financial_metrics(metrics, save_path=None)`

Visualize financial metrics.

##### `plot_risk_analysis(risk_df, save_path=None)`

Visualize risk analysis.

##### `create_summary_report(results, output_path='analytics_report.txt')`

Create text summary report.

---

## Data Models

### `Customer`

Pydantic model for customer data.

**Fields:**
- `customer_id` (str): Unique identifier
- `name` (str): Customer name
- `email` (str): Email address
- `phone` (str, optional): Phone number
- `account_type` (str): Account type
- `registration_date` (datetime): Registration date
- `credit_score` (int, optional): Credit score (300-850)
- `monthly_income` (float, optional): Monthly income
- `country` (str): Country of residence
- `risk_category` (str, optional): Risk category

### `Transaction`

Pydantic model for transaction data.

**Fields:**
- `transaction_id` (str): Unique identifier
- `customer_id` (str): Customer identifier
- `transaction_date` (datetime): Transaction date/time
- `amount` (float): Transaction amount
- `transaction_type` (str): Type (debit, credit, transfer)
- `category` (str): Category
- `merchant` (str, optional): Merchant name
- `location` (str, optional): Location
- `status` (str): Status (completed, pending, failed)
- `is_fraudulent` (bool): Fraud flag

### `Account`

Pydantic model for account data.

**Fields:**
- `account_id` (str): Unique identifier
- `customer_id` (str): Customer identifier
- `account_type` (str): Account type
- `balance` (float): Current balance
- `currency` (str): Currency code
- `opening_date` (datetime): Opening date
- `status` (str): Status (active, dormant, closed)
- `interest_rate` (float, optional): Interest rate

---

## Error Handling

All methods handle errors gracefully and return informative error messages:

```python
try:
    results = workflow.run_full_analysis(customers_df, transactions_df, accounts_df)
except ValueError as e:
    print(f"Data validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance Tips

1. **Use vectorized operations**: All analytics use pandas/numpy for performance
2. **Batch processing**: For large datasets, process in batches
3. **Filter data**: Filter unnecessary data before analysis
4. **Use appropriate periods**: Choose appropriate aggregation periods
5. **Cache results**: Cache expensive computations when possible

## Support

For additional help:
- Check the README.md for examples
- Run the demo script: `python examples/demo.py`
- View inline documentation: `help(CustomerAnalytics)`
- Open an issue on GitHub
