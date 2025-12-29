"""
Financial Metrics Module

Provides financial KPIs and metrics including:
- Revenue analysis
- Profitability metrics
- Account health metrics
- Portfolio performance
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class FinancialMetrics:
    """Financial metrics and KPI calculator for Wekeza Bank"""
    
    def calculate_revenue_metrics(
        self,
        transactions_df: pd.DataFrame,
        period: str = 'monthly'
    ) -> Dict:
        """
        Calculate revenue metrics
        
        Args:
            transactions_df: Transaction data
            period: Time period for aggregation
            
        Returns:
            Dictionary with revenue metrics
        """
        # Filter credit transactions (income)
        if 'transaction_type' in transactions_df:
            revenue_df = transactions_df[transactions_df['transaction_type'] == 'credit'].copy()
        else:
            revenue_df = transactions_df.copy()
        
        metrics = {
            'total_revenue': float(revenue_df['amount'].sum()),
            'avg_transaction_revenue': float(revenue_df['amount'].mean()),
            'transaction_count': len(revenue_df),
        }
        
        # Revenue by period
        if 'transaction_date' in revenue_df:
            revenue_df['transaction_date'] = pd.to_datetime(revenue_df['transaction_date'])
            
            freq_map = {'daily': 'D', 'weekly': 'W', 'monthly': 'M', 'quarterly': 'Q', 'yearly': 'Y'}
            freq = freq_map.get(period, 'M')
            
            revenue_by_period = revenue_df.groupby(
                pd.Grouper(key='transaction_date', freq=freq)
            )['amount'].sum()
            
            metrics['revenue_by_period'] = revenue_by_period.to_dict()
            metrics['avg_period_revenue'] = float(revenue_by_period.mean())
            metrics['revenue_growth_rate'] = self._calculate_growth_rate(revenue_by_period)
        
        return metrics
    
    def _calculate_growth_rate(self, series: pd.Series) -> Optional[float]:
        """Calculate growth rate from a time series"""
        if len(series) < 2:
            return None
        
        # Calculate period-over-period growth
        growth_rates = series.pct_change().dropna()
        return float(growth_rates.mean() * 100) if len(growth_rates) > 0 else None
    
    def calculate_account_health_metrics(
        self,
        accounts_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate account health metrics
        
        Args:
            accounts_df: Account data
            
        Returns:
            Dictionary with account health metrics
        """
        metrics = {
            'total_accounts': len(accounts_df),
            'total_balance': float(accounts_df['balance'].sum()),
            'avg_balance': float(accounts_df['balance'].mean()),
            'median_balance': float(accounts_df['balance'].median()),
        }
        
        # Account status distribution
        if 'status' in accounts_df:
            metrics['by_status'] = accounts_df['status'].value_counts().to_dict()
            metrics['active_account_rate'] = float(
                (accounts_df['status'] == 'active').sum() / len(accounts_df) * 100
            )
        
        # Account type distribution
        if 'account_type' in accounts_df:
            metrics['by_type'] = accounts_df['account_type'].value_counts().to_dict()
            metrics['balance_by_type'] = accounts_df.groupby('account_type')['balance'].sum().to_dict()
        
        # Low balance accounts
        low_balance_threshold = 100
        metrics['low_balance_accounts'] = int((accounts_df['balance'] < low_balance_threshold).sum())
        metrics['low_balance_rate'] = float(
            (accounts_df['balance'] < low_balance_threshold).sum() / len(accounts_df) * 100
        )
        
        return metrics
    
    def calculate_portfolio_metrics(
        self,
        accounts_df: pd.DataFrame,
        transactions_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate portfolio performance metrics
        
        Args:
            accounts_df: Account data
            transactions_df: Transaction data
            
        Returns:
            Dictionary with portfolio metrics
        """
        metrics = {
            'total_aum': float(accounts_df['balance'].sum()),  # Assets Under Management
            'account_count': len(accounts_df),
            'avg_account_balance': float(accounts_df['balance'].mean()),
        }
        
        # Customer concentration
        if 'customer_id' in accounts_df:
            customer_balances = accounts_df.groupby('customer_id')['balance'].sum()
            total_balance = customer_balances.sum()
            
            # Top 10% customers
            top_10_pct = customer_balances.nlargest(int(len(customer_balances) * 0.1))
            metrics['top_10_pct_concentration'] = float(
                top_10_pct.sum() / total_balance * 100 if total_balance > 0 else 0
            )
        
        # Transaction activity
        if len(transactions_df) > 0:
            metrics['total_transaction_volume'] = float(transactions_df['amount'].sum())
            metrics['transaction_count'] = len(transactions_df)
            metrics['avg_transaction_size'] = float(transactions_df['amount'].mean())
        
        return metrics
    
    def calculate_profitability_metrics(
        self,
        transactions_df: pd.DataFrame,
        accounts_df: Optional[pd.DataFrame] = None
    ) -> Dict:
        """
        Calculate profitability metrics
        
        Args:
            transactions_df: Transaction data
            accounts_df: Optional account data for additional metrics
            
        Returns:
            Dictionary with profitability metrics
        """
        # Separate revenue (credits) and costs (debits)
        if 'transaction_type' in transactions_df:
            revenue = transactions_df[transactions_df['transaction_type'] == 'credit']['amount'].sum()
            costs = transactions_df[transactions_df['transaction_type'] == 'debit']['amount'].sum()
        else:
            # Assume positive amounts are revenue, negative are costs
            revenue = transactions_df[transactions_df['amount'] > 0]['amount'].sum()
            costs = abs(transactions_df[transactions_df['amount'] < 0]['amount'].sum())
        
        profit = revenue - costs
        
        metrics = {
            'total_revenue': float(revenue),
            'total_costs': float(costs),
            'gross_profit': float(profit),
            'profit_margin': float((profit / revenue * 100) if revenue > 0 else 0),
        }
        
        # Add interest income if available
        if accounts_df is not None and 'interest_rate' in accounts_df:
            total_interest = (
                accounts_df['balance'] * accounts_df['interest_rate'] / 100
            ).sum()
            metrics['interest_income'] = float(total_interest)
        
        return metrics
    
    def calculate_kpis(
        self,
        transactions_df: pd.DataFrame,
        accounts_df: pd.DataFrame,
        customers_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate key performance indicators (KPIs)
        
        Args:
            transactions_df: Transaction data
            accounts_df: Account data
            customers_df: Customer data
            
        Returns:
            Dictionary with comprehensive KPIs
        """
        kpis = {
            'customer_metrics': {
                'total_customers': len(customers_df),
                'customers_per_account': float(len(customers_df) / len(accounts_df)) if len(accounts_df) > 0 else 0,
            },
            'account_metrics': self.calculate_account_health_metrics(accounts_df),
            'transaction_metrics': {
                'total_transactions': len(transactions_df),
                'total_volume': float(transactions_df['amount'].sum()),
                'avg_transaction_size': float(transactions_df['amount'].mean()),
            },
            'profitability': self.calculate_profitability_metrics(transactions_df, accounts_df),
        }
        
        # Calculate customer-level metrics
        if len(transactions_df) > 0 and len(customers_df) > 0:
            kpis['customer_metrics']['avg_transactions_per_customer'] = float(
                len(transactions_df) / len(customers_df)
            )
        
        return kpis
    
    def calculate_liquidity_metrics(
        self,
        accounts_df: pd.DataFrame
    ) -> Dict:
        """
        Calculate liquidity metrics
        
        Args:
            accounts_df: Account data
            
        Returns:
            Dictionary with liquidity metrics
        """
        total_balance = accounts_df['balance'].sum()
        
        metrics = {
            'total_deposits': float(total_balance),
            'avg_deposit': float(accounts_df['balance'].mean()),
            'median_deposit': float(accounts_df['balance'].median()),
        }
        
        # Deposit concentration
        if len(accounts_df) > 0:
            sorted_balances = accounts_df['balance'].sort_values(ascending=False)
            
            # Top 10 accounts concentration
            top_10_balance = sorted_balances.head(10).sum()
            metrics['top_10_accounts_concentration'] = float(
                (top_10_balance / total_balance * 100) if total_balance > 0 else 0
            )
        
        # Account type distribution
        if 'account_type' in accounts_df:
            type_balances = accounts_df.groupby('account_type')['balance'].sum()
            metrics['deposits_by_type'] = type_balances.to_dict()
        
        return metrics
