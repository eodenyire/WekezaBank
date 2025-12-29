"""
Transaction Analytics Module

Provides transaction analytics including:
- Transaction pattern analysis
- Anomaly detection
- Fraud detection
- Spending behavior analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from scipy import stats


class TransactionAnalytics:
    """Transaction analytics engine for Wekeza Bank"""
    
    def __init__(self):
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        
    def transaction_summary(
        self,
        transactions_df: pd.DataFrame,
        period: str = 'daily'
    ) -> pd.DataFrame:
        """
        Generate transaction summary statistics
        
        Args:
            transactions_df: Transaction data
            period: Aggregation period ('daily', 'weekly', 'monthly')
            
        Returns:
            DataFrame with transaction summaries
        """
        # Convert to datetime if not already
        transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])
        
        # Determine grouping frequency
        freq_map = {
            'daily': 'D',
            'weekly': 'W',
            'monthly': 'M'
        }
        freq = freq_map.get(period, 'D')
        
        # Group and aggregate
        summary = transactions_df.groupby(pd.Grouper(key='transaction_date', freq=freq)).agg({
            'transaction_id': 'count',
            'amount': ['sum', 'mean', 'median', 'std'],
        }).reset_index()
        
        summary.columns = ['date', 'transaction_count', 'total_amount', 
                          'avg_amount', 'median_amount', 'std_amount']
        
        return summary
    
    def detect_anomalies(
        self,
        transactions_df: pd.DataFrame,
        features: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Detect anomalous transactions using Isolation Forest
        
        Args:
            transactions_df: Transaction data
            features: Features to use for anomaly detection
            
        Returns:
            DataFrame with anomaly flags
        """
        if features is None:
            features = ['amount']
        
        # Prepare features
        X = transactions_df[features].fillna(0)
        
        # Detect anomalies
        predictions = self.anomaly_detector.fit_predict(X)
        transactions_df['is_anomaly'] = predictions == -1
        
        # Calculate anomaly score
        scores = self.anomaly_detector.score_samples(X)
        transactions_df['anomaly_score'] = -scores  # Convert to positive scores
        
        return transactions_df
    
    def fraud_detection_analysis(
        self,
        transactions_df: pd.DataFrame
    ) -> Dict:
        """
        Analyze fraud patterns in transactions
        
        Args:
            transactions_df: Transaction data with fraud flags
            
        Returns:
            Dictionary with fraud statistics
        """
        if 'is_fraudulent' not in transactions_df:
            return {'error': 'No fraud flags found in data'}
        
        total_transactions = len(transactions_df)
        fraudulent_transactions = transactions_df['is_fraudulent'].sum()
        
        fraud_stats = {
            'total_transactions': total_transactions,
            'fraudulent_count': int(fraudulent_transactions),
            'fraud_rate': (fraudulent_transactions / total_transactions * 100) if total_transactions > 0 else 0,
            'total_fraud_amount': float(transactions_df[transactions_df['is_fraudulent']]['amount'].sum()),
        }
        
        # Analyze fraud by category
        if 'category' in transactions_df:
            fraud_by_category = transactions_df[transactions_df['is_fraudulent']].groupby('category').size()
            fraud_stats['fraud_by_category'] = fraud_by_category.to_dict()
        
        # Analyze fraud by transaction type
        if 'transaction_type' in transactions_df:
            fraud_by_type = transactions_df[transactions_df['is_fraudulent']].groupby('transaction_type').size()
            fraud_stats['fraud_by_type'] = fraud_by_type.to_dict()
        
        return fraud_stats
    
    def spending_pattern_analysis(
        self,
        transactions_df: pd.DataFrame,
        customer_id: Optional[str] = None
    ) -> Dict:
        """
        Analyze spending patterns
        
        Args:
            transactions_df: Transaction data
            customer_id: Optional customer ID to analyze specific customer
            
        Returns:
            Dictionary with spending pattern statistics
        """
        # Filter for specific customer if provided
        if customer_id:
            df = transactions_df[transactions_df['customer_id'] == customer_id].copy()
        else:
            df = transactions_df.copy()
        
        if len(df) == 0:
            return {'error': 'No transactions found'}
        
        patterns = {
            'total_spending': float(df['amount'].sum()),
            'avg_transaction_size': float(df['amount'].mean()),
            'median_transaction_size': float(df['amount'].median()),
            'transaction_count': len(df),
        }
        
        # Spending by category
        if 'category' in df:
            patterns['spending_by_category'] = df.groupby('category')['amount'].sum().to_dict()
        
        # Spending by type
        if 'transaction_type' in df:
            patterns['spending_by_type'] = df.groupby('transaction_type')['amount'].sum().to_dict()
        
        # Time-based patterns
        if 'transaction_date' in df:
            df['transaction_date'] = pd.to_datetime(df['transaction_date'])
            df['hour'] = df['transaction_date'].dt.hour
            df['day_of_week'] = df['transaction_date'].dt.dayofweek
            df['month'] = df['transaction_date'].dt.month
            
            patterns['spending_by_hour'] = df.groupby('hour')['amount'].sum().to_dict()
            patterns['spending_by_day_of_week'] = df.groupby('day_of_week')['amount'].sum().to_dict()
            patterns['spending_by_month'] = df.groupby('month')['amount'].sum().to_dict()
        
        return patterns
    
    def transaction_velocity_analysis(
        self,
        transactions_df: pd.DataFrame,
        time_window_hours: int = 24
    ) -> pd.DataFrame:
        """
        Analyze transaction velocity (transactions per time window)
        
        Args:
            transactions_df: Transaction data
            time_window_hours: Time window for velocity calculation
            
        Returns:
            DataFrame with velocity metrics per customer
        """
        transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])
        
        # Sort by customer and date
        df = transactions_df.sort_values(['customer_id', 'transaction_date']).copy()
        
        # Calculate time difference between consecutive transactions
        df['time_diff'] = df.groupby('customer_id')['transaction_date'].diff()
        
        # Count transactions per customer in the time window
        velocity = df.groupby('customer_id').agg({
            'transaction_id': 'count',
            'time_diff': 'mean'
        }).reset_index()
        
        velocity.columns = ['customer_id', 'transaction_count', 'avg_time_between_transactions']
        
        # Calculate velocity score
        velocity['velocity_score'] = velocity['transaction_count'] / (
            velocity['avg_time_between_transactions'].dt.total_seconds() / 3600
        )
        
        return velocity
    
    def merchant_analysis(
        self,
        transactions_df: pd.DataFrame
    ) -> Dict:
        """
        Analyze merchant transaction patterns
        
        Args:
            transactions_df: Transaction data with merchant information
            
        Returns:
            Dictionary with merchant statistics
        """
        if 'merchant' not in transactions_df:
            return {'error': 'No merchant data found'}
        
        # Remove null merchants
        df = transactions_df[transactions_df['merchant'].notna()].copy()
        
        merchant_stats = {
            'unique_merchants': df['merchant'].nunique(),
            'top_merchants_by_transaction_count': df['merchant'].value_counts().head(10).to_dict(),
            'top_merchants_by_volume': df.groupby('merchant')['amount'].sum().nlargest(10).to_dict(),
        }
        
        return merchant_stats
    
    def calculate_transaction_metrics(
        self,
        transactions_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate comprehensive transaction metrics
        
        Args:
            transactions_df: Transaction data
            
        Returns:
            Dictionary with key transaction metrics
        """
        metrics = {
            'total_transactions': len(transactions_df),
            'total_volume': float(transactions_df['amount'].sum()),
            'avg_transaction_size': float(transactions_df['amount'].mean()),
            'median_transaction_size': float(transactions_df['amount'].median()),
            'std_transaction_size': float(transactions_df['amount'].std()),
            'max_transaction_size': float(transactions_df['amount'].max()),
            'min_transaction_size': float(transactions_df['amount'].min()),
        }
        
        # Status distribution
        if 'status' in transactions_df:
            metrics['by_status'] = transactions_df['status'].value_counts().to_dict()
        
        # Type distribution
        if 'transaction_type' in transactions_df:
            metrics['by_type'] = transactions_df['transaction_type'].value_counts().to_dict()
        
        return metrics
