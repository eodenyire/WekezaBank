"""
Wekeza Bank Advanced Analytics Framework

A comprehensive analytics framework for banking operations including:
- Customer analytics and segmentation
- Transaction pattern analysis
- Financial metrics and KPIs
- Predictive analytics and risk scoring
- Automated reporting and visualization
"""

__version__ = "0.1.0"
__author__ = "Wekeza Bank"

from wekeza_analytics.analytics import (
    CustomerAnalytics,
    TransactionAnalytics,
    FinancialMetrics,
    PredictiveAnalytics,
)

from wekeza_analytics.workflows import AnalyticsWorkflow

__all__ = [
    "CustomerAnalytics",
    "TransactionAnalytics",
    "FinancialMetrics",
    "PredictiveAnalytics",
    "AnalyticsWorkflow",
]
