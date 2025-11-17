# Deployment Guide - Predictive Transaction Intelligence

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Running the Pipeline](#running-the-pipeline)
4. [API Deployment](#api-deployment)
5. [Testing](#testing)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **OS**: Windows 10/11, Linux, or macOS
- **Python**: 3.8 or higher
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: 5GB free space
- **CPU**: Multi-core processor recommended

### Software Dependencies
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

## Installation

### Step 1: Clone or Navigate to Project Directory
```bash
cd c:\Users\megha\FRAUD_DETECTION
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: If you encounter issues with PyTorch or transformers, install them separately:
```bash
# For CPU-only (lighter)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# For GPU support (if available)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Step 4: Verify Installation
```bash
python -c "import pandas, sklearn, xgboost, lightgbm, fastapi; print('All packages installed successfully!')"
```

## Running the Pipeline

### Option 1: Run Complete Pipeline
Execute all modules sequentially:
```bash
python run_all.py
```

This will:
1. Preprocess the data
2. Train predictive models
3. Train fraud detection models
4. Generate exploratory analysis

### Option 2: Run Individual Modules

#### Module 1: Data Preprocessing
```bash
python src/module1_preprocessing/preprocess_data.py
```

**Output**:
- Processed data files in `data/processed/`
- Feature engineer artifact in `models/preprocessing/`
- Training, validation, and test sets

#### Module 2: Predictive Transaction Modeling
```bash
python src/module2_predictive/train_model.py
```

**Output**:
- Trained models in `models/predictive/`
- Model performance metrics
- Feature importance analysis

#### Module 3: Fraud Detection Engine
```bash
python src/module3_fraud_detection/train_fraud_detector.py
```

**Output**:
- Fraud detection model in `models/fraud_detection/`
- Anomaly detector
- Risk rules configuration

#### Exploratory Data Analysis
```bash
python notebooks/01_exploratory_analysis.py
```

**Output**:
- Visualizations in `notebooks/figures/`
- Statistical analysis reports

## API Deployment

### Local Development Server

#### Start the API Server
```bash
python src/module4_deployment/api_server.py
```

The API will be available at: `http://localhost:8000`

#### Access API Documentation
Open your browser and navigate to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### 1. Health Check
```bash
GET http://localhost:8000/health
```

#### 2. Detect Fraud (Single Transaction)
```bash
POST http://localhost:8000/detect/fraud
Content-Type: application/json

{
  "Transaction_Amount": 50000,
  "Transaction_Date": "2024-01-15",
  "Transaction_Time": "14:30:00",
  "Transaction_Location": "Mumbai",
  "Card_Type": "Visa",
  "Transaction_Currency": "INR",
  "Transaction_Status": "Completed",
  "Previous_Transaction_Count": 25,
  "Distance_Between_Transactions_km": 10.5,
  "Time_Since_Last_Transaction_min": 120,
  "Authentication_Method": "PIN",
  "Transaction_Velocity": 3,
  "Transaction_Category": "Shopping"
}
```

#### 3. Batch Fraud Detection
```bash
POST http://localhost:8000/detect/batch
Content-Type: application/json

{
  "transactions": [
    { /* transaction 1 */ },
    { /* transaction 2 */ }
  ]
}
```

#### 4. Get Metrics
```bash
GET http://localhost:8000/metrics
```

### Production Deployment

#### Using Uvicorn with Multiple Workers
```bash
uvicorn src.module4_deployment.api_server:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Using Gunicorn (Linux/Mac)
```bash
gunicorn src.module4_deployment.api_server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Docker Deployment (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.module4_deployment.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t fraud-detection-api .
docker run -p 8000:8000 fraud-detection-api
```

## Testing

### Run Unit Tests
```bash
pytest tests/ -v
```

### Test API Endpoints
```bash
# Make sure API server is running first
python src/module4_deployment/test_api.py
```

### Manual Testing with cURL

#### Test Health Endpoint
```bash
curl http://localhost:8000/health
```

#### Test Fraud Detection
```bash
curl -X POST http://localhost:8000/detect/fraud \
  -H "Content-Type: application/json" \
  -d '{
    "Transaction_Amount": 50000,
    "Transaction_Date": "2024-01-15",
    "Transaction_Time": "14:30:00",
    "Transaction_Location": "Mumbai",
    "Card_Type": "Visa",
    "Transaction_Currency": "INR",
    "Transaction_Status": "Completed",
    "Previous_Transaction_Count": 25,
    "Distance_Between_Transactions_km": 10.5,
    "Time_Since_Last_Transaction_min": 120,
    "Authentication_Method": "PIN",
    "Transaction_Velocity": 3,
    "Transaction_Category": "Shopping"
  }'
```

## Monitoring

### Application Logs
Logs are stored in the `logs/` directory. Monitor them using:
```bash
# Windows
type logs\app.log

# Linux/Mac
tail -f logs/app.log
```

### Performance Metrics
Access real-time metrics at:
```
GET http://localhost:8000/metrics
```

Metrics include:
- Total requests processed
- Fraud detection rate
- Average processing time
- System uptime

### Model Performance Monitoring
Track model performance over time:
- Monitor precision, recall, F1 score
- Track false positive/negative rates
- Analyze risk score distributions

## Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: `ModuleNotFoundError`

**Solution**:
```bash
# Ensure you're in the project root directory
cd c:\Users\megha\FRAUD_DETECTION

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Data File Not Found
**Problem**: `FileNotFoundError: card_fraud.csv_processed.csv`

**Solution**:
- Ensure the data file is in the project root directory
- Check file path in `config/config.py`

#### 3. Model Loading Errors
**Problem**: Model files not found

**Solution**:
```bash
# Run preprocessing and training first
python src/module1_preprocessing/preprocess_data.py
python src/module2_predictive/train_model.py
python src/module3_fraud_detection/train_fraud_detector.py
```

#### 4. API Server Won't Start
**Problem**: Port already in use

**Solution**:
```bash
# Change port in config/config.py or use different port
uvicorn src.module4_deployment.api_server:app --port 8001
```

#### 5. Memory Issues
**Problem**: Out of memory errors

**Solution**:
- Reduce batch size in config
- Process data in smaller chunks
- Use lighter models (e.g., LightGBM instead of XGBoost)

#### 6. Slow Training
**Problem**: Training takes too long

**Solution**:
- Reduce number of estimators
- Use smaller dataset for testing
- Enable GPU support if available

### Getting Help

For issues not covered here:
1. Check the logs in `logs/` directory
2. Review error messages carefully
3. Ensure all dependencies are correctly installed
4. Verify data file integrity

## Performance Optimization

### 1. Model Optimization
- Use model quantization for faster inference
- Implement model caching
- Use ensemble pruning

### 2. API Optimization
- Enable response caching
- Use connection pooling
- Implement rate limiting

### 3. Data Processing
- Use parallel processing
- Implement data streaming
- Cache preprocessed features

## Security Considerations

### 1. API Security
- Implement authentication (JWT tokens)
- Use HTTPS in production
- Add rate limiting
- Validate all inputs

### 2. Data Security
- Encrypt sensitive data
- Implement access controls
- Regular security audits
- Secure model artifacts

## Maintenance

### Regular Tasks
1. **Daily**: Monitor API metrics and logs
2. **Weekly**: Review fraud detection accuracy
3. **Monthly**: Retrain models with new data
4. **Quarterly**: Full system audit

### Model Retraining
```bash
# Retrain with new data
python src/module2_predictive/train_model.py
python src/module3_fraud_detection/train_fraud_detector.py

# Restart API server to load new models
```

## Support

For technical support or questions:
- Review documentation in `README.md`
- Check code comments for detailed explanations
- Refer to module-specific documentation

---

**Last Updated**: 2024
**Version**: 1.0.0
