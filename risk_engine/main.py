#!/usr/bin/env python3
"""
Main Risk Engine for Equity Bank Risk Management System

This script continuously monitors transactions from the data warehouse,
applies risk scoring models, and routes high-risk transactions to analysts
via Ballerine case management system.
"""

import logging
import time
import schedule
from datetime import datetime
import pandas as pd

from config import Config
from database import DatabaseManager
from risk_models import RiskScorer, CreditRiskModel, LiquidityRiskModel
from integrations import BallerineIntegration, CISOAssistantIntegration, TazamaIntegration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('risk_engine.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class RiskEngine:
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager()
        self.risk_scorer = RiskScorer()
        self.credit_model = CreditRiskModel()
        self.liquidity_model = LiquidityRiskModel()
        
        # Integrations
        self.ballerine = BallerineIntegration()
        self.ciso = CISOAssistantIntegration()
        self.tazama = TazamaIntegration()
        
        # Initialize anomaly detection model
        self._train_models()
    
    def _train_models(self):
        """Train ML models on historical data"""
        try:
            # Get historical data for training
            historical_query = """
            SELECT * FROM transaction_history 
            WHERE date(timestamp) >= date('now', '-30 days')
            ORDER BY timestamp DESC
            LIMIT 1000
            """
            historical_data = pd.read_sql(historical_query, self.db.engine)
            
            if len(historical_data) > 10:
                self.risk_scorer.train_anomaly_detector(historical_data)
                logger.info("Successfully trained risk models")
            else:
                logger.warning("Insufficient historical data for model training")
        except Exception as e:
            logger.error(f"Error training models: {e}")
    
    def process_transactions(self):
        """Main processing loop - fetch and analyze new transactions"""
        logger.info("Starting transaction processing cycle...")
        
        try:
            # Fetch pending transactions
            transactions = self.db.fetch_pending_transactions(limit=self.config.BATCH_SIZE)
            
            if transactions.empty:
                logger.info("No pending transactions to process")
                return
            
            logger.info(f"Processing {len(transactions)} transactions")
            
            # Process each transaction
            for _, transaction in transactions.iterrows():
                self._process_single_transaction(transaction)
            
            # Calculate and log portfolio metrics
            self._update_portfolio_metrics()
            
        except Exception as e:
            logger.error(f"Error in transaction processing: {e}")
    
    def _process_single_transaction(self, transaction):
        """Process a single transaction through the risk pipeline"""
        try:
            transaction_id = transaction['transaction_id']
            logger.info(f"Processing transaction: {transaction_id}")
            
            # Step 1: Calculate base risk score
            risk_score, risk_level, risk_reasons = self.risk_scorer.calculate_transaction_risk(transaction)
            
            # Step 2: Add anomaly detection score
            anomaly_score, anomaly_reason = self.risk_scorer.detect_anomaly(transaction)
            risk_score = min(risk_score + anomaly_score, 1.0)
            
            if anomaly_score > 0:
                risk_reasons += f"; {anomaly_reason}"
            
            # Step 3: Submit to Tazama for real-time fraud detection
            tazama_result = self.tazama.submit_transaction(transaction)
            if tazama_result.get('success') and tazama_result.get('fraud_score', 0) > 0.3:
                risk_score = min(risk_score + tazama_result['fraud_score'] * 0.2, 1.0)
                risk_reasons += f"; Tazama fraud indicators: {', '.join(tazama_result.get('typologies', []))}"
            
            # Recalculate risk level after all adjustments
            if risk_score >= self.config.HIGH_RISK_THRESHOLD:
                risk_level = 'HIGH'
            elif risk_score >= self.config.MEDIUM_RISK_THRESHOLD:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            logger.info(f"Transaction {transaction_id}: Risk Level = {risk_level}, Score = {risk_score:.3f}")
            
            # Step 4: Route based on risk level
            if risk_level in ['HIGH', 'MEDIUM']:
                # Create analyst case
                case_id = self.db.create_analyst_case(
                    transaction, risk_score, risk_level, risk_reasons
                )
                
                if case_id:
                    # Create case in Ballerine
                    ballerine_result = self.ballerine.create_case(
                        transaction, risk_score, risk_reasons
                    )
                    
                    if risk_level == 'HIGH':
                        # Log high-risk event to CISO Assistant
                        self.ciso.log_risk_event(
                            risk_type="OPERATIONAL",
                            title=f"High Risk Transaction Detected: {transaction_id}",
                            description=f"Transaction of {transaction['amount']:,.0f} KES flagged as high risk. Reasons: {risk_reasons}",
                            severity="high"
                        )
                        
                        # Block transaction for manual review
                        self.db.update_transaction_status(transaction_id, 'BLOCKED')
                    else:
                        # Medium risk - flag for review but don't block
                        self.db.update_transaction_status(transaction_id, 'FLAGGED')
            else:
                # Low risk - auto-approve
                self.db.update_transaction_status(transaction_id, 'APPROVED')
                logger.info(f"Transaction {transaction_id} auto-approved (low risk)")
            
        except Exception as e:
            logger.error(f"Error processing transaction {transaction.get('transaction_id', 'unknown')}: {e}")
    
    def _update_portfolio_metrics(self):
        """Calculate and update portfolio-level risk metrics"""
        try:
            # Get portfolio statistics
            portfolio_data = self.db.get_portfolio_metrics()
            
            # Calculate liquidity metrics
            liquidity_metrics = self.liquidity_model.calculate_liquidity_metrics(portfolio_data)
            
            # Log liquidity coverage ratio
            self.db.log_risk_metric(
                metric_type="LIQUIDITY",
                metric_name="Liquidity Coverage Ratio",
                value=liquidity_metrics['liquidity_coverage_ratio'],
                threshold=1.0,
                status=liquidity_metrics['status']
            )
            
            # Check for portfolio-level alerts
            if liquidity_metrics['status'] in ['WARNING', 'CRITICAL']:
                self.ciso.log_risk_event(
                    risk_type="LIQUIDITY",
                    title="Liquidity Coverage Ratio Alert",
                    description=f"LCR has dropped to {liquidity_metrics['liquidity_coverage_ratio']:.3f}",
                    severity="high" if liquidity_metrics['status'] == 'CRITICAL' else "medium"
                )
            
            # Calculate transaction volume metrics
            high_value_ratio = portfolio_data.get('high_value_count', 0) / max(portfolio_data.get('total_transactions', 1), 1)
            
            if high_value_ratio > 0.1:  # More than 10% high-value transactions
                self.ciso.log_risk_event(
                    risk_type="CREDIT",
                    title="High Value Transaction Volume Alert",
                    description=f"High value transactions represent {high_value_ratio:.1%} of daily volume",
                    severity="medium"
                )
            
            logger.info("Portfolio metrics updated successfully")
            
        except Exception as e:
            logger.error(f"Error updating portfolio metrics: {e}")
    
    def run_continuous(self):
        """Run the risk engine continuously"""
        logger.info("Starting Risk Engine in continuous mode...")
        
        # Schedule regular processing
        schedule.every(self.config.POLLING_INTERVAL_SECONDS).seconds.do(self.process_transactions)
        
        # Schedule daily model retraining
        schedule.every().day.at("02:00").do(self._train_models)
        
        # Schedule hourly portfolio metrics update
        schedule.every().hour.do(self._update_portfolio_metrics)
        
        logger.info(f"Risk Engine scheduled to run every {self.config.POLLING_INTERVAL_SECONDS} seconds")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Risk Engine stopped by user")
        except Exception as e:
            logger.error(f"Risk Engine crashed: {e}")
    
    def run_once(self):
        """Run a single processing cycle (useful for testing)"""
        logger.info("Running single processing cycle...")
        self.process_transactions()

def main():
    """Main entry point"""
    import sys
    
    engine = RiskEngine()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        engine.run_once()
    else:
        engine.run_continuous()

if __name__ == "__main__":
    main()