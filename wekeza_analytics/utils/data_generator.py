"""
Sample data generator for testing and demonstrations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict
import random


class DataGenerator:
    """Generate sample banking data for analytics testing"""
    
    def __init__(self, seed: int = 42):
        """
        Initialize data generator
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        np.random.seed(seed)
        random.seed(seed)
        
    def generate_customers(self, n_customers: int = 1000) -> pd.DataFrame:
        """
        Generate sample customer data
        
        Args:
            n_customers: Number of customers to generate
            
        Returns:
            DataFrame with customer data
        """
        account_types = ['savings', 'checking', 'business', 'investment']
        countries = ['USA', 'UK', 'Canada', 'Australia', 'Germany', 'France']
        risk_categories = ['low', 'medium', 'high']
        
        customers = []
        
        for i in range(n_customers):
            registration_date = datetime.now() - timedelta(
                days=random.randint(0, 1825)  # 0-5 years ago
            )
            
            customer = {
                'customer_id': f'CUST{i+1:05d}',
                'name': f'Customer {i+1}',
                'email': f'customer{i+1}@example.com',
                'phone': f'+1{random.randint(1000000000, 9999999999)}',
                'account_type': random.choice(account_types),
                'registration_date': registration_date,
                'credit_score': random.randint(300, 850),
                'monthly_income': random.choice([
                    random.randint(2000, 5000),    # Low income
                    random.randint(5000, 10000),   # Medium income
                    random.randint(10000, 25000),  # High income
                ]),
                'country': random.choice(countries),
                'risk_category': random.choice(risk_categories),
            }
            
            customers.append(customer)
        
        return pd.DataFrame(customers)
    
    def generate_transactions(
        self,
        customers_df: pd.DataFrame,
        avg_transactions_per_customer: int = 50
    ) -> pd.DataFrame:
        """
        Generate sample transaction data
        
        Args:
            customers_df: Customer data
            avg_transactions_per_customer: Average number of transactions per customer
            
        Returns:
            DataFrame with transaction data
        """
        transaction_types = ['debit', 'credit', 'transfer']
        categories = ['shopping', 'bills', 'salary', 'entertainment', 'groceries', 
                     'transport', 'healthcare', 'education', 'dining']
        statuses = ['completed', 'pending', 'failed']
        merchants = [
            'Amazon', 'Walmart', 'Target', 'Starbucks', 'Shell', 
            'Apple', 'Netflix', 'Uber', 'Airbnb', 'PayPal'
        ]
        locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
        
        transactions = []
        transaction_id = 1
        
        for _, customer in customers_df.iterrows():
            # Vary number of transactions per customer
            n_transactions = max(1, int(np.random.normal(
                avg_transactions_per_customer, avg_transactions_per_customer * 0.3
            )))
            
            customer_start_date = customer['registration_date']
            
            for _ in range(n_transactions):
                # Random date between registration and now
                days_since_registration = (datetime.now() - customer_start_date).days
                if days_since_registration > 0:
                    transaction_date = customer_start_date + timedelta(
                        days=random.randint(0, days_since_registration)
                    )
                else:
                    transaction_date = customer_start_date
                
                # Generate transaction amount based on type
                txn_type = random.choice(transaction_types)
                if txn_type == 'credit':
                    # Credits tend to be larger (salaries, refunds)
                    amount = random.uniform(500, 5000)
                else:
                    # Debits vary widely
                    amount = random.choice([
                        random.uniform(5, 50),      # Small purchases
                        random.uniform(50, 200),    # Medium purchases
                        random.uniform(200, 1000),  # Large purchases
                    ])
                
                transaction = {
                    'transaction_id': f'TXN{transaction_id:08d}',
                    'customer_id': customer['customer_id'],
                    'transaction_date': transaction_date,
                    'amount': round(amount, 2),
                    'transaction_type': txn_type,
                    'category': random.choice(categories),
                    'merchant': random.choice(merchants) if txn_type != 'credit' else None,
                    'location': random.choice(locations),
                    'status': random.choices(statuses, weights=[0.9, 0.05, 0.05])[0],
                    'is_fraudulent': random.random() < 0.01,  # 1% fraud rate
                }
                
                transactions.append(transaction)
                transaction_id += 1
        
        return pd.DataFrame(transactions)
    
    def generate_accounts(
        self,
        customers_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Generate sample account data
        
        Args:
            customers_df: Customer data
            
        Returns:
            DataFrame with account data
        """
        account_types = ['savings', 'checking', 'business', 'investment']
        currencies = ['USD', 'EUR', 'GBP', 'CAD']
        statuses = ['active', 'dormant', 'closed']
        
        accounts = []
        
        for i, customer in customers_df.iterrows():
            # Each customer can have 1-3 accounts
            n_accounts = random.randint(1, 3)
            
            for j in range(n_accounts):
                account_type = random.choice(account_types)
                
                # Balance varies by account type
                if account_type == 'savings':
                    balance = random.uniform(100, 50000)
                elif account_type == 'checking':
                    balance = random.uniform(50, 10000)
                elif account_type == 'business':
                    balance = random.uniform(1000, 100000)
                else:  # investment
                    balance = random.uniform(5000, 200000)
                
                # Interest rate varies by account type
                if account_type == 'savings':
                    interest_rate = random.uniform(1.0, 3.0)
                elif account_type == 'investment':
                    interest_rate = random.uniform(3.0, 8.0)
                else:
                    interest_rate = random.uniform(0.0, 0.5)
                
                account = {
                    'account_id': f'ACC{i+1:05d}{j+1}',
                    'customer_id': customer['customer_id'],
                    'account_type': account_type,
                    'balance': round(balance, 2),
                    'currency': random.choice(currencies),
                    'opening_date': customer['registration_date'],
                    'status': random.choices(statuses, weights=[0.85, 0.10, 0.05])[0],
                    'interest_rate': round(interest_rate, 2),
                }
                
                accounts.append(account)
        
        return pd.DataFrame(accounts)
    
    def generate_complete_dataset(
        self,
        n_customers: int = 1000,
        avg_transactions_per_customer: int = 50
    ) -> Dict[str, pd.DataFrame]:
        """
        Generate complete dataset with customers, transactions, and accounts
        
        Args:
            n_customers: Number of customers
            avg_transactions_per_customer: Average transactions per customer
            
        Returns:
            Dictionary with all DataFrames
        """
        print(f"Generating {n_customers} customers...")
        customers_df = self.generate_customers(n_customers)
        
        print(f"Generating transactions...")
        transactions_df = self.generate_transactions(
            customers_df, avg_transactions_per_customer
        )
        
        print(f"Generating accounts...")
        accounts_df = self.generate_accounts(customers_df)
        
        print(f"Dataset generation complete!")
        print(f"  - Customers: {len(customers_df)}")
        print(f"  - Transactions: {len(transactions_df)}")
        print(f"  - Accounts: {len(accounts_df)}")
        
        return {
            'customers': customers_df,
            'transactions': transactions_df,
            'accounts': accounts_df,
        }
