# System Architecture

## Overview

The Equity Bank Risk Management System is built using a microservices architecture with the following key components:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Data Warehouse (Equity Bank)                 │
│                     (Existing Transaction Data)                 │
└─────────────────────┬───────────────────────────────────────────┘
                      │ SQL Queries
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Python Risk Engine                         │
│  ┌─────────────────┬─────────────────┬─────────────────────────┐ │
│  │  Risk Models    │   Integrations  │    Database Manager     │ │
│  │  - Credit Risk  │   - Ballerine   │    - PostgreSQL         │ │
│  │  - Liquidity    │   - CISO Asst   │    - Case Management    │ │
│  │  - Market Risk  │   - Tazama      │    - Risk Metrics       │ │
│  │  - Anomaly Det  │                 │                         │ │
│  └─────────────────┴─────────────────┴─────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │ API Calls
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Service Layer                                │
│  ┌─────────────────┬─────────────────┬─────────────────────────┐ │
│  │   Ballerine     │ CISO Assistant  │      Tazama             │ │
│  │ (Case Mgmt)     │ (Risk Register) │  (Fraud Detection)      │ │
│  │ Port: 3000/5173 │ Port: 8000/8443 │   Port: 4001            │ │
│  └─────────────────┴─────────────────┴─────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │ Web Interface
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Unified Dashboard                               │
│                  (Streamlit)                                   │
│                 Port: 8501                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Data Layer

#### PostgreSQL Database
- **Purpose**: Central data store for all risk management data
- **Databases**:
  - `transactions_db`: Transaction data and analyst cases
  - `ciso_db`: Risk register and compliance data
  - `ballerine_db`: Case management workflows
- **Key Tables**:
  - `analyst_cases`: High/medium risk transactions for review
  - `risk_metrics`: Portfolio-level risk indicators
  - `transaction_history`: Simulated data warehouse

#### Data Warehouse Integration
- **Connection**: Direct SQL queries to existing Equity Bank systems
- **Frequency**: Real-time polling (configurable interval)
- **Data Flow**: Extract → Transform → Load into local PostgreSQL

### 2. Processing Layer

#### Python Risk Engine (`risk_engine/`)
The core intelligence of the system:

**Components:**
- `main.py`: Orchestration and scheduling
- `risk_models.py`: Risk scoring algorithms
- `database.py`: Data access layer
- `integrations.py`: External API connections
- `config.py`: Configuration management

**Risk Models:**
1. **Transaction Risk Scorer**
   - Amount-based risk (>10M KES = high risk)
   - Merchant risk (blacklist matching)
   - Location risk (geographic analysis)
   - Time-based risk (off-hours transactions)
   - Channel risk (online vs. mobile vs. ATM)

2. **Anomaly Detection**
   - Isolation Forest algorithm
   - Trained on historical transaction patterns
   - Detects unusual transaction behaviors

3. **Credit Risk Model**
   - Transaction velocity analysis
   - Large transaction frequency
   - Customer behavior patterns

4. **Liquidity Risk Model**
   - Liquidity Coverage Ratio (LCR) calculation
   - Asset liquidity assessment
   - Cash flow analysis

### 3. Service Layer

#### Ballerine (Case Management)
- **Purpose**: Analyst workflow management
- **Features**:
  - Case assignment and tracking
  - Workflow states (Assigned → In Progress → Closed)
  - Analyst feedback collection
  - Decision audit trail
- **Integration**: REST API for case creation and updates

#### CISO Assistant (Risk Register)
- **Purpose**: Enterprise risk management and GRC
- **Features**:
  - Risk register for different categories
  - Compliance framework mapping
  - Risk assessment workflows
  - Management reporting
- **Integration**: Django REST API

#### Tazama (Fraud Detection)
- **Purpose**: Real-time fraud detection
- **Features**:
  - ISO20022 compliant transaction processing
  - Rule-based fraud detection
  - Typology analysis
  - Real-time scoring
- **Integration**: HTTP API for transaction submission

### 4. Presentation Layer

#### Unified Dashboard (Streamlit)
- **Purpose**: Single pane of glass for all risk management activities
- **Pages**:
  - Dashboard Overview: Key metrics and trends
  - Analyst Workbench: Case review and actions
  - Risk Register: Enterprise risk management
  - Transaction Monitor: Real-time transaction flow
  - Deep Dive Analytics: Advanced analysis and reporting

## Data Flow

### 1. Transaction Processing Flow

```
Data Warehouse → Risk Engine → Risk Scoring → Routing Decision
                                    ↓
                            ┌───────┴───────┐
                            │               │
                        Low Risk        High/Medium Risk
                            │               │
                    Auto-Approve        Create Case
                            │               │
                    Update Status   → Ballerine → Analyst Review
                                        │
                                   Decision Made
                                        │
                                ┌───────┴───────┐
                                │               │
                            Approve         Block/Escalate
                                │               │
                        Close Case      Update Status
```

### 2. Risk Register Flow

```
Risk Engine → Portfolio Analysis → Risk Metrics → CISO Assistant
                    ↓
            Threshold Breach Detection
                    ↓
            Risk Event Creation
                    ↓
            Management Notification
```

## Security Architecture

### Authentication & Authorization
- **CISO Assistant**: Django-based user management
- **Ballerine**: JWT-based authentication
- **Dashboard**: Streamlit authentication (configurable)

### Network Security
- **Internal Network**: Docker bridge network for service communication
- **External Access**: Only web interfaces exposed
- **Database**: Internal access only, no external exposure

### Data Protection
- **Encryption**: TLS for all web traffic
- **Database**: Encrypted connections and at-rest encryption
- **Secrets**: Environment variables and Docker secrets

## Scalability Considerations

### Horizontal Scaling
- **Risk Engine**: Multiple instances with load balancing
- **Database**: Read replicas for analytics queries
- **Services**: Container orchestration (Kubernetes ready)

### Performance Optimization
- **Database Indexing**: Optimized for transaction queries
- **Caching**: Redis for frequently accessed data
- **Batch Processing**: Configurable batch sizes for high volume

### Monitoring & Observability
- **Logging**: Structured logging with correlation IDs
- **Metrics**: Prometheus-compatible metrics
- **Health Checks**: Service health endpoints
- **Alerting**: Integration with monitoring systems

## Integration Points

### External Systems
1. **Core Banking System**: Transaction data extraction
2. **Data Warehouse**: Historical data and analytics
3. **Email/SMS**: Alert notifications
4. **LDAP/AD**: User authentication
5. **SIEM**: Security event forwarding

### API Endpoints
- **Risk Engine**: Internal APIs for status and metrics
- **Ballerine**: Case management APIs
- **CISO Assistant**: Risk register APIs
- **Dashboard**: Data visualization APIs

## Deployment Architecture

### Development Environment
- **Single Machine**: Docker Compose deployment
- **Resource Requirements**: 8GB RAM, 4 CPU cores
- **Storage**: 50GB for databases and logs

### Production Environment
- **Multi-Node**: Kubernetes or Docker Swarm
- **High Availability**: Service redundancy
- **Load Balancing**: NGINX or cloud load balancer
- **Database**: Managed PostgreSQL service
- **Monitoring**: Prometheus + Grafana stack

## Configuration Management

### Environment Variables
- **Database**: Connection strings and credentials
- **Services**: API endpoints and authentication
- **Risk Models**: Thresholds and parameters
- **Monitoring**: Logging levels and destinations

### Feature Flags
- **Risk Models**: Enable/disable specific models
- **Integrations**: Toggle external service connections
- **UI Features**: Control dashboard functionality

## Disaster Recovery

### Backup Strategy
- **Database**: Automated daily backups
- **Configuration**: Version-controlled configs
- **Logs**: Centralized log aggregation

### Recovery Procedures
- **RTO**: 4 hours (Recovery Time Objective)
- **RPO**: 1 hour (Recovery Point Objective)
- **Failover**: Automated service failover
- **Data Recovery**: Point-in-time database recovery

## Future Enhancements

### Planned Features
1. **Machine Learning**: Advanced ML models for risk prediction
2. **Real-time Streaming**: Kafka-based event streaming
3. **Mobile App**: Mobile interface for analysts
4. **API Gateway**: Centralized API management
5. **Multi-tenancy**: Support for multiple business units

### Technology Roadmap
- **Cloud Migration**: AWS/Azure deployment
- **Microservices**: Further service decomposition
- **Event Sourcing**: Event-driven architecture
- **GraphQL**: Modern API layer
- **AI/ML**: Advanced analytics and predictions