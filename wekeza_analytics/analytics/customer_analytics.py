"""
Customer Analytics Module

Provides comprehensive customer analytics including:
- Customer segmentation (RFM analysis, clustering)
- Lifetime value calculation
- Churn prediction
- Customer behavior analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class CustomerAnalytics:
    """Customer analytics engine for Wekeza Bank"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        
    def rfm_analysis(
        self, 
        transactions_df: pd.DataFrame,
        reference_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Perform RFM (Recency, Frequency, Monetary) analysis
        
        Args:
            transactions_df: DataFrame with customer transactions
            reference_date: Reference date for recency calculation
            
        Returns:
            DataFrame with RFM scores for each customer
        """
        if reference_date is None:
            reference_date = datetime.now()
            
        # Calculate RFM metrics
        rfm = transactions_df.groupby('customer_id').agg({
            'transaction_date': lambda x: (reference_date - x.max()).days,  # Recency
            'transaction_id': 'count',  # Frequency
            'amount': 'sum'  # Monetary
        }).reset_index()
        
        rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
        
        # Calculate RFM scores (1-5 scale)
        rfm['r_score'] = pd.qcut(rfm['recency'], q=5, labels=[5, 4, 3, 2, 1], duplicates='drop')
        rfm['f_score'] = pd.qcut(rfm['frequency'], q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
        rfm['m_score'] = pd.qcut(rfm['monetary'], q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
        
        # Calculate RFM score
        rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)
        
        # Segment customers
        rfm['segment'] = rfm.apply(self._assign_rfm_segment, axis=1)
        
        return rfm
    
    def _assign_rfm_segment(self, row) -> str:
        """Assign customer segment based on RFM scores"""
        r, f, m = int(row['r_score']), int(row['f_score']), int(row['m_score'])
        
        if r >= 4 and f >= 4 and m >= 4:
            return 'Champions'
        elif r >= 3 and f >= 3 and m >= 3:
            return 'Loyal Customers'
        elif r >= 4 and f <= 2:
            return 'New Customers'
        elif r <= 2 and f >= 4:
            return 'At Risk'
        elif r <= 2 and f <= 2 and m >= 4:
            return 'Cant Lose Them'
        elif r <= 2:
            return 'Lost'
        else:
            return 'Regular'
    
    def customer_segmentation(
        self,
        customers_df: pd.DataFrame,
        n_clusters: int = 4
    ) -> Tuple[pd.DataFrame, Dict]:
        """
        Perform customer segmentation using K-means clustering
        
        Args:
            customers_df: DataFrame with customer features
            n_clusters: Number of segments to create
            
        Returns:
            Tuple of (segmented customers DataFrame, cluster statistics)
        """
        # Select features for clustering
        feature_cols = ['credit_score', 'monthly_income']
        available_cols = [col for col in feature_cols if col in customers_df.columns]
        
        if not available_cols:
            raise ValueError("No suitable features found for clustering")
        
        # Prepare data
        X = customers_df[available_cols].fillna(customers_df[available_cols].median())
        X_scaled = self.scaler.fit_transform(X)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        customers_df['segment'] = kmeans.fit_predict(X_scaled)
        
        # Calculate segment statistics
        segment_stats = {}
        for segment_id in range(n_clusters):
            segment_data = customers_df[customers_df['segment'] == segment_id]
            segment_stats[f'Segment_{segment_id}'] = {
                'count': len(segment_data),
                'avg_credit_score': segment_data['credit_score'].mean() if 'credit_score' in segment_data else None,
                'avg_income': segment_data['monthly_income'].mean() if 'monthly_income' in segment_data else None,
            }
        
        return customers_df, segment_stats
    
    def calculate_customer_lifetime_value(
        self,
        transactions_df: pd.DataFrame,
        customers_df: pd.DataFrame,
        time_period_months: int = 12
    ) -> pd.DataFrame:
        """
        Calculate Customer Lifetime Value (CLV)
        
        Args:
            transactions_df: Transaction history
            customers_df: Customer information
            time_period_months: Time period for CLV calculation
            
        Returns:
            DataFrame with CLV for each customer
        """
        # Calculate total value per customer
        customer_value = transactions_df.groupby('customer_id').agg({
            'amount': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        
        customer_value.columns = ['customer_id', 'total_value', 'transaction_count']
        
        # Merge with customer data
        clv_df = customers_df.merge(customer_value, on='customer_id', how='left')
        
        # Calculate average transaction value
        clv_df['avg_transaction_value'] = clv_df['total_value'] / clv_df['transaction_count']
        
        # Calculate purchase frequency (transactions per month)
        clv_df['purchase_frequency'] = clv_df['transaction_count'] / time_period_months
        
        # Simple CLV calculation: avg_value * frequency * time_period
        clv_df['clv'] = (
            clv_df['avg_transaction_value'] * 
            clv_df['purchase_frequency'] * 
            time_period_months
        )
        
        return clv_df[['customer_id', 'clv', 'avg_transaction_value', 'purchase_frequency']]
    
    def churn_risk_analysis(
        self,
        transactions_df: pd.DataFrame,
        customers_df: pd.DataFrame,
        inactive_days: int = 90
    ) -> pd.DataFrame:
        """
        Analyze customer churn risk
        
        Args:
            transactions_df: Transaction history
            customers_df: Customer information
            inactive_days: Days of inactivity to consider at-risk
            
        Returns:
            DataFrame with churn risk scores
        """
        # Calculate days since last transaction
        last_transaction = transactions_df.groupby('customer_id')['transaction_date'].max().reset_index()
        last_transaction.columns = ['customer_id', 'last_transaction_date']
        
        reference_date = datetime.now()
        last_transaction['days_since_last_transaction'] = (
            reference_date - last_transaction['last_transaction_date']
        ).dt.days
        
        # Merge with customer data
        churn_df = customers_df.merge(last_transaction, on='customer_id', how='left')
        
        # Calculate churn risk score (0-100)
        churn_df['churn_risk_score'] = np.clip(
            (churn_df['days_since_last_transaction'] / inactive_days) * 100,
            0, 100
        )
        
        # Assign risk category
        churn_df['churn_risk_category'] = pd.cut(
            churn_df['churn_risk_score'],
            bins=[0, 33, 66, 100],
            labels=['Low', 'Medium', 'High']
        )
        
        return churn_df[['customer_id', 'days_since_last_transaction', 
                        'churn_risk_score', 'churn_risk_category']]
    
    def customer_demographics_analysis(
        self,
        customers_df: pd.DataFrame
    ) -> Dict:
        """
        Analyze customer demographics
        
        Args:
            customers_df: Customer information
            
        Returns:
            Dictionary with demographic statistics
        """
        demographics = {
            'total_customers': len(customers_df),
            'by_account_type': customers_df['account_type'].value_counts().to_dict(),
            'by_country': customers_df['country'].value_counts().to_dict(),
            'avg_credit_score': customers_df['credit_score'].mean() if 'credit_score' in customers_df else None,
            'avg_monthly_income': customers_df['monthly_income'].mean() if 'monthly_income' in customers_df else None,
        }
        
        if 'risk_category' in customers_df:
            demographics['by_risk_category'] = customers_df['risk_category'].value_counts().to_dict()
        
        return demographics
