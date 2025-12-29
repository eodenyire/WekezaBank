"""
Tests for the Wekeza Bank Analytics Framework
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta

from wekeza_analytics.analytics import (
    CustomerAnalytics,
    TransactionAnalytics,
    FinancialMetrics,
    PredictiveAnalytics,
)
from wekeza_analytics.workflows import AnalyticsWorkflow
from wekeza_analytics.utils import DataGenerator


@pytest.fixture
def sample_data():
    """Generate sample data for testing"""
    generator = DataGenerator(seed=42)
    return generator.generate_complete_dataset(n_customers=100, avg_transactions_per_customer=20)


class TestCustomerAnalytics:
    """Test customer analytics functionality"""
    
    def test_rfm_analysis(self, sample_data):
        """Test RFM analysis"""
        analytics = CustomerAnalytics()
        transactions_df = sample_data['transactions']
        
        rfm_result = analytics.rfm_analysis(transactions_df)
        
        assert 'customer_id' in rfm_result.columns
        assert 'recency' in rfm_result.columns
        assert 'frequency' in rfm_result.columns
        assert 'monetary' in rfm_result.columns
        assert 'segment' in rfm_result.columns
        assert len(rfm_result) > 0
    
    def test_customer_segmentation(self, sample_data):
        """Test customer segmentation"""
        analytics = CustomerAnalytics()
        customers_df = sample_data['customers']
        
        segmented_df, stats = analytics.customer_segmentation(customers_df, n_clusters=4)
        
        assert 'segment' in segmented_df.columns
        assert len(stats) == 4
        assert all('count' in stat for stat in stats.values())
    
    def test_customer_lifetime_value(self, sample_data):
        """Test CLV calculation"""
        analytics = CustomerAnalytics()
        transactions_df = sample_data['transactions']
        customers_df = sample_data['customers']
        
        clv_result = analytics.calculate_customer_lifetime_value(
            transactions_df, customers_df
        )
        
        assert 'customer_id' in clv_result.columns
        assert 'clv' in clv_result.columns
        assert len(clv_result) > 0
    
    def test_churn_risk_analysis(self, sample_data):
        """Test churn risk analysis"""
        analytics = CustomerAnalytics()
        transactions_df = sample_data['transactions']
        customers_df = sample_data['customers']
        
        churn_result = analytics.churn_risk_analysis(
            transactions_df, customers_df
        )
        
        assert 'customer_id' in churn_result.columns
        assert 'churn_risk_score' in churn_result.columns
        assert 'churn_risk_category' in churn_result.columns
    
    def test_demographics_analysis(self, sample_data):
        """Test demographics analysis"""
        analytics = CustomerAnalytics()
        customers_df = sample_data['customers']
        
        demographics = analytics.customer_demographics_analysis(customers_df)
        
        assert 'total_customers' in demographics
        assert demographics['total_customers'] == len(customers_df)
        assert 'by_account_type' in demographics
        assert 'by_country' in demographics


class TestTransactionAnalytics:
    """Test transaction analytics functionality"""
    
    def test_transaction_summary(self, sample_data):
        """Test transaction summary"""
        analytics = TransactionAnalytics()
        transactions_df = sample_data['transactions']
        
        summary = analytics.transaction_summary(transactions_df, period='daily')
        
        assert 'date' in summary.columns
        assert 'transaction_count' in summary.columns
        assert 'total_amount' in summary.columns
        assert len(summary) > 0
    
    def test_anomaly_detection(self, sample_data):
        """Test anomaly detection"""
        analytics = TransactionAnalytics()
        transactions_df = sample_data['transactions']
        
        result = analytics.detect_anomalies(transactions_df)
        
        assert 'is_anomaly' in result.columns
        assert 'anomaly_score' in result.columns
    
    def test_fraud_detection_analysis(self, sample_data):
        """Test fraud detection analysis"""
        analytics = TransactionAnalytics()
        transactions_df = sample_data['transactions']
        
        fraud_stats = analytics.fraud_detection_analysis(transactions_df)
        
        assert 'total_transactions' in fraud_stats
        assert 'fraudulent_count' in fraud_stats
        assert 'fraud_rate' in fraud_stats
    
    def test_spending_pattern_analysis(self, sample_data):
        """Test spending pattern analysis"""
        analytics = TransactionAnalytics()
        transactions_df = sample_data['transactions']
        
        patterns = analytics.spending_pattern_analysis(transactions_df)
        
        assert 'total_spending' in patterns
        assert 'avg_transaction_size' in patterns
        assert 'transaction_count' in patterns
    
    def test_transaction_metrics(self, sample_data):
        """Test transaction metrics calculation"""
        analytics = TransactionAnalytics()
        transactions_df = sample_data['transactions']
        
        metrics = analytics.calculate_transaction_metrics(transactions_df)
        
        assert 'total_transactions' in metrics
        assert 'total_volume' in metrics
        assert 'avg_transaction_size' in metrics


class TestFinancialMetrics:
    """Test financial metrics functionality"""
    
    def test_revenue_metrics(self, sample_data):
        """Test revenue metrics calculation"""
        metrics = FinancialMetrics()
        transactions_df = sample_data['transactions']
        
        revenue = metrics.calculate_revenue_metrics(transactions_df)
        
        assert 'total_revenue' in revenue
        assert 'avg_transaction_revenue' in revenue
        assert 'transaction_count' in revenue
    
    def test_account_health_metrics(self, sample_data):
        """Test account health metrics"""
        metrics = FinancialMetrics()
        accounts_df = sample_data['accounts']
        
        health = metrics.calculate_account_health_metrics(accounts_df)
        
        assert 'total_accounts' in health
        assert 'total_balance' in health
        assert 'avg_balance' in health
    
    def test_portfolio_metrics(self, sample_data):
        """Test portfolio metrics"""
        metrics = FinancialMetrics()
        accounts_df = sample_data['accounts']
        transactions_df = sample_data['transactions']
        
        portfolio = metrics.calculate_portfolio_metrics(
            accounts_df, transactions_df
        )
        
        assert 'total_aum' in portfolio
        assert 'account_count' in portfolio
    
    def test_kpis(self, sample_data):
        """Test KPI calculation"""
        metrics = FinancialMetrics()
        transactions_df = sample_data['transactions']
        accounts_df = sample_data['accounts']
        customers_df = sample_data['customers']
        
        kpis = metrics.calculate_kpis(
            transactions_df, accounts_df, customers_df
        )
        
        assert 'customer_metrics' in kpis
        assert 'account_metrics' in kpis
        assert 'transaction_metrics' in kpis
        assert 'profitability' in kpis


class TestPredictiveAnalytics:
    """Test predictive analytics functionality"""
    
    def test_credit_risk_score(self, sample_data):
        """Test credit risk scoring"""
        analytics = PredictiveAnalytics()
        customers_df = sample_data['customers']
        transactions_df = sample_data['transactions']
        
        risk_scores = analytics.calculate_credit_risk_score(
            customers_df, transactions_df
        )
        
        assert 'customer_id' in risk_scores.columns
        assert 'credit_risk_score' in risk_scores.columns
        assert 'risk_category' in risk_scores.columns
    
    def test_churn_prediction(self, sample_data):
        """Test churn prediction"""
        analytics = PredictiveAnalytics()
        customers_df = sample_data['customers']
        transactions_df = sample_data['transactions']
        
        predictions = analytics.predict_customer_churn(
            customers_df, transactions_df
        )
        
        assert 'customer_id' in predictions.columns
        assert 'churn_probability' in predictions.columns
        assert 'churn_risk' in predictions.columns
    
    def test_transaction_forecast(self, sample_data):
        """Test transaction volume forecasting"""
        analytics = PredictiveAnalytics()
        transactions_df = sample_data['transactions']
        
        forecast = analytics.forecast_transaction_volume(
            transactions_df, periods=30
        )
        
        assert 'date' in forecast.columns
        assert 'forecasted_transaction_count' in forecast.columns
        assert len(forecast) == 30
    
    def test_high_value_customers(self, sample_data):
        """Test high-value customer identification"""
        analytics = PredictiveAnalytics()
        customers_df = sample_data['customers']
        transactions_df = sample_data['transactions']
        
        high_value = analytics.identify_high_value_customers(
            customers_df, transactions_df, top_n=10
        )
        
        assert len(high_value) <= 10
        assert 'customer_id' in high_value.columns
        assert 'predicted_clv' in high_value.columns


class TestAnalyticsWorkflow:
    """Test analytics workflow orchestration"""
    
    def test_full_workflow(self, sample_data):
        """Test full analytics workflow"""
        workflow = AnalyticsWorkflow()
        
        results = workflow.run_full_analysis(
            customers_df=sample_data['customers'],
            transactions_df=sample_data['transactions'],
            accounts_df=sample_data['accounts']
        )
        
        assert 'timestamp' in results
        assert 'customer_analytics' in results
        assert 'transaction_analytics' in results
        assert 'financial_metrics' in results
        assert 'predictive_analytics' in results
    
    def test_customer_workflow(self, sample_data):
        """Test customer-focused workflow"""
        workflow = AnalyticsWorkflow()
        
        results = workflow.run_customer_workflow(
            customers_df=sample_data['customers'],
            transactions_df=sample_data['transactions']
        )
        
        assert 'timestamp' in results
        assert 'demographics' in results
    
    def test_transaction_workflow(self, sample_data):
        """Test transaction-focused workflow"""
        workflow = AnalyticsWorkflow()
        
        results = workflow.run_transaction_workflow(
            transactions_df=sample_data['transactions']
        )
        
        assert 'timestamp' in results
        assert 'summary' in results
        assert 'metrics' in results
    
    def test_financial_workflow(self, sample_data):
        """Test financial metrics workflow"""
        workflow = AnalyticsWorkflow()
        
        results = workflow.run_financial_workflow(
            transactions_df=sample_data['transactions'],
            accounts_df=sample_data['accounts'],
            customers_df=sample_data['customers']
        )
        
        assert 'timestamp' in results
        assert 'kpis' in results
    
    def test_predictive_workflow(self, sample_data):
        """Test predictive analytics workflow"""
        workflow = AnalyticsWorkflow()
        
        results = workflow.run_predictive_workflow(
            customers_df=sample_data['customers'],
            transactions_df=sample_data['transactions']
        )
        
        assert 'timestamp' in results
        assert 'credit_risk_scores' in results
        assert 'churn_predictions' in results


class TestDataGenerator:
    """Test data generation utilities"""
    
    def test_generate_customers(self):
        """Test customer data generation"""
        generator = DataGenerator(seed=42)
        customers = generator.generate_customers(n_customers=50)
        
        assert len(customers) == 50
        assert 'customer_id' in customers.columns
        assert 'name' in customers.columns
        assert 'email' in customers.columns
    
    def test_generate_transactions(self):
        """Test transaction data generation"""
        generator = DataGenerator(seed=42)
        customers = generator.generate_customers(n_customers=10)
        transactions = generator.generate_transactions(customers, avg_transactions_per_customer=20)
        
        assert len(transactions) > 0
        assert 'transaction_id' in transactions.columns
        assert 'customer_id' in transactions.columns
        assert 'amount' in transactions.columns
    
    def test_generate_accounts(self):
        """Test account data generation"""
        generator = DataGenerator(seed=42)
        customers = generator.generate_customers(n_customers=10)
        accounts = generator.generate_accounts(customers)
        
        assert len(accounts) > 0
        assert 'account_id' in accounts.columns
        assert 'customer_id' in accounts.columns
        assert 'balance' in accounts.columns
    
    def test_generate_complete_dataset(self):
        """Test complete dataset generation"""
        generator = DataGenerator(seed=42)
        data = generator.generate_complete_dataset(n_customers=50, avg_transactions_per_customer=10)
        
        assert 'customers' in data
        assert 'transactions' in data
        assert 'accounts' in data
        assert len(data['customers']) == 50
        assert len(data['transactions']) > 0
        assert len(data['accounts']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
