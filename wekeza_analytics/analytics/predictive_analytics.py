"""
Predictive Analytics Module

Provides predictive analytics including:
- Credit risk scoring
- Churn prediction
- Transaction forecasting
- Customer behavior prediction
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class PredictiveAnalytics:
    """Predictive analytics engine for Wekeza Bank"""
    
    def __init__(self):
        self.risk_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.forecast_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        
    def calculate_credit_risk_score(
        self,
        customers_df: pd.DataFrame,
        transactions_df: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Calculate credit risk scores for customers
        
        Args:
            customers_df: Customer data
            transactions_df: Optional transaction history
            
        Returns:
            DataFrame with risk scores
        """
        result_df = customers_df.copy()
        
        # Basic risk factors
        risk_scores = []
        
        for _, customer in customers_df.iterrows():
            score = 100  # Start with perfect score
            
            # Credit score factor (if available)
            if 'credit_score' in customer and pd.notna(customer['credit_score']):
                credit_score = customer['credit_score']
                if credit_score < 600:
                    score -= 30
                elif credit_score < 700:
                    score -= 15
                elif credit_score > 750:
                    score += 10
            
            # Income factor
            if 'monthly_income' in customer and pd.notna(customer['monthly_income']):
                income = customer['monthly_income']
                if income < 2000:
                    score -= 20
                elif income > 10000:
                    score += 15
            
            # Account age factor
            if 'registration_date' in customer:
                account_age_days = (pd.Timestamp.now() - customer['registration_date']).days
                if account_age_days < 180:  # Less than 6 months
                    score -= 10
                elif account_age_days > 730:  # More than 2 years
                    score += 10
            
            # Transaction history factor (if available)
            if transactions_df is not None:
                customer_txns = transactions_df[
                    transactions_df['customer_id'] == customer['customer_id']
                ]
                
                if len(customer_txns) > 0:
                    # Regular activity is good
                    if len(customer_txns) > 50:
                        score += 10
                    
                    # Check for fraud history
                    if 'is_fraudulent' in customer_txns:
                        fraud_count = customer_txns['is_fraudulent'].sum()
                        if fraud_count > 0:
                            score -= 30
            
            # Ensure score is between 0 and 100
            risk_scores.append(max(0, min(100, score)))
        
        result_df['credit_risk_score'] = risk_scores
        
        # Assign risk category
        result_df['risk_category'] = pd.cut(
            result_df['credit_risk_score'],
            bins=[0, 40, 70, 100],
            labels=['High Risk', 'Medium Risk', 'Low Risk']
        )
        
        return result_df[['customer_id', 'credit_risk_score', 'risk_category']]
    
    def predict_customer_churn(
        self,
        customers_df: pd.DataFrame,
        transactions_df: pd.DataFrame,
        train_model: bool = False
    ) -> pd.DataFrame:
        """
        Predict customer churn probability
        
        Args:
            customers_df: Customer data
            transactions_df: Transaction history
            train_model: Whether to train the model (requires labeled data)
            
        Returns:
            DataFrame with churn predictions
        """
        # Calculate customer features
        features_df = self._calculate_churn_features(customers_df, transactions_df)
        
        # Simple rule-based prediction (since we don't have labeled data)
        churn_probabilities = []
        
        for _, row in features_df.iterrows():
            prob = 0.0
            
            # Days since last transaction
            if row['days_since_last_transaction'] > 90:
                prob += 0.4
            elif row['days_since_last_transaction'] > 60:
                prob += 0.2
            
            # Transaction frequency
            if row['transaction_frequency'] < 1:  # Less than 1 per month
                prob += 0.3
            
            # Average transaction amount
            if row['avg_transaction_amount'] < 50:
                prob += 0.1
            
            # Account age
            if row['account_age_days'] < 90:
                prob += 0.2
            
            churn_probabilities.append(min(prob, 1.0))
        
        features_df['churn_probability'] = churn_probabilities
        features_df['churn_risk'] = pd.cut(
            features_df['churn_probability'],
            bins=[0, 0.3, 0.7, 1.0],
            labels=['Low', 'Medium', 'High']
        )
        
        return features_df[['customer_id', 'churn_probability', 'churn_risk']]
    
    def _calculate_churn_features(
        self,
        customers_df: pd.DataFrame,
        transactions_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Calculate features for churn prediction"""
        # Transaction metrics per customer
        txn_features = transactions_df.groupby('customer_id').agg({
            'transaction_id': 'count',
            'amount': ['mean', 'sum', 'std'],
            'transaction_date': ['min', 'max']
        }).reset_index()
        
        txn_features.columns = [
            'customer_id', 'transaction_count', 'avg_transaction_amount',
            'total_spending', 'std_transaction_amount', 'first_transaction', 'last_transaction'
        ]
        
        # Calculate additional features
        reference_date = pd.Timestamp.now()
        txn_features['days_since_last_transaction'] = (
            reference_date - txn_features['last_transaction']
        ).dt.days
        
        txn_features['transaction_frequency'] = txn_features['transaction_count'] / 30  # per month
        
        # Merge with customer data
        features_df = customers_df.merge(txn_features, on='customer_id', how='left')
        
        # Calculate account age
        features_df['account_age_days'] = (
            reference_date - features_df['registration_date']
        ).dt.days
        
        # Fill missing values
        features_df = features_df.fillna({
            'transaction_count': 0,
            'avg_transaction_amount': 0,
            'total_spending': 0,
            'days_since_last_transaction': 365,
            'transaction_frequency': 0,
        })
        
        return features_df
    
    def forecast_transaction_volume(
        self,
        transactions_df: pd.DataFrame,
        periods: int = 30
    ) -> pd.DataFrame:
        """
        Forecast transaction volume for future periods
        
        Args:
            transactions_df: Historical transaction data
            periods: Number of periods to forecast
            
        Returns:
            DataFrame with forecasted values
        """
        # Aggregate by date
        transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])
        
        daily_volume = transactions_df.groupby('transaction_date').agg({
            'transaction_id': 'count',
            'amount': 'sum'
        }).reset_index()
        
        daily_volume.columns = ['date', 'transaction_count', 'total_amount']
        
        # Simple moving average forecast
        window = min(7, len(daily_volume))
        
        forecast_dates = pd.date_range(
            start=daily_volume['date'].max() + pd.Timedelta(days=1),
            periods=periods,
            freq='D'
        )
        
        # Calculate moving average for forecast
        avg_count = daily_volume['transaction_count'].tail(window).mean()
        avg_amount = daily_volume['total_amount'].tail(window).mean()
        
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'forecasted_transaction_count': avg_count,
            'forecasted_total_amount': avg_amount
        })
        
        return forecast_df
    
    def predict_next_transaction_amount(
        self,
        customer_id: str,
        transactions_df: pd.DataFrame
    ) -> Dict:
        """
        Predict the next transaction amount for a customer
        
        Args:
            customer_id: Customer identifier
            transactions_df: Transaction history
            
        Returns:
            Dictionary with prediction
        """
        customer_txns = transactions_df[
            transactions_df['customer_id'] == customer_id
        ].copy()
        
        if len(customer_txns) == 0:
            return {'error': 'No transaction history found'}
        
        # Statistical prediction based on historical patterns
        prediction = {
            'customer_id': customer_id,
            'predicted_amount': float(customer_txns['amount'].mean()),
            'confidence_interval_lower': float(
                customer_txns['amount'].mean() - 1.96 * customer_txns['amount'].std()
            ),
            'confidence_interval_upper': float(
                customer_txns['amount'].mean() + 1.96 * customer_txns['amount'].std()
            ),
            'prediction_method': 'historical_average',
            'sample_size': len(customer_txns)
        }
        
        return prediction
    
    def identify_high_value_customers(
        self,
        customers_df: pd.DataFrame,
        transactions_df: pd.DataFrame,
        top_n: int = 100
    ) -> pd.DataFrame:
        """
        Identify high-value customers based on predicted lifetime value
        
        Args:
            customers_df: Customer data
            transactions_df: Transaction history
            top_n: Number of top customers to return
            
        Returns:
            DataFrame with high-value customers
        """
        # Calculate customer value metrics
        customer_value = transactions_df.groupby('customer_id').agg({
            'amount': ['sum', 'mean', 'count'],
            'transaction_date': ['min', 'max']
        }).reset_index()
        
        customer_value.columns = [
            'customer_id', 'total_value', 'avg_transaction',
            'transaction_count', 'first_date', 'last_date'
        ]
        
        # Calculate customer lifetime (in months)
        customer_value['lifetime_months'] = (
            customer_value['last_date'] - customer_value['first_date']
        ).dt.days / 30
        
        customer_value['lifetime_months'] = customer_value['lifetime_months'].clip(lower=1)
        
        # Calculate predicted CLV (simple version)
        customer_value['predicted_clv'] = (
            customer_value['avg_transaction'] *
            customer_value['transaction_count'] /
            customer_value['lifetime_months'] *
            12  # Annualized
        )
        
        # Get top N customers
        top_customers = customer_value.nlargest(top_n, 'predicted_clv')
        
        # Merge with customer info
        result = top_customers.merge(customers_df, on='customer_id', how='left')
        
        return result[['customer_id', 'predicted_clv', 'total_value', 
                      'transaction_count', 'avg_transaction']]
