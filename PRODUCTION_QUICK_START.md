# 🚀 Production Quick Start Guide
## Wekeza Bank Risk Management System

Get your production system running in 5 minutes!

## ⚡ Quick Commands

### 1. Start Everything
```bash
python start_production.py
```

### 2. Test Everything
```bash
python test_production.py
```

### 3. Stop Everything
```bash
cd infrastructure && docker-compose down
```

## 🌐 Access URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Risk Dashboard** | http://localhost:8501 | Main interface |
| **Ballerine** | http://localhost:5173 | Case management |
| **CISO Assistant** | http://localhost:8443 | Risk register |
| **Tazama** | http://localhost:4000 | Fraud detection |

## 🔧 Management Commands

### View Service Status
```bash
cd infrastructure && docker-compose ps
```

### View Logs
```bash
cd infrastructure && docker-compose logs -f [service_name]
```

### Restart Service
```bash
cd infrastructure && docker-compose restart [service_name]
```

### Scale Services
```bash
cd infrastructure && docker-compose up -d --scale risk-engine=3
```

## 📊 Key Features

### 🛡️ Risk Management
- **Real-time monitoring** of all transactions
- **ML-based risk scoring** with configurable thresholds
- **Automated case creation** for high-risk transactions
- **Analyst workbench** for case review and decision making

### 🔍 Fraud Detection
- **Tazama integration** for real-time fraud detection
- **Pattern recognition** for suspicious activities
- **Alert management** with severity levels
- **ISO20022 message format** support

### 📋 Compliance & GRC
- **CISO Assistant** for enterprise risk register
- **Risk framework** support (ISO 27001, NIST)
- **Audit trails** for all risk decisions
- **Regulatory reporting** capabilities

### 📈 Analytics & Reporting
- **Interactive dashboards** with Plotly visualizations
- **Portfolio risk metrics** and KPIs
- **Trend analysis** and historical reporting
- **Export capabilities** for further analysis

## 🔐 Security Features

- **PostgreSQL** with encrypted connections
- **Redis** for secure session management
- **API authentication** with JWT tokens
- **Role-based access control** (RBAC)
- **Audit logging** for all activities

## 📱 Integration Points

### APIs Available
- **Risk Engine API** - Submit transactions for scoring
- **Ballerine API** - Case management operations
- **CISO Assistant API** - Risk register management
- **Tazama API** - Fraud detection services

### Webhooks
- **Transaction alerts** - Real-time notifications
- **Case updates** - Status change notifications
- **Risk threshold breaches** - Automated alerts

## 🚨 Troubleshooting

### Services Won't Start
```bash
# Check Docker
docker --version
docker-compose --version

# Check logs
cd infrastructure && docker-compose logs
```

### Database Issues
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U risk_user -d risk_management

# Check database status
docker-compose exec postgres pg_isready
```

### Performance Issues
```bash
# Check resource usage
docker stats

# Scale services
docker-compose up -d --scale risk-engine=2
```

## 📞 Support

- **Documentation**: `/docs` folder
- **Logs**: `docker-compose logs [service]`
- **GitHub**: https://github.com/eodenyire/WekezaBank

## 🎯 Production Checklist

- [ ] Docker and Docker Compose installed
- [ ] Environment variables configured in `.env.production`
- [ ] Security keys changed from defaults
- [ ] Database backups configured
- [ ] Monitoring and alerting set up
- [ ] SSL certificates configured (for public deployment)
- [ ] Firewall rules configured
- [ ] Load balancer configured (for high availability)

---

**🏦 Ready for Production - Wekeza Bank Risk Management System**