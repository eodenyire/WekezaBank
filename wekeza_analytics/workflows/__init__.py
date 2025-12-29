"""
Analytics Workflow Orchestration

Provides workflow management for running analytics pipelines
"""

import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime
from wekeza_analytics.analytics import (
    CustomerAnalytics,
    TransactionAnalytics,
    FinancialMetrics,
    PredictiveAnalytics,
)


class AnalyticsWorkflow:
    """
    Orchestrates analytics workflows for Wekeza Bank
    """
    
    def __init__(self):
        self.customer_analytics = CustomerAnalytics()
        self.transaction_analytics = TransactionAnalytics()
        self.financial_metrics = FinancialMetrics()
        self.predictive_analytics = PredictiveAnalytics()
        self.results = {}
        
    def run_full_analysis(
        self,
        customers_df: pd.DataFrame,
        transactions_df: pd.DataFrame,
        accounts_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Run comprehensive analytics workflow
        
        Args:
            customers_df: Customer data
            transactions_df: Transaction data
            accounts_df: Account data
            
        Returns:
            Dictionary with all analysis results
        """
        print("Starting full analytics workflow...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'customer_analytics': {},
            'transaction_analytics': {},
            'financial_metrics': {},
            'predictive_analytics': {},
        }
        
        # Customer Analytics
        print("Running customer analytics...")
        try:
            results['customer_analytics']['demographics'] = (
                self.customer_analytics.customer_demographics_analysis(customers_df)
            )
            
            if len(transactions_df) > 0:
                results['customer_analytics']['rfm'] = (
                    self.customer_analytics.rfm_analysis(transactions_df)
                ).to_dict('records')
                
                results['customer_analytics']['clv'] = (
                    self.customer_analytics.calculate_customer_lifetime_value(
                        transactions_df, customers_df
                    )
                ).to_dict('records')
                
                results['customer_analytics']['churn_risk'] = (
                    self.customer_analytics.churn_risk_analysis(
                        transactions_df, customers_df
                    )
                ).to_dict('records')
        except Exception as e:
            results['customer_analytics']['error'] = str(e)
        
        # Transaction Analytics
        print("Running transaction analytics...")
        try:
            results['transaction_analytics']['summary'] = (
                self.transaction_analytics.transaction_summary(transactions_df)
            ).to_dict('records')
            
            results['transaction_analytics']['metrics'] = (
                self.transaction_analytics.calculate_transaction_metrics(transactions_df)
            )
            
            results['transaction_analytics']['spending_patterns'] = (
                self.transaction_analytics.spending_pattern_analysis(transactions_df)
            )
            
            if 'is_fraudulent' in transactions_df:
                results['transaction_analytics']['fraud_analysis'] = (
                    self.transaction_analytics.fraud_detection_analysis(transactions_df)
                )
        except Exception as e:
            results['transaction_analytics']['error'] = str(e)
        
        # Financial Metrics
        print("Running financial metrics...")
        try:
            results['financial_metrics']['kpis'] = (
                self.financial_metrics.calculate_kpis(
                    transactions_df, accounts_df, customers_df
                )
            )
            
            results['financial_metrics']['portfolio'] = (
                self.financial_metrics.calculate_portfolio_metrics(
                    accounts_df, transactions_df
                )
            )
            
            results['financial_metrics']['liquidity'] = (
                self.financial_metrics.calculate_liquidity_metrics(accounts_df)
            )
        except Exception as e:
            results['financial_metrics']['error'] = str(e)
        
        # Predictive Analytics
        print("Running predictive analytics...")
        try:
            results['predictive_analytics']['credit_risk'] = (
                self.predictive_analytics.calculate_credit_risk_score(
                    customers_df, transactions_df
                )
            ).to_dict('records')
            
            results['predictive_analytics']['churn_prediction'] = (
                self.predictive_analytics.predict_customer_churn(
                    customers_df, transactions_df
                )
            ).to_dict('records')
            
            results['predictive_analytics']['high_value_customers'] = (
                self.predictive_analytics.identify_high_value_customers(
                    customers_df, transactions_df, top_n=20
                )
            ).to_dict('records')
            
            if len(transactions_df) > 0:
                results['predictive_analytics']['volume_forecast'] = (
                    self.predictive_analytics.forecast_transaction_volume(
                        transactions_df, periods=30
                    )
                ).to_dict('records')
        except Exception as e:
            results['predictive_analytics']['error'] = str(e)
        
        self.results = results
        print("Analytics workflow completed!")
        
        return results
    
    def run_customer_workflow(
        self,
        customers_df: pd.DataFrame,
        transactions_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Run customer-focused analytics workflow
        
        Args:
            customers_df: Customer data
            transactions_df: Transaction data
            
        Returns:
            Dictionary with customer analysis results
        """
        print("Running customer analytics workflow...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'demographics': self.customer_analytics.customer_demographics_analysis(customers_df),
        }
        
        if len(transactions_df) > 0:
            results['rfm_analysis'] = self.customer_analytics.rfm_analysis(
                transactions_df
            ).to_dict('records')
            
            results['segmentation'], results['segment_stats'] = (
                self.customer_analytics.customer_segmentation(customers_df)
            )
            results['segmentation'] = results['segmentation'].to_dict('records')
            
            results['lifetime_value'] = (
                self.customer_analytics.calculate_customer_lifetime_value(
                    transactions_df, customers_df
                )
            ).to_dict('records')
            
            results['churn_risk'] = (
                self.customer_analytics.churn_risk_analysis(
                    transactions_df, customers_df
                )
            ).to_dict('records')
        
        return results
    
    def run_transaction_workflow(
        self,
        transactions_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Run transaction-focused analytics workflow
        
        Args:
            transactions_df: Transaction data
            
        Returns:
            Dictionary with transaction analysis results
        """
        print("Running transaction analytics workflow...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.transaction_analytics.transaction_summary(
                transactions_df
            ).to_dict('records'),
            'metrics': self.transaction_analytics.calculate_transaction_metrics(
                transactions_df
            ),
            'spending_patterns': self.transaction_analytics.spending_pattern_analysis(
                transactions_df
            ),
        }
        
        # Anomaly detection
        with_anomalies = self.transaction_analytics.detect_anomalies(transactions_df)
        results['anomalies'] = with_anomalies[
            with_anomalies['is_anomaly']
        ].to_dict('records')
        
        # Fraud analysis if available
        if 'is_fraudulent' in transactions_df:
            results['fraud_analysis'] = (
                self.transaction_analytics.fraud_detection_analysis(transactions_df)
            )
        
        return results
    
    def run_financial_workflow(
        self,
        transactions_df: pd.DataFrame,
        accounts_df: pd.DataFrame,
        customers_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Run financial metrics workflow
        
        Args:
            transactions_df: Transaction data
            accounts_df: Account data
            customers_df: Customer data
            
        Returns:
            Dictionary with financial analysis results
        """
        print("Running financial metrics workflow...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'kpis': self.financial_metrics.calculate_kpis(
                transactions_df, accounts_df, customers_df
            ),
            'revenue': self.financial_metrics.calculate_revenue_metrics(
                transactions_df
            ),
            'portfolio': self.financial_metrics.calculate_portfolio_metrics(
                accounts_df, transactions_df
            ),
            'account_health': self.financial_metrics.calculate_account_health_metrics(
                accounts_df
            ),
            'liquidity': self.financial_metrics.calculate_liquidity_metrics(
                accounts_df
            ),
            'profitability': self.financial_metrics.calculate_profitability_metrics(
                transactions_df, accounts_df
            ),
        }
        
        return results
    
    def run_predictive_workflow(
        self,
        customers_df: pd.DataFrame,
        transactions_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Run predictive analytics workflow
        
        Args:
            customers_df: Customer data
            transactions_df: Transaction data
            
        Returns:
            Dictionary with predictive analysis results
        """
        print("Running predictive analytics workflow...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'credit_risk_scores': self.predictive_analytics.calculate_credit_risk_score(
                customers_df, transactions_df
            ).to_dict('records'),
            'churn_predictions': self.predictive_analytics.predict_customer_churn(
                customers_df, transactions_df
            ).to_dict('records'),
            'high_value_customers': self.predictive_analytics.identify_high_value_customers(
                customers_df, transactions_df, top_n=20
            ).to_dict('records'),
        }
        
        if len(transactions_df) > 0:
            results['transaction_forecast'] = (
                self.predictive_analytics.forecast_transaction_volume(
                    transactions_df, periods=30
                )
            ).to_dict('records')
        
        return results
