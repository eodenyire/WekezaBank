"""
Visualization utilities for analytics results
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Dict, List
import json


class AnalyticsVisualizer:
    """Create visualizations for analytics results"""
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize visualizer
        
        Args:
            style: Matplotlib style to use
        """
        try:
            plt.style.use(style)
        except:
            # Fallback to default if style not available
            pass
        
        sns.set_palette("husl")
        
    def plot_customer_segments(
        self,
        rfm_df: pd.DataFrame,
        save_path: Optional[str] = None
    ):
        """
        Visualize customer segments from RFM analysis
        
        Args:
            rfm_df: RFM analysis results
            save_path: Optional path to save the plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Segment distribution
        segment_counts = rfm_df['segment'].value_counts()
        axes[0, 0].bar(segment_counts.index, segment_counts.values)
        axes[0, 0].set_title('Customer Segment Distribution')
        axes[0, 0].set_xlabel('Segment')
        axes[0, 0].set_ylabel('Number of Customers')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # RFM Score distribution
        axes[0, 1].hist(rfm_df['recency'], bins=30, alpha=0.7, label='Recency')
        axes[0, 1].set_title('Recency Distribution')
        axes[0, 1].set_xlabel('Days Since Last Transaction')
        axes[0, 1].set_ylabel('Frequency')
        
        # Frequency vs Monetary scatter
        axes[1, 0].scatter(rfm_df['frequency'], rfm_df['monetary'], alpha=0.5)
        axes[1, 0].set_title('Frequency vs Monetary Value')
        axes[1, 0].set_xlabel('Transaction Frequency')
        axes[1, 0].set_ylabel('Total Monetary Value')
        
        # Top segments by value
        segment_value = rfm_df.groupby('segment')['monetary'].sum().sort_values(ascending=False)
        axes[1, 1].barh(segment_value.index, segment_value.values)
        axes[1, 1].set_title('Total Value by Segment')
        axes[1, 1].set_xlabel('Total Monetary Value')
        axes[1, 1].set_ylabel('Segment')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_transaction_trends(
        self,
        transactions_df: pd.DataFrame,
        save_path: Optional[str] = None
    ):
        """
        Visualize transaction trends over time
        
        Args:
            transactions_df: Transaction data
            save_path: Optional path to save the plot
        """
        transactions_df = transactions_df.copy()
        transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Daily transaction volume
        daily_volume = transactions_df.groupby(
            transactions_df['transaction_date'].dt.date
        )['amount'].sum()
        
        axes[0, 0].plot(daily_volume.index, daily_volume.values)
        axes[0, 0].set_title('Daily Transaction Volume')
        axes[0, 0].set_xlabel('Date')
        axes[0, 0].set_ylabel('Total Amount')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Transaction count by type
        if 'transaction_type' in transactions_df:
            type_counts = transactions_df['transaction_type'].value_counts()
            axes[0, 1].pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%')
            axes[0, 1].set_title('Transactions by Type')
        
        # Transaction amount distribution
        axes[1, 0].hist(transactions_df['amount'], bins=50, edgecolor='black')
        axes[1, 0].set_title('Transaction Amount Distribution')
        axes[1, 0].set_xlabel('Amount')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_yscale('log')
        
        # Spending by category
        if 'category' in transactions_df:
            category_spending = transactions_df.groupby('category')['amount'].sum().sort_values()
            axes[1, 1].barh(category_spending.index, category_spending.values)
            axes[1, 1].set_title('Spending by Category')
            axes[1, 1].set_xlabel('Total Amount')
            axes[1, 1].set_ylabel('Category')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_financial_metrics(
        self,
        metrics: Dict,
        save_path: Optional[str] = None
    ):
        """
        Visualize financial metrics
        
        Args:
            metrics: Financial metrics dictionary
            save_path: Optional path to save the plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # KPI Overview
        kpis = metrics.get('kpis', {})
        kpi_values = []
        kpi_labels = []
        
        if 'customer_metrics' in kpis:
            kpi_labels.append('Total Customers')
            kpi_values.append(kpis['customer_metrics'].get('total_customers', 0))
        
        if 'transaction_metrics' in kpis:
            kpi_labels.append('Total Transactions')
            kpi_values.append(kpis['transaction_metrics'].get('total_transactions', 0))
        
        axes[0, 0].bar(kpi_labels, kpi_values)
        axes[0, 0].set_title('Key Performance Indicators')
        axes[0, 0].set_ylabel('Count')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Profitability
        profitability = metrics.get('profitability', {})
        if profitability:
            prof_labels = ['Revenue', 'Costs', 'Profit']
            prof_values = [
                profitability.get('total_revenue', 0),
                profitability.get('total_costs', 0),
                profitability.get('gross_profit', 0)
            ]
            axes[0, 1].bar(prof_labels, prof_values)
            axes[0, 1].set_title('Profitability Metrics')
            axes[0, 1].set_ylabel('Amount')
        
        # Account health
        account_health = metrics.get('account_health', {})
        if 'by_status' in account_health:
            status_data = account_health['by_status']
            axes[1, 0].pie(status_data.values(), labels=status_data.keys(), autopct='%1.1f%%')
            axes[1, 0].set_title('Account Status Distribution')
        
        # Liquidity
        liquidity = metrics.get('liquidity', {})
        if liquidity:
            liq_labels = ['Total Deposits', 'Avg Deposit']
            liq_values = [
                liquidity.get('total_deposits', 0),
                liquidity.get('avg_deposit', 0)
            ]
            axes[1, 1].bar(liq_labels, liq_values)
            axes[1, 1].set_title('Liquidity Metrics')
            axes[1, 1].set_ylabel('Amount')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_risk_analysis(
        self,
        risk_df: pd.DataFrame,
        save_path: Optional[str] = None
    ):
        """
        Visualize risk analysis results
        
        Args:
            risk_df: Risk analysis results
            save_path: Optional path to save the plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Risk score distribution
        if 'credit_risk_score' in risk_df:
            axes[0, 0].hist(risk_df['credit_risk_score'], bins=30, edgecolor='black')
            axes[0, 0].set_title('Credit Risk Score Distribution')
            axes[0, 0].set_xlabel('Risk Score')
            axes[0, 0].set_ylabel('Frequency')
        
        # Risk category distribution
        if 'risk_category' in risk_df:
            category_counts = risk_df['risk_category'].value_counts()
            axes[0, 1].pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%')
            axes[0, 1].set_title('Risk Category Distribution')
        
        # Churn probability
        if 'churn_probability' in risk_df:
            axes[1, 0].hist(risk_df['churn_probability'], bins=30, edgecolor='black')
            axes[1, 0].set_title('Churn Probability Distribution')
            axes[1, 0].set_xlabel('Churn Probability')
            axes[1, 0].set_ylabel('Frequency')
        
        # Risk vs value scatter (if available)
        if 'credit_risk_score' in risk_df and 'clv' in risk_df:
            axes[1, 1].scatter(risk_df['credit_risk_score'], risk_df['clv'], alpha=0.5)
            axes[1, 1].set_title('Risk Score vs Customer Lifetime Value')
            axes[1, 1].set_xlabel('Credit Risk Score')
            axes[1, 1].set_ylabel('CLV')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_summary_report(
        self,
        results: Dict,
        output_path: str = 'analytics_report.txt'
    ):
        """
        Create a text summary report of analytics results
        
        Args:
            results: Analytics results dictionary
            output_path: Path to save the report
        """
        with open(output_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("WEKEZA BANK ANALYTICS REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Report Generated: {results.get('timestamp', 'N/A')}\n\n")
            
            # Customer Analytics
            if 'customer_analytics' in results:
                f.write("-" * 80 + "\n")
                f.write("CUSTOMER ANALYTICS\n")
                f.write("-" * 80 + "\n")
                
                demographics = results['customer_analytics'].get('demographics', {})
                f.write(f"Total Customers: {demographics.get('total_customers', 0)}\n")
                f.write(f"Average Credit Score: {demographics.get('avg_credit_score', 0):.2f}\n")
                f.write(f"Average Monthly Income: ${demographics.get('avg_monthly_income', 0):.2f}\n\n")
            
            # Transaction Analytics
            if 'transaction_analytics' in results:
                f.write("-" * 80 + "\n")
                f.write("TRANSACTION ANALYTICS\n")
                f.write("-" * 80 + "\n")
                
                metrics = results['transaction_analytics'].get('metrics', {})
                f.write(f"Total Transactions: {metrics.get('total_transactions', 0)}\n")
                f.write(f"Total Volume: ${metrics.get('total_volume', 0):.2f}\n")
                f.write(f"Average Transaction: ${metrics.get('avg_transaction_size', 0):.2f}\n\n")
            
            # Financial Metrics
            if 'financial_metrics' in results:
                f.write("-" * 80 + "\n")
                f.write("FINANCIAL METRICS\n")
                f.write("-" * 80 + "\n")
                
                kpis = results['financial_metrics'].get('kpis', {})
                prof = kpis.get('profitability', {})
                
                f.write(f"Total Revenue: ${prof.get('total_revenue', 0):.2f}\n")
                f.write(f"Total Costs: ${prof.get('total_costs', 0):.2f}\n")
                f.write(f"Gross Profit: ${prof.get('gross_profit', 0):.2f}\n")
                f.write(f"Profit Margin: {prof.get('profit_margin', 0):.2f}%\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
        
        print(f"Report saved to {output_path}")
