# Quick Start Guide

Get your Equity Bank Risk Management System running in 10 minutes!

## 🚀 One-Command Setup

```bash
# 1. Run the automated setup
python setup.py

# 2. Configure your environment
cp risk_engine/.env.example risk_engine/.env
# Edit risk_engine/.env with your settings

# 3. Start everything
python start_system.py
```

## 🎯 What You Get

After running the setup, you'll have:

- **Real-time Transaction Monitoring** - Automatically scores and routes risky transactions
- **Analyst Workbench** - Queue of high-risk transactions for manual review
- **Risk Register** - Enterprise risk management across Credit, Liquidity, Market, etc.
- **Unified Dashboard** - Single view of all risk management activities
- **Sample Data** - 100+ test transactions to explore the system

## 📊 Access Your System

| Component | URL | Purpose |
|-----------|-----|---------|
| **Unified Dashboard** | http://localhost:8501 | Main interface for analysts and managers |
| **CISO Assistant** | https://localhost:8443 | Risk register and compliance management |
| **Database** | localhost:5432 | PostgreSQL with risk data |

## 🔧 Quick Configuration

### Essential Settings (risk_engine/.env)

```bash
# Database (use defaults for quick start)
DB_PASSWORD=risk_password

# Risk Thresholds (adjust for your bank)
HIGH_RISK_THRESHOLD=0.8        # Transactions above this go to analysts
AMOUNT_THRESHOLD_HIGH=10000000 # 10M KES triggers high risk
AMOUNT_THRESHOLD_MEDIUM=1000000 # 1M KES triggers medium risk

# Processing Speed
POLLING_INTERVAL_SECONDS=30    # How often to check for new transactions
```

### Connect Your Data Warehouse

Edit `risk_engine/database.py`, function `fetch_pending_transactions()`:

```python
def fetch_pending_transactions(self, limit=None):
    # Replace this query with your actual data warehouse connection
    query = """
    SELECT 
        transaction_id, customer_id, amount, currency,
        merchant_name, transaction_type, location, 
        channel, timestamp
    FROM your_warehouse.live_transactions 
    WHERE processed_flag = 0
    ORDER BY timestamp DESC
    """
    # ... rest stays the same
```

## 🧪 Test Your Setup

```bash
# Quick system test
python test_system.py --quick

# Generate more sample data
python test_data/generate_sample_data.py --count 200

# Full system test
python test_system.py
```

## 📈 Using the System

### 1. Monitor Transactions (Dashboard Overview)
- See real-time transaction volume and risk distribution
- Track high-risk cases and analyst performance
- Monitor portfolio-level risk metrics

### 2. Review Cases (Analyst Workbench)
- Queue of high/medium risk transactions
- Add comments and approve/reject/escalate
- Track case resolution times

### 3. Manage Enterprise Risk (Risk Register)
- Credit Risk, Liquidity Risk, Market Risk sections
- Risk assessment workflows
- Management reporting and dashboards

### 4. Deep Dive Analysis
- Transaction patterns and trends
- Risk score distributions
- Merchant and location analysis

## ⚡ Performance Tips

### For High Volume (>1000 TPS)
```bash
# In .env file
BATCH_SIZE=500
POLLING_INTERVAL_SECONDS=5

# Scale database
# Add more CPU/RAM to PostgreSQL container
```

### For Production
```bash
# Use managed database
DB_HOST=your-rds-endpoint.amazonaws.com

# Enable SSL
DB_SSL_MODE=require

# Set strong passwords
DB_PASSWORD=$(openssl rand -base64 32)
```

## 🔍 Troubleshooting

### Services Won't Start
```bash
# Check Docker
docker ps

# Check logs
docker-compose -f infrastructure/docker-compose.yml logs

# Restart services
docker-compose -f infrastructure/docker-compose.yml restart
```

### Dashboard Shows No Data
```bash
# Generate sample data
python test_data/generate_sample_data.py --count 100

# Check database connection
python test_system.py --quick
```

### Risk Engine Not Processing
```bash
# Check logs
tail -f risk_engine.log

# Run once manually
python risk_engine/main.py --once
```

## 🎯 Next Steps

1. **Customize Risk Models** - Edit `risk_engine/risk_models.py` for your specific risk criteria
2. **Add Real Data** - Connect to your core banking system or data warehouse
3. **Configure Alerts** - Set up email/SMS notifications for high-risk events
4. **Train Models** - Let the system run for a week to collect training data
5. **Add Users** - Create analyst and manager accounts in CISO Assistant

## 📚 Learn More

- **Full Documentation**: `docs/INSTALLATION.md`
- **Architecture Guide**: `docs/ARCHITECTURE.md`
- **API Reference**: Check each component's `/api/docs` endpoint
- **Community**: Join discussions on GitHub Issues

## 🆘 Need Help?

1. **Check Logs**: Most issues show up in the logs first
2. **Run Tests**: `python test_system.py` diagnoses common problems
3. **Sample Data**: Use `generate_sample_data.py` to create test scenarios
4. **Documentation**: Detailed guides in the `docs/` folder

---

**🎉 You're ready to start managing risk like a pro!**

The system is designed to learn and improve over time. The more transactions you process, the better the risk models become at detecting genuine threats while reducing false positives.