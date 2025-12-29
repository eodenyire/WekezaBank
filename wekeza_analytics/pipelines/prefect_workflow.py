"""
Prefect workflow example for Wekeza Bank Analytics

This demonstrates how to orchestrate analytics workflows using Prefect.
"""

from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wekeza_analytics.workflows import AnalyticsWorkflow
from wekeza_analytics.utils import DataGenerator, AnalyticsVisualizer


@task(name="Generate Sample Data", retries=2)
def generate_sample_data(n_customers: int = 1000, n_transactions: int = 50):
    """Generate sample banking data"""
    print(f"Generating data for {n_customers} customers...")
    generator = DataGenerator(seed=42)
    data = generator.generate_complete_dataset(
        n_customers=n_customers,
        avg_transactions_per_customer=n_transactions
    )
    return data


@task(name="Validate Data Quality", retries=1)
def validate_data(data: dict):
    """Validate data quality"""
    print("Validating data quality...")
    
    checks = {
        'customers_not_empty': len(data['customers']) > 0,
        'transactions_not_empty': len(data['transactions']) > 0,
        'accounts_not_empty': len(data['accounts']) > 0,
        'no_null_customer_ids': data['customers']['customer_id'].notna().all(),
        'no_null_transaction_ids': data['transactions']['transaction_id'].notna().all(),
    }
    
    if not all(checks.values()):
        failed_checks = [k for k, v in checks.items() if not v]
        raise ValueError(f"Data quality checks failed: {failed_checks}")
    
    print("✓ All data quality checks passed")
    return data


@task(name="Run Customer Analytics", retries=1)
def run_customer_analytics(data: dict):
    """Run customer analytics workflow"""
    print("Running customer analytics...")
    workflow = AnalyticsWorkflow()
    results = workflow.run_customer_workflow(
        customers_df=data['customers'],
        transactions_df=data['transactions']
    )
    print("✓ Customer analytics completed")
    return results


@task(name="Run Transaction Analytics", retries=1)
def run_transaction_analytics(data: dict):
    """Run transaction analytics workflow"""
    print("Running transaction analytics...")
    workflow = AnalyticsWorkflow()
    results = workflow.run_transaction_workflow(
        transactions_df=data['transactions']
    )
    print("✓ Transaction analytics completed")
    return results


@task(name="Run Financial Analytics", retries=1)
def run_financial_analytics(data: dict):
    """Run financial analytics workflow"""
    print("Running financial analytics...")
    workflow = AnalyticsWorkflow()
    results = workflow.run_financial_workflow(
        transactions_df=data['transactions'],
        accounts_df=data['accounts'],
        customers_df=data['customers']
    )
    print("✓ Financial analytics completed")
    return results


@task(name="Run Predictive Analytics", retries=1)
def run_predictive_analytics(data: dict):
    """Run predictive analytics workflow"""
    print("Running predictive analytics...")
    workflow = AnalyticsWorkflow()
    results = workflow.run_predictive_workflow(
        customers_df=data['customers'],
        transactions_df=data['transactions']
    )
    print("✓ Predictive analytics completed")
    return results


@task(name="Combine Results", retries=1)
def combine_results(customer_results, transaction_results, financial_results, predictive_results):
    """Combine all analytics results"""
    print("Combining results...")
    combined = {
        'timestamp': datetime.now().isoformat(),
        'customer_analytics': customer_results,
        'transaction_analytics': transaction_results,
        'financial_metrics': financial_results,
        'predictive_analytics': predictive_results,
    }
    print("✓ Results combined")
    return combined


@task(name="Generate Visualizations", retries=1)
def generate_visualizations(data: dict, results: dict):
    """Generate visualizations"""
    print("Generating visualizations...")
    
    os.makedirs('output', exist_ok=True)
    visualizer = AnalyticsVisualizer()
    
    try:
        # Customer segments
        if 'rfm_analysis' in results['customer_analytics']:
            rfm_df = pd.DataFrame(results['customer_analytics']['rfm_analysis'])
            visualizer.plot_customer_segments(rfm_df, 'output/customer_segments.png')
            print("  ✓ Customer segments chart created")
        
        # Transaction trends
        visualizer.plot_transaction_trends(data['transactions'], 'output/transaction_trends.png')
        print("  ✓ Transaction trends chart created")
        
        # Financial metrics
        visualizer.plot_financial_metrics(results['financial_metrics'], 'output/financial_metrics.png')
        print("  ✓ Financial metrics chart created")
        
        # Risk analysis
        if 'credit_risk_scores' in results['predictive_analytics']:
            risk_df = pd.DataFrame(results['predictive_analytics']['credit_risk_scores'])
            visualizer.plot_risk_analysis(risk_df, 'output/risk_analysis.png')
            print("  ✓ Risk analysis chart created")
    
    except Exception as e:
        print(f"  ⚠ Warning: Could not create some visualizations: {e}")
    
    print("✓ Visualizations completed")
    return True


@task(name="Generate Report", retries=1)
def generate_report(results: dict):
    """Generate summary report"""
    print("Generating report...")
    
    os.makedirs('output', exist_ok=True)
    visualizer = AnalyticsVisualizer()
    visualizer.create_summary_report(results, 'output/analytics_report.txt')
    
    print("✓ Report generated: output/analytics_report.txt")
    return 'output/analytics_report.txt'


@task(name="Save Results", retries=1)
def save_results(results: dict):
    """Save results to JSON"""
    import json
    
    print("Saving results...")
    os.makedirs('output', exist_ok=True)
    
    with open('output/analytics_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("✓ Results saved: output/analytics_results.json")
    return 'output/analytics_results.json'


@flow(
    name="Daily Analytics Workflow",
    description="Daily analytics workflow for Wekeza Bank",
    task_runner=ConcurrentTaskRunner()
)
def daily_analytics_flow(n_customers: int = 1000):
    """
    Main analytics workflow that runs daily
    
    Args:
        n_customers: Number of customers to process
    """
    print("=" * 80)
    print("WEKEZA BANK DAILY ANALYTICS WORKFLOW")
    print("=" * 80)
    print()
    
    # Step 1: Generate/Extract Data
    data = generate_sample_data(n_customers=n_customers, n_transactions=50)
    
    # Step 2: Validate Data
    validated_data = validate_data(data)
    
    # Step 3: Run Analytics (in parallel)
    customer_results = run_customer_analytics(validated_data)
    transaction_results = run_transaction_analytics(validated_data)
    financial_results = run_financial_analytics(validated_data)
    predictive_results = run_predictive_analytics(validated_data)
    
    # Step 4: Combine Results
    combined_results = combine_results(
        customer_results,
        transaction_results,
        financial_results,
        predictive_results
    )
    
    # Step 5: Generate Outputs
    save_results(combined_results)
    generate_visualizations(validated_data, combined_results)
    generate_report(combined_results)
    
    print()
    print("=" * 80)
    print("WORKFLOW COMPLETED SUCCESSFULLY")
    print("=" * 80)
    
    return combined_results


@flow(
    name="Weekly Customer Insights",
    description="Weekly customer analytics and segmentation"
)
def weekly_customer_flow(n_customers: int = 1000):
    """Weekly customer insights workflow"""
    print("Running weekly customer insights workflow...")
    
    # Generate data
    data = generate_sample_data(n_customers=n_customers)
    validated_data = validate_data(data)
    
    # Run customer analytics
    results = run_customer_analytics(validated_data)
    
    # Generate visualizations
    if 'rfm_analysis' in results:
        os.makedirs('output', exist_ok=True)
        visualizer = AnalyticsVisualizer()
        rfm_df = pd.DataFrame(results['rfm_analysis'])
        visualizer.plot_customer_segments(rfm_df, 'output/weekly_customer_segments.png')
    
    print("Weekly customer insights workflow completed")
    return results


@flow(
    name="Monthly Financial Report",
    description="Monthly financial reporting workflow"
)
def monthly_financial_flow(n_customers: int = 1000):
    """Monthly financial reporting workflow"""
    print("Running monthly financial report workflow...")
    
    # Generate data
    data = generate_sample_data(n_customers=n_customers)
    validated_data = validate_data(data)
    
    # Run financial analytics
    results = run_financial_analytics(validated_data)
    
    # Generate report
    os.makedirs('output', exist_ok=True)
    visualizer = AnalyticsVisualizer()
    
    # Create comprehensive financial report
    report = {
        'timestamp': datetime.now().isoformat(),
        'financial_metrics': results
    }
    
    visualizer.create_summary_report(report, 'output/monthly_financial_report.txt')
    visualizer.plot_financial_metrics(results, 'output/monthly_financial_metrics.png')
    
    print("Monthly financial report workflow completed")
    return results


if __name__ == "__main__":
    # Run the daily analytics workflow
    result = daily_analytics_flow(n_customers=500)
    print("\nWorkflow execution completed!")
