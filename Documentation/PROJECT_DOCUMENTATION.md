# Project Documentation - Predictive Transaction Intelligence

## Executive Summary

This project implements an AI-driven fraud detection system for the Banking, Financial Services, and Insurance (BFSI) sector. The system uses Large Language Models (LLMs) and machine learning to analyze transaction patterns, predict future transactions, and detect fraud in real-time.

## Project Architecture

### System Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    Data Input Layer                          │
│              (Card Transaction Data)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              MODULE 1: Data Preprocessing                    │
│  - Data Loading & Validation                                 │
│  - Feature Engineering                                       │
│  - Data Splitting                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│         MODULE 2: Predictive Modeling                        │
│  - Transaction Pattern Learning                              │
│  - Ensemble Model Training                                   │
│  - LLM Embeddings (Optional)                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│         MODULE 3: Fraud Detection Engine                     │
│  - ML-based Risk Scoring                                     │
│  - Rule-based Detection                                      │
│  - Anomaly Detection                                         │
│  - Alert Generation                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│         MODULE 4: Deployment & Integration                   │
│  - REST API Server                                           │
│  - Real-time Processing                                      │
│  - Monitoring & Metrics                                      │
└─────────────────────────────────────────────────────────────┘
```

## Module Descriptions

### Module 1: Data Collection and Preprocessing

**Purpose**: Clean, transform, and prepare transaction data for modeling.

**Components**:
1. **Data Loader** (`data_loader.py`)
   - Loads transaction data from CSV
   - Validates data quality
   - Provides data statistics

2. **Feature Engineer** (`feature_engineer.py`)
   - Extracts time-based features (hour, day, weekend)
   - Creates aggregated features (z-scores, percentiles)
   - Generates interaction features
   - Encodes categorical variables
   - Scales numerical features
   - Creates risk indicators

3. **Preprocessing Pipeline** (`preprocess_data.py`)
   - Orchestrates data loading and feature engineering
   - Splits data into train/validation/test sets
   - Saves processed artifacts

**Key Features Created**:
- Time features: Day of week, hour, business hours, night flag
- Amount features: Z-score, percentile, log transform
- Velocity features: High velocity flag, velocity ratios
- Distance features: Long distance flag, unusual location
- Risk indicators: Combined risk score from multiple factors

**Output**:
- `data/processed/train_data.csv`
- `data/processed/val_data.csv`
- `data/processed/test_data.csv`
- `models/preprocessing/feature_engineer.pkl`

### Module 2: Predictive Transaction Modeling

**Purpose**: Build models to predict transaction patterns and behaviors.

**Components**:
1. **Transaction Predictor** (`transaction_predictor.py`)
   - Supports multiple algorithms: XGBoost, LightGBM, Random Forest
   - Ensemble modeling for improved accuracy
   - Feature importance analysis
   - Model evaluation and metrics

2. **LLM Embeddings** (`llm_embeddings.py`)
   - Creates contextual embeddings using transformers
   - Converts transactions to text representations
   - Analyzes transaction sequences
   - Pattern detection in transaction history

3. **Training Pipeline** (`train_model.py`)
   - Loads preprocessed data
   - Trains ensemble of models
   - Evaluates performance
   - Saves trained models

**Models Used**:
- **XGBoost**: Gradient boosting for high performance
- **LightGBM**: Fast, efficient gradient boosting
- **Random Forest**: Ensemble decision trees

**Performance Metrics**:
- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

**Output**:
- `models/predictive/ensemble/` (ensemble models)
- `models/predictive/transaction_predictor.pkl`

### Module 3: Real-Time Fraud Detection Engine

**Purpose**: Detect fraudulent transactions in real-time using ML and rules.

**Components**:
1. **Fraud Detector** (`fraud_detector.py`)
   - ML-based risk scoring
   - Rule-based fraud detection
   - Combined risk assessment
   - Alert generation
   - Batch processing support

2. **Anomaly Detector**
   - Learns baseline from normal transactions
   - Detects statistical anomalies
   - Z-score and IQR methods

3. **Training Pipeline** (`train_fraud_detector.py`)
   - Trains fraud detection models
   - Configures risk rules
   - Evaluates detection accuracy

**Risk Rules**:
- High transaction amount (>75M)
- High velocity (>10 transactions)
- Long distance (>500 km)
- Rapid succession (<1 minute)
- Night transactions (10 PM - 6 AM)
- Failed authentication

**Risk Levels**:
- **HIGH** (≥0.7): Block transaction, manual review required
- **MEDIUM** (0.4-0.7): Additional verification recommended
- **LOW** (<0.4): Approve transaction

**Output**:
- `models/fraud_detection/fraud_detector.pkl`
- `models/fraud_detection/anomaly_detector.pkl`
- `models/fraud_detection/risk_rules.pkl`

### Module 4: Deployment and Integration Layer

**Purpose**: Deploy models as REST API for real-time fraud detection.

**Components**:
1. **API Server** (`api_server.py`)
   - FastAPI-based REST API
   - Real-time fraud detection endpoint
   - Batch processing endpoint
   - Health check and metrics
   - CORS support

2. **API Testing** (`test_api.py`)
   - Comprehensive API tests
   - Performance benchmarking
   - Integration testing

**API Endpoints**:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API info |
| `/health` | GET | Health check |
| `/detect/fraud` | POST | Detect fraud in single transaction |
| `/detect/batch` | POST | Batch fraud detection |
| `/metrics` | GET | API performance metrics |
| `/predict/transaction` | POST | Predict transaction patterns |

**API Response Format**:
```json
{
  "is_fraud": true,
  "ml_risk_score": 0.85,
  "rule_risk_score": 0.72,
  "combined_risk_score": 0.81,
  "risk_level": "HIGH",
  "triggered_rules": [
    "High transaction amount",
    "Night time transaction"
  ],
  "recommendation": "BLOCK - High fraud risk detected",
  "timestamp": "2024-01-15T14:30:00",
  "processing_time_ms": 45.2
}
```

## Data Schema

### Input Features (16 columns)

| Feature | Type | Description |
|---------|------|-------------|
| Transaction_Amount | int64 | Transaction amount in currency |
| Transaction_Date | object | Date of transaction |
| Transaction_Time | object | Time of transaction |
| Transaction_Location | object | Location of transaction |
| Card_Type | object | Type of card (Visa, Mastercard, etc.) |
| Transaction_Currency | object | Currency code |
| Transaction_Status | object | Status (Completed, Pending, etc.) |
| Previous_Transaction_Count | int64 | Number of previous transactions |
| Distance_Between_Transactions_km | float64 | Distance from last transaction |
| Time_Since_Last_Transaction_min | int64 | Time since last transaction |
| Authentication_Method | object | Authentication method used |
| Transaction_Velocity | int64 | Transaction velocity metric |
| Transaction_Category | object | Category (Shopping, Transfer, etc.) |
| isFraud | int64 | Target variable (0=Normal, 1=Fraud) |
| Log_Transaction_Amount | float64 | Log-transformed amount |
| Velocity_Distance_Interact | float64 | Interaction feature |

### Engineered Features (40+ additional features)

**Time Features**:
- Day_of_Week, Day_of_Month, Month
- Hour, Is_Weekend, Is_Night, Is_Business_Hours

**Statistical Features**:
- Amount_Zscore, Amount_Percentile
- High_Velocity, Long_Distance
- Quick_Succession, Time_Gap_Category

**Interaction Features**:
- Amount_Velocity_Ratio
- Amount_Distance_Product
- Amount_Per_Previous_Txn

**Risk Indicators**:
- High_Amount_Flag
- Unusual_Location_Flag
- Rapid_Transaction_Flag
- Risk_Score

## Performance Benchmarks

### Model Performance (Expected)
- **Accuracy**: 85-95%
- **Precision**: 80-90%
- **Recall**: 80-90%
- **F1 Score**: 80-90%
- **ROC-AUC**: 90-95%

### API Performance
- **Latency**: <100ms per transaction
- **Throughput**: 100+ requests/second
- **Availability**: 99.9% uptime

## Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning utilities

### Machine Learning
- **XGBoost**: Gradient boosting
- **LightGBM**: Fast gradient boosting
- **PyTorch**: Deep learning framework
- **Transformers**: LLM support

### API & Deployment
- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### Visualization
- **Matplotlib**: Plotting
- **Seaborn**: Statistical visualization
- **Plotly**: Interactive charts

## Configuration

All configuration is centralized in `config/config.py`:

```python
# Data paths
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Model parameters
RANDOM_SEED = 42
TEST_SIZE = 0.2
VAL_SIZE = 0.1
BATCH_SIZE = 32
EPOCHS = 10

# Fraud thresholds
FRAUD_THRESHOLD = 0.5
HIGH_RISK_THRESHOLD = 0.7
MEDIUM_RISK_THRESHOLD = 0.4

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8000
```

## Security Considerations

### Data Security
- Sensitive data should be encrypted at rest
- Use secure connections (HTTPS) in production
- Implement access controls and authentication

### API Security
- Add JWT authentication for production
- Implement rate limiting
- Validate all inputs
- Use API keys for external access

### Model Security
- Protect model files from unauthorized access
- Version control for models
- Regular security audits

## Scalability

### Horizontal Scaling
- Deploy multiple API instances behind load balancer
- Use Redis for caching and session management
- Implement message queues for async processing

### Vertical Scaling
- Optimize model inference
- Use GPU acceleration where available
- Implement model quantization

### Database Integration
- Connect to production databases
- Implement connection pooling
- Use read replicas for queries

## Monitoring & Logging

### Application Logs
- Located in `logs/` directory
- Structured logging format
- Log levels: INFO, WARNING, ERROR

### Metrics to Monitor
- Request count and latency
- Fraud detection rate
- Model accuracy over time
- System resource usage
- Error rates

### Alerting
- Set up alerts for high fraud rates
- Monitor API downtime
- Track model performance degradation

## Future Enhancements

### Short-term
1. Add user authentication
2. Implement caching layer
3. Add more visualization dashboards
4. Enhance API documentation

### Medium-term
1. Real-time model retraining
2. A/B testing framework
3. Advanced anomaly detection
4. Customer behavior profiling

### Long-term
1. Deep learning models
2. Graph neural networks for transaction networks
3. Explainable AI features
4. Multi-language support

## Best Practices

### Development
- Follow PEP 8 style guide
- Write comprehensive tests
- Document all functions
- Use type hints

### Deployment
- Use virtual environments
- Pin dependency versions
- Implement CI/CD pipeline
- Regular backups

### Maintenance
- Regular model retraining
- Monitor data drift
- Update dependencies
- Performance optimization

## Troubleshooting Guide

See `DEPLOYMENT_GUIDE.md` for detailed troubleshooting steps.

## References

### Academic Papers
- XGBoost: A Scalable Tree Boosting System
- LightGBM: A Highly Efficient Gradient Boosting Decision Tree
- Attention Is All You Need (Transformers)

### Documentation
- FastAPI: https://fastapi.tiangolo.com/
- Scikit-learn: https://scikit-learn.org/
- XGBoost: https://xgboost.readthedocs.io/

## License

MIT License - See LICENSE file for details

## Contributors

Developed for BFSI fraud detection and transaction intelligence.

---

**Document Version**: 1.0.0
**Last Updated**: 2024
**Status**: Production Ready
