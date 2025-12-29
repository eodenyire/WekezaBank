# Installation Guide

## Prerequisites

Before installing the Equity Bank Risk Management System, ensure you have:

1. **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop/)
2. **Python 3.8+** - [Download here](https://www.python.org/downloads/)
3. **Git** - [Download here](https://git-scm.com/downloads)

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd equity-risk-management

# Run the automated setup
python setup.py
```

### 2. Configure Environment

Edit `risk_engine/.env` with your database credentials:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=transactions_db
DB_USER=risk_user
DB_PASSWORD=your_secure_password

# Risk Thresholds (adjust as needed)
HIGH_RISK_THRESHOLD=0.8
MEDIUM_RISK_THRESHOLD=0.5
AMOUNT_THRESHOLD_HIGH=10000000  # 10M KES
```

### 3. Start Services

```bash
# Start Docker services
python setup.py --start-services

# Wait for services to be ready (about 2-3 minutes)
```

### 4. Initialize Database

```bash
# Activate Python environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Run database initialization
python risk_engine/main.py --once
```

### 5. Start Components

Open 3 terminal windows:

**Terminal 1 - Risk Engine:**
```bash
source venv/bin/activate
python risk_engine/main.py
```

**Terminal 2 - Dashboard:**
```bash
source venv/bin/activate
streamlit run dashboard/app.py
```

**Terminal 3 - Monitor Services:**
```bash
docker-compose -f infrastructure/docker-compose.yml logs -f
```

## Access Points

Once everything is running:

- **Unified Dashboard**: http://localhost:8501
- **CISO Assistant**: https://localhost:8443 (accept security warning)
- **Database**: localhost:5432 (use your DB credentials)

## Default Login Credentials

### CISO Assistant
- Create admin user on first access
- Follow the setup wizard

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check what's using the ports
   netstat -an | grep :5432
   netstat -an | grep :8443
   
   # Stop conflicting services or change ports in docker-compose.yml
   ```

2. **Database Connection Issues**
   ```bash
   # Check if PostgreSQL is running
   docker-compose -f infrastructure/docker-compose.yml ps
   
   # View database logs
   docker-compose -f infrastructure/docker-compose.yml logs postgres
   ```

3. **Python Dependencies**
   ```bash
   # Reinstall dependencies
   pip install -r risk_engine/requirements.txt --force-reinstall
   ```

### Service Status Check

```bash
# Check all services
docker-compose -f infrastructure/docker-compose.yml ps

# Expected output:
# ciso_assistant     Up      0.0.0.0:8000->8000/tcp
# ciso_frontend      Up      0.0.0.0:8443->3000/tcp  
# risk_postgres      Up      0.0.0.0:5432->5432/tcp
# risk_redis         Up      0.0.0.0:6379->6379/tcp
```

## Data Warehouse Integration

To connect to your existing data warehouse:

1. **Update Database Configuration**
   
   Edit `risk_engine/database.py` and modify the `fetch_pending_transactions()` method:

   ```python
   def fetch_pending_transactions(self, limit=None):
       # Replace with your actual data warehouse query
       query = """
       SELECT 
           transaction_id, customer_id, amount, currency,
           merchant_name, transaction_type, location, 
           channel, timestamp
       FROM your_warehouse.transactions 
       WHERE processed_flag = 0
       ORDER BY timestamp DESC
       """
       # ... rest of the method
   ```

2. **Configure Connection**
   
   Add your data warehouse credentials to `.env`:
   
   ```bash
   # Data Warehouse Configuration
   DW_HOST=your-warehouse-host
   DW_PORT=1433
   DW_DATABASE=your_warehouse_db
   DW_USER=warehouse_user
   DW_PASSWORD=warehouse_password
   ```

## Performance Tuning

### For High Volume (>1000 TPS)

1. **Increase Batch Size**
   ```bash
   # In .env file
   BATCH_SIZE=500
   POLLING_INTERVAL_SECONDS=10
   ```

2. **Database Optimization**
   ```sql
   -- Add indexes for performance
   CREATE INDEX idx_transactions_timestamp ON transaction_history(timestamp);
   CREATE INDEX idx_transactions_status ON transaction_history(status);
   CREATE INDEX idx_transactions_amount ON transaction_history(amount);
   ```

3. **Scale Services**
   ```yaml
   # In docker-compose.yml, add resource limits
   services:
     postgres:
       deploy:
         resources:
           limits:
             memory: 2G
             cpus: '1.0'
   ```

## Security Configuration

### Production Deployment

1. **Change Default Passwords**
   ```bash
   # Generate secure passwords
   openssl rand -base64 32
   ```

2. **Enable SSL/TLS**
   - Configure SSL certificates for CISO Assistant
   - Use HTTPS for all web interfaces
   - Enable database SSL connections

3. **Network Security**
   ```yaml
   # In docker-compose.yml, restrict network access
   networks:
     risk_network:
       driver: bridge
       internal: true  # Prevent external access
   ```

## Backup and Recovery

### Database Backup
```bash
# Create backup
docker exec risk_postgres pg_dump -U risk_user risk_management > backup.sql

# Restore backup
docker exec -i risk_postgres psql -U risk_user risk_management < backup.sql
```

### Configuration Backup
```bash
# Backup configuration
tar -czf config_backup.tar.gz risk_engine/.env infrastructure/docker-compose.yml
```

## Monitoring and Logs

### Log Locations
- Risk Engine: `risk_engine.log`
- Docker Services: `docker-compose logs`
- Dashboard: Streamlit console output

### Health Checks
```bash
# Check service health
curl http://localhost:8000/health  # CISO Assistant
curl http://localhost:8501/health  # Dashboard (if health endpoint added)
```

## Next Steps

After successful installation:

1. **Configure Risk Models** - Adjust thresholds in `risk_engine/risk_models.py`
2. **Set Up Alerts** - Configure email/SMS notifications
3. **Train Models** - Let the system run for a few days to collect training data
4. **Create Users** - Set up analyst and manager accounts
5. **Customize Dashboards** - Modify `dashboard/app.py` for your specific needs

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review logs for error messages
3. Consult the component documentation:
   - [CISO Assistant Docs](https://intuitem.gitbook.io/ciso-assistant/)
   - [Ballerine Docs](https://docs.ballerine.com/)
   - [Streamlit Docs](https://docs.streamlit.io/)