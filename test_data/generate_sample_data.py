#!/usr/bin/env python3
"""
Generate sample transaction data for testing the risk management system
"""

import random
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'risk_engine'))
from database import DatabaseManager

class SampleDataGenerator:
    def __init__(self):
        self.db = DatabaseManager()
        
        # Sample data pools
        self.customers = [f"CUST_{i:05d}" for i in range(1000, 2000)]
        self.accounts = [f"{random.randint(1000000000, 9999999999)}" for _ in range(len(self.customers))]
        
        self.merchants = [
            "Safaricom Ltd", "Equity Bank", "KCB Bank", "Cooperative Bank",
            "Nakumatt Supermarket", "Tuskys Supermarket", "Java House",
            "Shell Kenya", "Total Kenya", "Kenol Kobil",
            "Nairobi Hospital", "Aga Khan Hospital", "MP Shah Hospital",
            "University of Nairobi", "Strathmore University", "USIU",
            "Kenya Airways", "Jambojet", "Fly540",
            "Uber Kenya", "Bolt Kenya", "Little Cab",
            "Jumia Kenya", "Kilimall", "Masoko",
            # High-risk merchants for testing
            "Unknown Shell Co", "Suspicious Entity", "Offshore Holdings",
            "Cash Advance Ltd", "Quick Money Transfer", "Anonymous Trader"
        ]
        
        self.locations = [
            "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret",
            "Thika", "Kitale", "Malindi", "Nyeri", "Meru",
            "Kakamega", "Kericho", "Machakos", "Garissa", "Isiolo",
            # High-risk locations
            "Unknown", "Offshore", "Foreign"
        ]
        
        self.transaction_types = ["TRANSFER", "PAYMENT", "WITHDRAWAL", "DEPOSIT"]
        self.channels = ["MOBILE", "ONLINE", "ATM", "BRANCH"]
        self.merchant_categories = [
            "RETAIL", "FUEL", "HEALTHCARE", "EDUCATION", "TRANSPORT",
            "ECOMMERCE", "RESTAURANT", "BANKING", "TELECOM", "GOVERNMENT",
            "UNKNOWN", "HIGH_RISK", "SOFTWARE"
        ]
    
    def generate_normal_transaction(self):
        """Generate a normal, low-risk transaction"""
        customer_id = random.choice(self.customers)
        account_number = random.choice(self.accounts)
        
        # Normal transaction amounts (mostly under 1M KES)
        amount = random.choice([
            random.uniform(100, 50000),      # 70% - small transactions
            random.uniform(50000, 500000),   # 25% - medium transactions  
            random.uniform(500000, 1000000)  # 5% - large but normal
        ])
        
        merchant = random.choice(self.merchants[:20])  # Avoid high-risk merchants
        location = random.choice(self.locations[:15])  # Avoid high-risk locations
        
        return {
            'transaction_id': f"TXN_{random.randint(100000, 999999)}",
            'customer_id': customer_id,
            'account_number': account_number,
            'amount': round(amount, 2),
            'currency': 'KES',
            'transaction_type': random.choice(self.transaction_types),
            'merchant_name': merchant,
            'merchant_category': random.choice(self.merchant_categories[:10]),
            'location': location,
            'channel': random.choice(self.channels),
            'timestamp': datetime.now() - timedelta(
                hours=random.randint(0, 168),  # Last 7 days
                minutes=random.randint(0, 59)
            ),
            'status': 'PENDING'
        }
    
    def generate_medium_risk_transaction(self):
        """Generate a medium-risk transaction"""
        transaction = self.generate_normal_transaction()
        
        # Make it medium risk by adjusting parameters
        risk_factors = random.choice([
            'high_amount',
            'suspicious_merchant',
            'off_hours',
            'high_velocity'
        ])
        
        if risk_factors == 'high_amount':
            transaction['amount'] = random.uniform(1000000, 5000000)  # 1-5M KES
        elif risk_factors == 'suspicious_merchant':
            transaction['merchant_name'] = random.choice(self.merchants[-6:])  # High-risk merchants
            transaction['merchant_category'] = 'HIGH_RISK'
        elif risk_factors == 'off_hours':
            # Set to off-hours (late night/early morning)
            transaction['timestamp'] = transaction['timestamp'].replace(
                hour=random.choice([1, 2, 3, 4, 5, 23])
            )
        elif risk_factors == 'high_velocity':
            transaction['amount'] = random.uniform(800000, 1500000)
            transaction['channel'] = 'ONLINE'
        
        return transaction
    
    def generate_high_risk_transaction(self):
        """Generate a high-risk transaction"""
        transaction = self.generate_normal_transaction()
        
        # Make it high risk with multiple factors
        transaction['amount'] = random.uniform(5000000, 50000000)  # 5-50M KES
        transaction['merchant_name'] = random.choice(self.merchants[-6:])  # High-risk merchants
        transaction['merchant_category'] = 'HIGH_RISK'
        transaction['location'] = random.choice(self.locations[-3:])  # High-risk locations
        transaction['channel'] = 'ONLINE'
        
        # Often off-hours
        if random.random() < 0.7:
            transaction['timestamp'] = transaction['timestamp'].replace(
                hour=random.choice([1, 2, 3, 4, 23])
            )
        
        return transaction
    
    def generate_batch(self, count=100):
        """Generate a batch of mixed transactions"""
        transactions = []
        
        for _ in range(count):
            risk_type = random.choices(
                ['normal', 'medium', 'high'],
                weights=[0.85, 0.12, 0.03],  # 85% normal, 12% medium, 3% high
                k=1
            )[0]
            
            if risk_type == 'normal':
                transaction = self.generate_normal_transaction()
            elif risk_type == 'medium':
                transaction = self.generate_medium_risk_transaction()
            else:
                transaction = self.generate_high_risk_transaction()
            
            transactions.append(transaction)
        
        return transactions
    
    def insert_transactions(self, transactions):
        """Insert transactions into the database"""
        conn = self.db.get_connection()
        try:
            cur = conn.cursor()
            
            for txn in transactions:
                cur.execute("""
                    INSERT OR IGNORE INTO transaction_history 
                    (transaction_id, customer_id, account_number, amount, currency,
                     transaction_type, merchant_name, merchant_category, location, 
                     channel, timestamp, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    txn['transaction_id'], txn['customer_id'], txn['account_number'],
                    txn['amount'], txn['currency'], txn['transaction_type'],
                    txn['merchant_name'], txn['merchant_category'], txn['location'],
                    txn['channel'], txn['timestamp'], txn['status']
                ))
            
            conn.commit()
            print(f"✅ Inserted {len(transactions)} transactions")
            
        except Exception as e:
            print(f"❌ Error inserting transactions: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def generate_and_insert(self, count=100):
        """Generate and insert sample transactions"""
        print(f"🔄 Generating {count} sample transactions...")
        transactions = self.generate_batch(count)
        self.insert_transactions(transactions)
        
        # Print summary
        risk_summary = {}
        for txn in transactions:
            amount = txn['amount']
            if amount >= 5000000:
                risk_level = 'HIGH'
            elif amount >= 1000000 or txn['merchant_category'] == 'HIGH_RISK':
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            risk_summary[risk_level] = risk_summary.get(risk_level, 0) + 1
        
        print(f"📊 Generated transactions by risk level:")
        for level, count in risk_summary.items():
            print(f"   {level}: {count}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate sample transaction data')
    parser.add_argument('--count', type=int, default=100, help='Number of transactions to generate')
    parser.add_argument('--continuous', action='store_true', help='Generate transactions continuously')
    parser.add_argument('--interval', type=int, default=30, help='Interval in seconds for continuous mode')
    
    args = parser.parse_args()
    
    generator = SampleDataGenerator()
    
    if args.continuous:
        print(f"🔄 Starting continuous generation (every {args.interval} seconds)")
        print("Press Ctrl+C to stop")
        
        import time
        try:
            while True:
                generator.generate_and_insert(10)  # Generate 10 at a time
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n⏹️ Stopped by user")
    else:
        generator.generate_and_insert(args.count)

if __name__ == "__main__":
    main()