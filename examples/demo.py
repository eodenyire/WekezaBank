#!/usr/bin/env python3
"""
Example script demonstrating the Wekeza Bank Analytics Framework

This script shows how to:
1. Generate sample data
2. Run analytics workflows
3. Generate visualizations
4. Create reports
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wekeza_analytics.utils import DataGenerator, AnalyticsVisualizer
from wekeza_analytics.workflows import AnalyticsWorkflow
import json


def main():
    """Main execution function"""
    
    print("=" * 80)
    print("WEKEZA BANK ADVANCED ANALYTICS DEMO")
    print("=" * 80)
    print()
    
    # Step 1: Generate sample data
    print("Step 1: Generating sample data...")
    print("-" * 80)
    
    generator = DataGenerator(seed=42)
    data = generator.generate_complete_dataset(
        n_customers=500,
        avg_transactions_per_customer=30
    )
    
    customers_df = data['customers']
    transactions_df = data['transactions']
    accounts_df = data['accounts']
    
    print()
    
    # Step 2: Run analytics workflows
    print("Step 2: Running analytics workflows...")
    print("-" * 80)
    
    workflow = AnalyticsWorkflow()
    
    # Run full analysis
    results = workflow.run_full_analysis(
        customers_df=customers_df,
        transactions_df=transactions_df,
        accounts_df=accounts_df
    )
    
    print()
    
    # Step 3: Display key insights
    print("Step 3: Key Insights")
    print("-" * 80)
    
    # Customer insights
    if 'customer_analytics' in results:
        demographics = results['customer_analytics'].get('demographics', {})
        print(f"\nCustomer Insights:")
        print(f"  Total Customers: {demographics.get('total_customers', 0)}")
        print(f"  Average Credit Score: {demographics.get('avg_credit_score', 0):.2f}")
        print(f"  Average Monthly Income: ${demographics.get('avg_monthly_income', 0):,.2f}")
    
    # Transaction insights
    if 'transaction_analytics' in results:
        metrics = results['transaction_analytics'].get('metrics', {})
        print(f"\nTransaction Insights:")
        print(f"  Total Transactions: {metrics.get('total_transactions', 0):,}")
        print(f"  Total Volume: ${metrics.get('total_volume', 0):,.2f}")
        print(f"  Average Transaction: ${metrics.get('avg_transaction_size', 0):.2f}")
    
    # Financial insights
    if 'financial_metrics' in results:
        kpis = results['financial_metrics'].get('kpis', {})
        prof = kpis.get('profitability', {})
        print(f"\nFinancial Insights:")
        print(f"  Total Revenue: ${prof.get('total_revenue', 0):,.2f}")
        print(f"  Total Costs: ${prof.get('total_costs', 0):,.2f}")
        print(f"  Gross Profit: ${prof.get('gross_profit', 0):,.2f}")
        print(f"  Profit Margin: {prof.get('profit_margin', 0):.2f}%")
    
    print()
    
    # Step 4: Save results
    print("Step 4: Saving results...")
    print("-" * 80)
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Save JSON results
    with open('output/analytics_results.json', 'w') as f:
        # Convert DataFrames to serializable format
        serializable_results = {}
        for key, value in results.items():
            if isinstance(value, dict):
                serializable_results[key] = value
            else:
                serializable_results[key] = str(value)
        
        json.dump(serializable_results, f, indent=2, default=str)
    
    print("  ✓ Results saved to output/analytics_results.json")
    
    # Create visualizations
    print("\nStep 5: Creating visualizations...")
    print("-" * 80)
    
    visualizer = AnalyticsVisualizer()
    
    # Customer segment visualization
    try:
        if 'customer_analytics' in results and 'rfm' in results['customer_analytics']:
            import pandas as pd
            rfm_df = pd.DataFrame(results['customer_analytics']['rfm'])
            visualizer.plot_customer_segments(rfm_df, 'output/customer_segments.png')
            print("  ✓ Customer segments visualization saved")
    except Exception as e:
        print(f"  ✗ Could not create customer segments visualization: {e}")
    
    # Transaction trends visualization
    try:
        visualizer.plot_transaction_trends(transactions_df, 'output/transaction_trends.png')
        print("  ✓ Transaction trends visualization saved")
    except Exception as e:
        print(f"  ✗ Could not create transaction trends visualization: {e}")
    
    # Financial metrics visualization
    try:
        visualizer.plot_financial_metrics(results['financial_metrics'], 'output/financial_metrics.png')
        print("  ✓ Financial metrics visualization saved")
    except Exception as e:
        print(f"  ✗ Could not create financial metrics visualization: {e}")
    
    # Risk analysis visualization
    try:
        if 'predictive_analytics' in results and 'credit_risk' in results['predictive_analytics']:
            import pandas as pd
            risk_df = pd.DataFrame(results['predictive_analytics']['credit_risk'])
            visualizer.plot_risk_analysis(risk_df, 'output/risk_analysis.png')
            print("  ✓ Risk analysis visualization saved")
    except Exception as e:
        print(f"  ✗ Could not create risk analysis visualization: {e}")
    
    # Create summary report
    visualizer.create_summary_report(results, 'output/analytics_report.txt')
    print("  ✓ Summary report saved to output/analytics_report.txt")
    
    print()
    print("=" * 80)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\nOutput files saved to the 'output' directory:")
    print("  - analytics_results.json")
    print("  - customer_segments.png")
    print("  - transaction_trends.png")
    print("  - financial_metrics.png")
    print("  - risk_analysis.png")
    print("  - analytics_report.txt")
    print()


if __name__ == "__main__":
    main()
