import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)

class RiskScorer:
    def __init__(self):
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def calculate_transaction_risk(self, transaction_data):
        """
        Calculate risk score for a single transaction
        Returns: (risk_score, risk_level, reasons)
        """
        risk_factors = []
        risk_score = 0.0
        
        # Amount-based risk
        amount = float(transaction_data.get('amount', 0))
        if amount > 10000000:  # 10M KES
            risk_score += 0.4
            risk_factors.append(f"High amount: {amount:,.0f} KES")
        elif amount > 1000000:  # 1M KES
            risk_score += 0.2
            risk_factors.append(f"Medium amount: {amount:,.0f} KES")
        
        # Merchant risk
        merchant = str(transaction_data.get('merchant_name', '')).lower()
        high_risk_merchants = ['unknown', 'shell', 'suspicious', 'cash']
        if any(keyword in merchant for keyword in high_risk_merchants):
            risk_score += 0.3
            risk_factors.append(f"High-risk merchant: {merchant}")
        
        # Transaction type risk
        tx_type = str(transaction_data.get('transaction_type', '')).lower()
        if tx_type in ['transfer', 'payment'] and amount > 5000000:
            risk_score += 0.2
            risk_factors.append("Large transfer/payment")
        
        # Location risk
        location = str(transaction_data.get('location', '')).lower()
        if location in ['unknown', 'offshore', 'foreign']:
            risk_score += 0.25
            risk_factors.append(f"High-risk location: {location}")
        
        # Channel risk
        channel = str(transaction_data.get('channel', '')).lower()
        if channel == 'online' and amount > 2000000:
            risk_score += 0.15
            risk_factors.append("Large online transaction")
        
        # Time-based risk (transactions outside business hours)
        timestamp = transaction_data.get('timestamp')
        if timestamp:
            hour = pd.to_datetime(timestamp).hour
            if hour < 6 or hour > 22:  # Outside 6 AM - 10 PM
                risk_score += 0.1
                risk_factors.append("Off-hours transaction")
        
        # Determine risk level
        if risk_score >= 0.8:
            risk_level = 'HIGH'
        elif risk_score >= 0.5:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        return risk_score, risk_level, '; '.join(risk_factors)
    
    def train_anomaly_detector(self, historical_data):
        """Train the isolation forest on historical transaction data"""
        try:
            if len(historical_data) < 10:
                logger.warning("Insufficient data for anomaly detection training")
                return False
            
            # Prepare features for anomaly detection
            features = self._prepare_features(historical_data)
            
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            
            # Train isolation forest
            self.isolation_forest.fit(features_scaled)
            self.is_trained = True
            
            logger.info(f"Trained anomaly detector on {len(historical_data)} transactions")
            return True
        except Exception as e:
            logger.error(f"Error training anomaly detector: {e}")
            return False
    
    def detect_anomaly(self, transaction_data):
        """Detect if a transaction is anomalous using the trained model"""
        if not self.is_trained:
            return 0.0, "Model not trained"
        
        try:
            # Prepare features
            features = self._prepare_features(pd.DataFrame([transaction_data]))
            features_scaled = self.scaler.transform(features)
            
            # Get anomaly score
            anomaly_score = self.isolation_forest.decision_function(features_scaled)[0]
            is_anomaly = self.isolation_forest.predict(features_scaled)[0] == -1
            
            # Convert to risk score (anomaly_score is negative for anomalies)
            risk_contribution = max(0, -anomaly_score * 0.3)  # Scale to 0-0.3 range
            
            reason = "Anomalous pattern detected" if is_anomaly else "Normal pattern"
            return risk_contribution, reason
        except Exception as e:
            logger.error(f"Error in anomaly detection: {e}")
            return 0.0, "Anomaly detection failed"
    
    def _prepare_features(self, data):
        """Prepare numerical features for machine learning"""
        features = pd.DataFrame()
        
        # Amount (log-transformed to handle large values)
        features['log_amount'] = np.log1p(data['amount'].astype(float))
        
        # Hour of day
        if 'timestamp' in data.columns:
            features['hour'] = pd.to_datetime(data['timestamp']).dt.hour
        else:
            features['hour'] = 12  # Default to noon
        
        # Day of week
        if 'timestamp' in data.columns:
            features['day_of_week'] = pd.to_datetime(data['timestamp']).dt.dayofweek
        else:
            features['day_of_week'] = 1  # Default to Tuesday
        
        # Transaction type encoding
        tx_type_map = {'transfer': 1, 'payment': 2, 'withdrawal': 3, 'deposit': 4}
        features['tx_type_encoded'] = data.get('transaction_type', 'transfer').map(
            lambda x: tx_type_map.get(str(x).lower(), 0)
        )
        
        # Channel encoding
        channel_map = {'mobile': 1, 'online': 2, 'atm': 3, 'branch': 4}
        features['channel_encoded'] = data.get('channel', 'mobile').map(
            lambda x: channel_map.get(str(x).lower(), 0)
        )
        
        return features.fillna(0)

class CreditRiskModel:
    """Specialized model for credit risk assessment"""
    
    def calculate_credit_risk(self, customer_data, transaction_history):
        """Calculate credit risk for a customer based on transaction history"""
        risk_score = 0.0
        factors = []
        
        if len(transaction_history) == 0:
            return 0.5, "No transaction history available"
        
        # Calculate transaction velocity
        daily_volume = transaction_history.groupby(
            transaction_history['timestamp'].dt.date
        )['amount'].sum()
        
        avg_daily_volume = daily_volume.mean()
        max_daily_volume = daily_volume.max()
        
        if max_daily_volume > avg_daily_volume * 5:
            risk_score += 0.3
            factors.append("High transaction velocity detected")
        
        # Large transaction frequency
        large_txns = transaction_history[transaction_history['amount'] > 1000000]
        if len(large_txns) > len(transaction_history) * 0.1:
            risk_score += 0.2
            factors.append("Frequent large transactions")
        
        return min(risk_score, 1.0), '; '.join(factors)

class LiquidityRiskModel:
    """Model for liquidity risk assessment"""
    
    def calculate_liquidity_metrics(self, portfolio_data):
        """Calculate liquidity coverage ratio and other metrics"""
        # Simplified LCR calculation
        # In reality, this would use actual HQLA and net cash outflows
        
        total_assets = portfolio_data.get('total_transactions', 0) * 1000000  # Simplified
        liquid_assets = total_assets * 0.3  # Assume 30% are liquid
        
        lcr = liquid_assets / (total_assets * 0.1)  # Simplified outflow calculation
        
        status = 'OK' if lcr >= 1.0 else 'WARNING' if lcr >= 0.8 else 'CRITICAL'
        
        return {
            'liquidity_coverage_ratio': lcr,
            'status': status,
            'liquid_assets': liquid_assets
        }