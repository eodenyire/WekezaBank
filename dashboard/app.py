import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import risk_engine modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'risk_engine'))
from config import Config
from database import DatabaseManager

# Page configuration
st.set_page_config(
    page_title="Wekeza Bank Risk Management Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def init_database():
    return DatabaseManager()

db = init_database()
config = Config()

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .high-risk { border-left-color: #d62728; }
    .medium-risk { border-left-color: #ff7f0e; }
    .low-risk { border-left-color: #2ca02c; }
</style>
""", unsafe_allow_html=True)

def load_analyst_cases():
    """Load analyst cases from database"""
    try:
        query = """
        SELECT 
            case_id, transaction_id, customer_id, amount, currency,
            merchant_name, risk_score, risk_level, status,
            flagged_reason, created_at, updated_at
        FROM analyst_cases 
        ORDER BY created_at DESC
        """
        return pd.read_sql(query, db.engine)
    except Exception as e:
        st.error(f"Error loading analyst cases: {e}")
        return pd.DataFrame()

def load_risk_metrics():
    """Load risk metrics from database"""
    try:
        query = """
        SELECT metric_type, metric_name, metric_value, threshold_value, 
               status, calculated_at
        FROM risk_metrics 
        WHERE date(calculated_at) >= date('now', '-7 days')
        ORDER BY calculated_at DESC
        """
        return pd.read_sql(query, db.engine)
    except Exception as e:
        st.error(f"Error loading risk metrics: {e}")
        return pd.DataFrame()

def load_transaction_history():
    """Load recent transaction history"""
    try:
        query = """
        SELECT transaction_id, customer_id, amount, transaction_type,
               merchant_name, location, channel, timestamp, status
        FROM transaction_history 
        WHERE date(timestamp) >= date('now', '-7 days')
        ORDER BY timestamp DESC
        LIMIT 1000
        """
        return pd.read_sql(query, db.engine)
    except Exception as e:
        st.error(f"Error loading transaction history: {e}")
        return pd.DataFrame()

def update_case_status(case_id, new_status, comment):
    """Update analyst case status"""
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE analyst_cases 
            SET status = ?, analyst_comment = ?, updated_at = ?
            WHERE case_id = ?
        """, (new_status, comment, datetime.now(), case_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error updating case: {e}")
        return False

# Sidebar navigation
st.sidebar.title("🛡️ Risk Management")
page = st.sidebar.selectbox(
    "Navigate to:",
    ["Dashboard Overview", "Analyst Workbench", "Risk Register", "Transaction Monitor", "Deep Dive Analytics"]
)

# Main content based on selected page
if page == "Dashboard Overview":
    st.title("Risk Management Dashboard Overview")
    
    # Load data
    cases_df = load_analyst_cases()
    metrics_df = load_risk_metrics()
    transactions_df = load_transaction_history()
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_cases = len(cases_df)
        st.metric("Total Cases", total_cases)
    
    with col2:
        high_risk_cases = len(cases_df[cases_df['risk_level'] == 'HIGH'])
        st.metric("High Risk Cases", high_risk_cases, delta=f"{high_risk_cases/max(total_cases,1)*100:.1f}%")
    
    with col3:
        pending_cases = len(cases_df[cases_df['status'] == 'ASSIGNED'])
        st.metric("Pending Review", pending_cases)
    
    with col4:
        total_amount = transactions_df['amount'].sum() if not transactions_df.empty else 0
        st.metric("Daily Volume", f"KES {total_amount:,.0f}")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        if not cases_df.empty:
            # Risk level distribution
            risk_counts = cases_df['risk_level'].value_counts()
            fig_risk = px.pie(
                values=risk_counts.values, 
                names=risk_counts.index,
                title="Risk Level Distribution",
                color_discrete_map={'HIGH': '#d62728', 'MEDIUM': '#ff7f0e', 'LOW': '#2ca02c'}
            )
            st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        if not cases_df.empty:
            # Case status distribution
            status_counts = cases_df['status'].value_counts()
            fig_status = px.bar(
                x=status_counts.index, 
                y=status_counts.values,
                title="Case Status Distribution",
                labels={'x': 'Status', 'y': 'Count'}
            )
            st.plotly_chart(fig_status, use_container_width=True)
    
    # Recent high-risk cases
    st.subheader("Recent High-Risk Cases")
    if not cases_df.empty:
        high_risk = cases_df[cases_df['risk_level'] == 'HIGH'].head(10)
        if not high_risk.empty:
            st.dataframe(
                high_risk[['case_id', 'transaction_id', 'amount', 'merchant_name', 'risk_score', 'status', 'created_at']],
                use_container_width=True
            )
        else:
            st.info("No high-risk cases in recent data")
    else:
        st.info("No case data available")

elif page == "Analyst Workbench":
    st.title("🚨 Analyst Workbench")
    
    # Load cases
    cases_df = load_analyst_cases()
    
    if cases_df.empty:
        st.info("No cases available for review")
    else:
        # Filter controls
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All"] + list(cases_df['status'].unique()))
        with col2:
            risk_filter = st.selectbox("Filter by Risk Level", ["All"] + list(cases_df['risk_level'].unique()))
        with col3:
            sort_by = st.selectbox("Sort by", ["Created Date", "Risk Score", "Amount"])
        
        # Apply filters
        filtered_cases = cases_df.copy()
        if status_filter != "All":
            filtered_cases = filtered_cases[filtered_cases['status'] == status_filter]
        if risk_filter != "All":
            filtered_cases = filtered_cases[filtered_cases['risk_level'] == risk_filter]
        
        # Sort
        if sort_by == "Risk Score":
            filtered_cases = filtered_cases.sort_values('risk_score', ascending=False)
        elif sort_by == "Amount":
            filtered_cases = filtered_cases.sort_values('amount', ascending=False)
        else:
            filtered_cases = filtered_cases.sort_values('created_at', ascending=False)
        
        st.write(f"Showing {len(filtered_cases)} cases")
        
        # Display cases for review
        for idx, case in filtered_cases.iterrows():
            with st.expander(f"Case #{case['case_id']} - {case['transaction_id']} - Risk: {case['risk_level']} ({case['risk_score']:.3f})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Transaction Details:**")
                    st.write(f"- Amount: KES {case['amount']:,.2f}")
                    st.write(f"- Customer: {case['customer_id']}")
                    st.write(f"- Merchant: {case['merchant_name']}")
                    st.write(f"- Status: {case['status']}")
                    st.write(f"- Created: {case['created_at']}")
                    
                    st.write("**Risk Analysis:**")
                    st.write(f"- Risk Score: {case['risk_score']:.3f}")
                    st.write(f"- Risk Level: {case['risk_level']}")
                    st.write(f"- Flagged Reason: {case['flagged_reason']}")
                
                with col2:
                    st.write("**Analyst Actions:**")
                    
                    # Only show actions for pending cases
                    if case['status'] == 'ASSIGNED':
                        comment = st.text_area(f"Analysis Comment", key=f"comment_{case['case_id']}")
                        
                        col_btn1, col_btn2, col_btn3 = st.columns(3)
                        
                        with col_btn1:
                            if st.button("✅ Approve (False Positive)", key=f"approve_{case['case_id']}"):
                                if update_case_status(case['case_id'], 'CLOSED', f"Approved: {comment}"):
                                    st.success("Case approved and closed")
                                    st.rerun()
                        
                        with col_btn2:
                            if st.button("⚠️ Escalate", key=f"escalate_{case['case_id']}"):
                                if update_case_status(case['case_id'], 'ESCALATED', f"Escalated: {comment}"):
                                    st.warning("Case escalated to manager")
                                    st.rerun()
                        
                        with col_btn3:
                            if st.button("🚫 Block Transaction", key=f"block_{case['case_id']}"):
                                if update_case_status(case['case_id'], 'BLOCKED', f"Blocked: {comment}"):
                                    st.error("Transaction blocked")
                                    st.rerun()
                    else:
                        st.info(f"Case status: {case['status']}")
                        if case.get('analyst_comment'):
                            st.write(f"**Previous Comment:** {case['analyst_comment']}")

elif page == "Risk Register":
    st.title("📚 Enterprise Risk Register")
    
    # Risk categories
    risk_categories = ["Credit Risk", "Liquidity Risk", "Market Risk", "Technology Risk", "Model Risk", "Research Risk", "Operational Risk"]
    
    selected_category = st.selectbox("Select Risk Category", risk_categories)
    
    # Load risk metrics for selected category
    metrics_df = load_risk_metrics()
    
    if not metrics_df.empty:
        category_metrics = metrics_df[metrics_df['metric_type'].str.upper() == selected_category.split()[0].upper()]
        
        if not category_metrics.empty:
            st.subheader(f"{selected_category} Metrics")
            
            # Display metrics as cards
            for _, metric in category_metrics.iterrows():
                status_color = {
                    'OK': 'low-risk',
                    'WARNING': 'medium-risk', 
                    'CRITICAL': 'high-risk'
                }.get(metric['status'], 'low-risk')
                
                st.markdown(f"""
                <div class="metric-card {status_color}">
                    <h4>{metric['metric_name']}</h4>
                    <p><strong>Value:</strong> {metric['metric_value']:.4f}</p>
                    <p><strong>Threshold:</strong> {metric['threshold_value']:.4f}</p>
                    <p><strong>Status:</strong> {metric['status']}</p>
                    <p><strong>Last Updated:</strong> {metric['calculated_at']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.write("")
        else:
            st.info(f"No metrics available for {selected_category}")
    
    # Add new risk entry
    st.subheader("Add New Risk Entry")
    with st.form("add_risk"):
        risk_name = st.text_input("Risk Name")
        risk_description = st.text_area("Risk Description")
        likelihood = st.selectbox("Likelihood", [1, 2, 3, 4, 5])
        impact = st.selectbox("Impact", [1, 2, 3, 4, 5])
        
        if st.form_submit_button("Add Risk"):
            # Here you would integrate with CISO Assistant API
            st.success(f"Risk '{risk_name}' added to {selected_category} register")

elif page == "Transaction Monitor":
    st.title("💳 Real-Time Transaction Monitor")
    
    transactions_df = load_transaction_history()
    
    if not transactions_df.empty:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_txns = len(transactions_df)
            st.metric("Total Transactions", total_txns)
        
        with col2:
            total_volume = transactions_df['amount'].sum()
            st.metric("Total Volume", f"KES {total_volume:,.0f}")
        
        with col3:
            avg_amount = transactions_df['amount'].mean()
            st.metric("Average Amount", f"KES {avg_amount:,.0f}")
        
        with col4:
            blocked_txns = len(transactions_df[transactions_df['status'] == 'BLOCKED'])
            st.metric("Blocked Transactions", blocked_txns)
        
        # Transaction volume over time
        if 'timestamp' in transactions_df.columns:
            transactions_df['hour'] = pd.to_datetime(transactions_df['timestamp']).dt.hour
            hourly_volume = transactions_df.groupby('hour')['amount'].sum().reset_index()
            
            fig_volume = px.line(
                hourly_volume, 
                x='hour', 
                y='amount',
                title="Transaction Volume by Hour",
                labels={'hour': 'Hour of Day', 'amount': 'Volume (KES)'}
            )
            st.plotly_chart(fig_volume, use_container_width=True)
        
        # Recent transactions table
        st.subheader("Recent Transactions")
        st.dataframe(
            transactions_df.head(50)[['transaction_id', 'amount', 'transaction_type', 'merchant_name', 'status', 'timestamp']],
            use_container_width=True
        )
    else:
        st.info("No transaction data available")

elif page == "Deep Dive Analytics":
    st.title("🔍 Deep Dive Analytics")
    
    # Load all data
    cases_df = load_analyst_cases()
    transactions_df = load_transaction_history()
    
    if not cases_df.empty and not transactions_df.empty:
        # Risk score distribution
        fig_risk_dist = px.histogram(
            cases_df, 
            x='risk_score', 
            nbins=20,
            title="Risk Score Distribution",
            labels={'risk_score': 'Risk Score', 'count': 'Number of Cases'}
        )
        st.plotly_chart(fig_risk_dist, use_container_width=True)
        
        # Amount vs Risk Score scatter
        fig_scatter = px.scatter(
            cases_df, 
            x='amount', 
            y='risk_score',
            color='risk_level',
            title="Transaction Amount vs Risk Score",
            labels={'amount': 'Amount (KES)', 'risk_score': 'Risk Score'},
            color_discrete_map={'HIGH': '#d62728', 'MEDIUM': '#ff7f0e', 'LOW': '#2ca02c'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Risk by merchant analysis
        if 'merchant_name' in cases_df.columns:
            merchant_risk = cases_df.groupby('merchant_name').agg({
                'risk_score': 'mean',
                'case_id': 'count'
            }).reset_index()
            merchant_risk.columns = ['merchant_name', 'avg_risk_score', 'case_count']
            merchant_risk = merchant_risk[merchant_risk['case_count'] >= 2]  # Only merchants with 2+ cases
            
            if not merchant_risk.empty:
                fig_merchant = px.bar(
                    merchant_risk.sort_values('avg_risk_score', ascending=False).head(10),
                    x='merchant_name',
                    y='avg_risk_score',
                    title="Average Risk Score by Merchant (Top 10)",
                    labels={'merchant_name': 'Merchant', 'avg_risk_score': 'Average Risk Score'}
                )
                fig_merchant.update_xaxis(tickangle=45)
                st.plotly_chart(fig_merchant, use_container_width=True)
    else:
        st.info("Insufficient data for deep dive analytics")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Wekeza Bank Risk Management System**")
st.sidebar.markdown("Powered by Open Source Tools")
st.sidebar.markdown("- Ballerine (Case Management)")
st.sidebar.markdown("- CISO Assistant (Risk Register)")
st.sidebar.markdown("- Tazama (Fraud Detection)")