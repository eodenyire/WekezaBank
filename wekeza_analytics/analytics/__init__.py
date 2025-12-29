"""
Analytics modules for Wekeza Bank
"""

from wekeza_analytics.analytics.customer_analytics import CustomerAnalytics
from wekeza_analytics.analytics.transaction_analytics import TransactionAnalytics
from wekeza_analytics.analytics.financial_metrics import FinancialMetrics
from wekeza_analytics.analytics.predictive_analytics import PredictiveAnalytics

__all__ = [
    'CustomerAnalytics',
    'TransactionAnalytics',
    'FinancialMetrics',
    'PredictiveAnalytics',
]
