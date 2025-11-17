# 🛡️ Fraud Detection System - Deployment Guide

## 🚀 Deployment Options

Your fraud detection system can be deployed in two ways:

### Option 1: FastAPI (REST API) ⚡
**Best for:** Production, integration with other systems, programmatic access

### Option 2: Streamlit (Web Interface) 🖥️
**Best for:** Interactive use, demos, user-friendly interface

### Option 3: Both (Combined) 🔄
**Best for:** Development and testing

---

## 📦 Installation

First, install the additional dependencies:

```bash
# Install Streamlit and Plotly for the web interface
pip install streamlit plotly
```

---

## 🚀 Deployment Commands

### Option A: FastAPI Only (API Server)
```bash
# Start FastAPI server
python src/module4_deployment/api_server.py

# Or use the deployment script
python deploy.py --mode api --api-port 8000
```

**Access Points:**
- 📚 **API Documentation:** http://localhost:8000/docs
- 🔄 **Alternative Docs:** http://localhost:8000/redoc
- 🏥 **Health Check:** http://localhost:8000/health
- 📊 **Metrics:** http://localhost:8000/metrics

### Option B: Streamlit Only (Web Interface)
```bash
# Start Streamlit web app
venv/Scripts/activate
streamlit run app_premium.py
streamlit run streamlit_app.py

# Or use the deployment script
python deploy.py --mode web --web-port 8501
```

**Access Point:**
- 🖥️ **Web Interface:** http://localhost:8501

### Option C: Both Services (Recommended)
```bash
# Start both FastAPI and Streamlit
python deploy.py --mode both

# This will start:
# - FastAPI API server on port 8000
# - Streamlit web interface on port 8501
```

---

## 🎯 API Endpoints (FastAPI)

### 1. Single Transaction Fraud Detection
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

**Response:**
```json
{
  "is_fraud": false,
  "ml_risk_score": 0.23,
  "rule_risk_score": 0.15,
  "combined_risk_score": 0.19,
  "risk_level": "LOW",
  "triggered_rules": [],
  "recommendation": "APPROVE",
  "timestamp": "2024-01-15T14:30:00",
  "processing_time_ms": 45.2
}
```

### 2. Batch Processing
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

### 3. Health Check
```bash
GET http://localhost:8000/health
```

### 4. System Metrics
```bash
GET http://localhost:8000/metrics
```

---

## 🖥️ Web Interface Features (Streamlit)

### Single Transaction Detection
- ✅ **Interactive Form:** Fill in transaction details
- ✅ **Real-time Results:** Instant fraud detection with risk scores
- ✅ **Visual Feedback:** Color-coded results (Red=High, Yellow=Medium, Green=Low)
- ✅ **Detailed Analysis:** ML score, rule score, triggered rules

### Batch Processing
- ✅ **CSV Upload:** Upload transaction files for batch processing
- ✅ **Results Table:** View all detection results
- ✅ **Risk Distribution:** Pie chart showing risk levels
- ✅ **Export Options:** Download results

### Analytics Dashboard
- ✅ **System Metrics:** Total requests, fraud rate, processing times
- ✅ **Performance Monitoring:** API uptime and response times
- ✅ **Real-time Updates:** Live system statistics

### System Information
- ✅ **Model Status:** Check if all models are loaded
- ✅ **File Sizes:** Monitor model and data file sizes
- ✅ **Health Monitoring:** API connection status

---

## 🧪 Testing Your Deployment

### Test FastAPI
```bash
# Test API connection
python deploy.py --mode test

# Or manually test with curl
curl -X POST http://localhost:8000/detect/fraud \
  -H "Content-Type: application/json" \
  -d '{
    "Transaction_Amount": 95000000,
    "Transaction_Date": "2024-01-15",
    "Transaction_Time": "02:30:00",
    "Transaction_Location": "Unknown",
    "Card_Type": "Mastercard",
    "Transaction_Currency": "INR",
    "Transaction_Status": "Pending",
    "Previous_Transaction_Count": 2,
    "Distance_Between_Transactions_km": 800.0,
    "Time_Since_Last_Transaction_min": 1,
    "Authentication_Method": "Failed",
    "Transaction_Velocity": 15,
    "Transaction_Category": "Transfer"
  }'
```

### Test Streamlit
1. Open http://localhost:8501
2. Go to "Single Transaction" tab
3. Fill in a suspicious transaction (high amount, night time, etc.)
4. Click "Detect Fraud" button
5. Check the result and recommendation

---

## 📊 Expected Performance

### FastAPI
- **Latency:** <100ms per transaction
- **Throughput:** 100+ requests/second
- **Uptime:** 99.9%+

### Streamlit
- **Responsive UI:** Real-time updates
- **Interactive:** User-friendly interface
- **Visual:** Charts and graphs

---

## 🔧 Configuration

### Change Ports
```bash
# FastAPI on different port
python deploy.py --mode api --api-port 9000

# Streamlit on different port
python deploy.py --mode web --web-port 9001

# Both on different ports
python deploy.py --mode both --api-port 9000 --web-port 9001
```

### Custom Host
```bash
# Run on all interfaces (0.0.0.0)
python deploy.py --host 0.0.0.0
```

---

## 🚨 Troubleshooting

### Common Issues

**1. "Models not found" error**
```bash
# Solution: Run training first
python run_all.py
```

**2. Port already in use**
```bash
# Solution: Use different ports
python deploy.py --api-port 8001 --web-port 8502
```

**3. Streamlit won't open browser**
```bash
# Solution: Manual access
# Open http://localhost:8501 in your browser
```

**4. API connection refused**
```bash
# Solution: Check if FastAPI is running
python deploy.py --mode test
```

---

## 🎯 Production Deployment

### Option 1: FastAPI Production
```bash
# Using Uvicorn (recommended for production)
uvicorn src.module4_deployment.api_server:app --host 0.0.0.0 --port 8000 --workers 4

# Using Gunicorn
gunicorn src.module4_deployment.api_server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Option 2: Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8501

CMD ["python", "deploy.py", "--mode", "both"]
```

```bash
# Build and run
docker build -t fraud-detection .
docker run -p 8000:8000 -p 8501:8501 fraud-detection
```

### Option 3: Cloud Deployment
- **AWS:** ECS, Lambda, API Gateway
- **Azure:** App Service, Functions
- **GCP:** Cloud Run, App Engine

---

## 📈 Monitoring

### API Metrics
Visit http://localhost:8000/metrics to see:
- Total requests processed
- Fraud detection rate
- Average processing time
- System uptime

### Logs
- **API Logs:** Check console output
- **Application Logs:** Check `logs/` directory

---

## 🔄 Restarting Services

```bash
# Stop all services (Ctrl+C)

# Restart FastAPI only
python deploy.py --mode api

# Restart Streamlit only
python deploy.py --mode web

# Restart both
python deploy.py --mode both
```

---

## 🎉 Success!

Your fraud detection system is now deployed and ready to use!

### What's Running:
- ✅ **FastAPI:** REST API with fraud detection endpoints
- ✅ **Streamlit:** User-friendly web interface
- ✅ **Models:** All trained models loaded and ready
- ✅ **Monitoring:** Real-time metrics and health checks

### Ready for:
- 🛡️ Real-time fraud detection
- 📊 Batch processing
- 📈 Analytics and monitoring
- 🔧 System management

---

**🎯 Next Steps:**
1. Visit http://localhost:8501 for the web interface
2. Visit http://localhost:8000/docs for API documentation
3. Test with sample transactions
4. Customize for your specific needs

**Happy Fraud Detection! 🛡️🚀**
