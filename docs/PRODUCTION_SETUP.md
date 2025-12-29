# Production Setup Guide
## Wekeza Bank Risk Management System

This guide will help you deploy the complete production-ready risk management system with Docker, PostgreSQL, and integrated open-source tools.

## 🏗️ Architecture Overview

The production system consists of:

### Core Services
- **PostgreSQL Database** - Primary data storage
- **Redis** - Caching and session management  
- **Risk Engine** - Custom Python risk processing
- **Streamlit Dashboard** - Risk management interface

### Integrated Open Source Tools
- **Ballerine** - Transaction monitoring and case management
- **CISO Assistant** - Enterprise risk register and GRC
- **Tazama** - Real-time fraud detection
- **NATS** - Message broker for real-time processing

## 📋 Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows with WSL2
- **RAM**: Minimum 8GB, Recommended 16GB
- **Storage**: Minimum 20GB free space
- **CPU**: 4+ cores recommended

### Software Requirements
- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Git** for version control
- **Python** 3.11+ (for local development)

## 🚀 Quick Start

### 1. Install Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# macOS (using Homebrew)
brew install --cask docker

# Windows
# Download Docker Desktop from https://docker.com
```

### 2. Clone and Setup
```bash
git clone https://github.com/eodenyire/WekezaBank.git
cd WekezaBank
```

### 3. Configure Environment
```bash
# Copy and customize production environment
cp .env.production .env.production.local
nano .env.production.local  # Edit with your settings
```

### 4. Start Production System
```bash
python start_production.py
```

## 🔧 Manual Setup (Alternative)

If you prefer manual control:

### 1. Build and Start Services
```bash
cd infrastructure
cp ../.env.production .env
docker-compose build
docker-compose up -d
```

### 2. Verify Services
```bash
docker-compose ps
docker-compose logs -f
```

### 3. Initialize Data
```bash
# The system will auto-initialize with sample data
# To add more data:
python ../test_data/generate_sample_data.py --count 10000
```

## 🌐 Service Access

Once started, access these URLs:

| Service | URL | Purpose |
|---------|-----|---------|
| **Risk Dashboard** | http://localhost:8501 | Main risk management interface |
| **Ballerine** | http://localhost:5173 | Transaction monitoring & cases |
| **CISO Assistant** | http://localhost:8443 | Risk register & compliance |
| **Tazama** | http://localhost:4000 | Fraud detection dashboard |

### Database Access
- **Host**: localhost:5432
- **Database**: risk_management
- **Username**: risk_user
- **Password**: risk_password

## 🔐 Security Configuration

### Production Security Checklist

1. **Change Default Passwords**
   ```bash
   # Edit .env.production
   DB_PASSWORD=your-secure-password
   JWT_SECRET_KEY=your-jwt-secret
   DJANGO_SECRET_KEY=your-django-secret
   ```

2. **Enable SSL/TLS**
   - Configure reverse proxy (nginx/traefik)
   - Use Let's Encrypt certificates
   - Update CORS settings

3. **Network Security**
   - Use Docker networks
   - Restrict port exposure
   - Configure firewall rules

4. **Database Security**
   - Enable PostgreSQL SSL
   - Use connection pooling
   - Regular backups

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# Check all services
docker-compose ps

# View logs
docker-compose logs -f risk-engine
docker-compose logs -f dashboard

# Check resource usage
docker stats
```

### Backup Strategy
```bash
# Database backup
docker-compose exec postgres pg_dump -U risk_user risk_management > backup.sql

# Full system backup
docker-compose down
tar -czf system-backup.tar.gz .
```

### Updates
```bash
# Pull latest images
docker-compose pull

# Rebuild custom services
docker-compose build --no-cache

# Restart with new images
docker-compose up -d
```

## 🔧 Troubleshooting

### Common Issues

**Services won't start**
```bash
# Check Docker daemon
sudo systemctl status docker

# Check logs
docker-compose logs

# Reset everything
docker-compose down -v
docker system prune -a
```

**Database connection errors**
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Verify database exists
docker-compose exec postgres psql -U risk_user -l
```

**Memory issues**
```bash
# Increase Docker memory limit
# Docker Desktop: Settings > Resources > Memory

# Check container memory usage
docker stats
```

### Performance Tuning

**PostgreSQL Optimization**
```sql
-- Add to postgresql.conf
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
```

**Application Scaling**
```yaml
# In docker-compose.yml
services:
  risk-engine:
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

## 🔄 Integration Configuration

### Ballerine Setup
1. Access http://localhost:5173
2. Configure API endpoints in admin panel
3. Set up case management workflows
4. Connect to risk engine via webhooks

### CISO Assistant Setup
1. Access http://localhost:8443
2. Create admin user account
3. Import risk frameworks (ISO 27001, NIST)
4. Configure risk assessment templates

### Tazama Setup
1. Access http://localhost:4000
2. Configure transaction rules
3. Set up alert thresholds
4. Connect to NATS message broker

## 📈 Scaling for Production

### Horizontal Scaling
```yaml
# docker-compose.override.yml
services:
  risk-engine:
    deploy:
      replicas: 3
  
  dashboard:
    deploy:
      replicas: 2
```

### Load Balancing
```yaml
# Add nginx reverse proxy
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
```

### Database Clustering
```yaml
# PostgreSQL with read replicas
postgres-primary:
  image: postgres:15-alpine
  environment:
    POSTGRES_REPLICATION_MODE: master

postgres-replica:
  image: postgres:15-alpine
  environment:
    POSTGRES_REPLICATION_MODE: slave
    POSTGRES_MASTER_SERVICE: postgres-primary
```

## 📞 Support

For issues and questions:
- **GitHub Issues**: https://github.com/eodenyire/WekezaBank/issues
- **Documentation**: Check `/docs` folder
- **Logs**: Always check `docker-compose logs` first

## 🎯 Next Steps

After successful deployment:
1. **Load test data**: `python test_data/generate_sample_data.py --count 50000`
2. **Configure integrations**: Set up API keys and webhooks
3. **Customize dashboards**: Modify Streamlit pages for your needs
4. **Set up monitoring**: Add Prometheus/Grafana for metrics
5. **Configure alerts**: Set up email/Slack notifications

---

**🏦 Wekeza Bank Risk Management System - Production Ready**