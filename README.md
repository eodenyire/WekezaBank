# Wekeza Bank Advanced Analytics Framework

A comprehensive Python-based analytics framework for banking operations, providing powerful tools for customer analytics, transaction analysis, financial metrics, and predictive modeling.

## 🌟 Features

### Customer Analytics
- **RFM Analysis**: Segment customers based on Recency, Frequency, and Monetary value
- **Customer Segmentation**: K-means clustering for advanced segmentation
- **Customer Lifetime Value (CLV)**: Calculate and predict customer value
- **Churn Risk Analysis**: Identify customers at risk of churning
- **Demographics Analysis**: Comprehensive demographic insights

### Transaction Analytics
- **Pattern Analysis**: Identify spending patterns and trends
- **Anomaly Detection**: Detect unusual transactions using machine learning
- **Fraud Detection**: Analyze fraud patterns and risk factors
- **Velocity Analysis**: Track transaction frequency and patterns
- **Merchant Analysis**: Insights into merchant transactions

### Financial Metrics
- **KPI Dashboard**: Comprehensive key performance indicators
- **Revenue Analysis**: Track and forecast revenue streams
- **Profitability Metrics**: Calculate margins and profitability
- **Portfolio Analysis**: Monitor assets under management
- **Liquidity Metrics**: Track deposits and cash positions
- **Account Health**: Monitor account status and balances

### Predictive Analytics
- **Credit Risk Scoring**: Assess customer credit risk
- **Churn Prediction**: Predict customer churn probability
- **Transaction Forecasting**: Forecast future transaction volumes
- **High-Value Customer Identification**: Identify top customers
- **Next Transaction Prediction**: Predict customer behavior

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install from source

```bash
git clone https://github.com/eodenyire/WekezaBank.git
cd WekezaBank
pip install -e .
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Basic Usage

```python
from wekeza_analytics.workflows import AnalyticsWorkflow
from wekeza_analytics.utils import DataGenerator
import pandas as pd

# Generate sample data
generator = DataGenerator(seed=42)
data = generator.generate_complete_dataset(
    n_customers=1000,
    avg_transactions_per_customer=50
)

# Initialize workflow
workflow = AnalyticsWorkflow()

# Run comprehensive analysis
results = workflow.run_full_analysis(
    customers_df=data['customers'],
    transactions_df=data['transactions'],
    accounts_df=data['accounts']
)

# Access results
print(results['customer_analytics']['demographics'])
print(results['financial_metrics']['kpis'])
```

### Customer Analytics Example

```python
from wekeza_analytics.analytics import CustomerAnalytics

analytics = CustomerAnalytics()

# RFM Analysis
rfm_results = analytics.rfm_analysis(transactions_df)

# Customer Segmentation
segmented_customers, stats = analytics.customer_segmentation(customers_df, n_clusters=4)

# Calculate CLV
clv_results = analytics.calculate_customer_lifetime_value(
    transactions_df, 
    customers_df
)

# Churn Risk Analysis
churn_risks = analytics.churn_risk_analysis(transactions_df, customers_df)
```

### Transaction Analytics Example

```python
from wekeza_analytics.analytics import TransactionAnalytics

analytics = TransactionAnalytics()

# Get transaction summary
summary = analytics.transaction_summary(transactions_df, period='monthly')

# Detect anomalies
anomalies = analytics.detect_anomalies(transactions_df)

# Analyze spending patterns
patterns = analytics.spending_pattern_analysis(transactions_df)

# Fraud analysis
fraud_stats = analytics.fraud_detection_analysis(transactions_df)
```

### Financial Metrics Example

```python
from wekeza_analytics.analytics import FinancialMetrics

metrics = FinancialMetrics()

# Calculate KPIs
kpis = metrics.calculate_kpis(transactions_df, accounts_df, customers_df)

# Revenue metrics
revenue = metrics.calculate_revenue_metrics(transactions_df)

# Portfolio metrics
portfolio = metrics.calculate_portfolio_metrics(accounts_df, transactions_df)

# Profitability
profitability = metrics.calculate_profitability_metrics(transactions_df, accounts_df)
```

### Predictive Analytics Example

```python
from wekeza_analytics.analytics import PredictiveAnalytics

analytics = PredictiveAnalytics()

# Credit risk scoring
risk_scores = analytics.calculate_credit_risk_score(customers_df, transactions_df)

# Churn prediction
churn_predictions = analytics.predict_customer_churn(customers_df, transactions_df)

# Transaction forecasting
forecast = analytics.forecast_transaction_volume(transactions_df, periods=30)

# High-value customers
high_value = analytics.identify_high_value_customers(
    customers_df, 
    transactions_df, 
    top_n=100
)
```

### Workflow Orchestration

```python
from wekeza_analytics.workflows import AnalyticsWorkflow

workflow = AnalyticsWorkflow()

# Run specific workflows
customer_results = workflow.run_customer_workflow(customers_df, transactions_df)
transaction_results = workflow.run_transaction_workflow(transactions_df)
financial_results = workflow.run_financial_workflow(transactions_df, accounts_df, customers_df)
predictive_results = workflow.run_predictive_workflow(customers_df, transactions_df)

# Run full analysis
full_results = workflow.run_full_analysis(customers_df, transactions_df, accounts_df)
```

## 📊 Visualization

```python
from wekeza_analytics.utils import AnalyticsVisualizer

visualizer = AnalyticsVisualizer()

# Create visualizations
visualizer.plot_customer_segments(rfm_df, save_path='customer_segments.png')
visualizer.plot_transaction_trends(transactions_df, save_path='transactions.png')
visualizer.plot_financial_metrics(metrics, save_path='financial.png')
visualizer.plot_risk_analysis(risk_df, save_path='risk.png')

# Generate summary report
visualizer.create_summary_report(results, output_path='report.txt')
```

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=wekeza_analytics --cov-report=html

# Run specific test file
pytest tests/test_analytics.py -v
```

## 📁 Project Structure

```
WekezaBank/
├── wekeza_analytics/
│   ├── __init__.py
│   ├── models/              # Data models
│   │   └── __init__.py
│   ├── analytics/           # Analytics modules
│   │   ├── __init__.py
│   │   ├── customer_analytics.py
│   │   ├── transaction_analytics.py
│   │   ├── financial_metrics.py
│   │   └── predictive_analytics.py
│   ├── workflows/           # Workflow orchestration
│   │   └── __init__.py
│   └── utils/               # Utilities
│       ├── __init__.py
│       ├── data_generator.py
│       └── visualization.py
├── tests/                   # Test suite
│   └── test_analytics.py
├── examples/                # Example scripts
│   └── demo.py
├── requirements.txt
├── setup.py
└── README.md
```

## 🎯 Use Cases

### Banking Operations
- Monitor daily transaction volumes and patterns
- Track account health and customer engagement
- Identify high-value customers for targeted marketing

### Risk Management
- Detect fraudulent transactions in real-time
- Score customer credit risk
- Identify customers at risk of churning

### Business Intelligence
- Generate comprehensive KPI dashboards
- Track revenue and profitability metrics
- Analyze customer segments and behavior

### Predictive Modeling
- Forecast transaction volumes
- Predict customer lifetime value
- Anticipate customer churn

## 🔧 Configuration

The framework is designed to work out-of-the-box with sensible defaults, but can be customized:

```python
# Custom analytics parameters
analytics = CustomerAnalytics()
rfm_results = analytics.rfm_analysis(
    transactions_df,
    reference_date=custom_date
)

# Custom segmentation
segmented, stats = analytics.customer_segmentation(
    customers_df,
    n_clusters=5  # Custom number of clusters
)

# Custom risk thresholds
churn_risks = analytics.churn_risk_analysis(
    transactions_df,
    customers_df,
    inactive_days=60  # Custom threshold
)
```

## 📈 Performance

The framework is optimized for performance:
- Vectorized operations using NumPy and Pandas
- Efficient data structures
- Parallel processing capabilities
- Scalable to millions of transactions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋 Support

For questions or issues, please open an issue on GitHub.

## 🎓 Example Demo

Run the included demo to see the framework in action:

```bash
cd examples
python demo.py
```

This will:
1. Generate sample banking data
2. Run comprehensive analytics
3. Create visualizations
4. Generate reports

Output will be saved to the `output/` directory.

## 📚 Documentation

For detailed API documentation, see the docstrings in each module:

```python
help(CustomerAnalytics)
help(TransactionAnalytics)
help(FinancialMetrics)
help(PredictiveAnalytics)
```

## 🌐 Requirements

- pandas >= 2.0.0
- numpy >= 1.24.0
- scikit-learn >= 1.3.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- plotly >= 5.14.0
- statsmodels >= 0.14.0
- pydantic >= 2.0.0

See `requirements.txt` for the complete list.

---

**Wekeza Bank Analytics Framework** - Empowering data-driven banking decisions 🚀