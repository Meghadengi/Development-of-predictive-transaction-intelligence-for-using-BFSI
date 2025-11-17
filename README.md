# 🛡️ Predictive Transaction Intelligence for BFSI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Project Overview
An **AI-driven fraud detection system** utilizing Large Language Models (LLMs) and machine learning to analyze historical customer transaction patterns and behavioral data for predicting future transactions and assessing fraud risks in **real-time**.

### ✨ Key Features
- 🔮 **Predictive Modeling**: Anticipate customer transactions using behavioral and historical data
- ⚡ **Real-Time Risk Assessment**: Evaluate transaction legitimacy instantly (<100ms)
- 🚨 **Fraud Detection**: Identify anomalous or high-risk transactions through pattern learning
- 🛡️ **Enhanced Financial Security**: Strengthen anti-fraud systems for financial institutions
- 🚀 **Production-Ready API**: FastAPI-based REST API with auto-documentation
- 📊 **Comprehensive Analytics**: 40+ engineered features and ensemble models

## Project Structure
```
FRAUD_DETECTION/
├── data/                           # Data storage
│   ├── raw/                        # Raw transaction data
│   ├── processed/                  # Preprocessed data
│   └── features/                   # Feature engineered data
├── models/                         # Trained models
│   ├── predictive/                 # Transaction prediction models
│   └── fraud_detection/            # Fraud detection models
├── src/                            # Source code
│   ├── module1_preprocessing/      # Data preprocessing
│   ├── module2_predictive/         # Predictive modeling
│   ├── module3_fraud_detection/    # Fraud detection engine
│   └── module4_deployment/         # Deployment layer
├── notebooks/                      # Jupyter notebooks for analysis
├── tests/                          # Unit tests
├── config/                         # Configuration files
└── logs/                           # Application logs
```

## Modules

### Module 1: Data Collection and Preprocessing
- Data cleaning and normalization
- Feature engineering
- Transaction tagging (fraud/legitimate)

### Module 2: Predictive Transaction Modeling
- LLM fine-tuning for transaction forecasting
- Customer behavior pattern learning
- Model evaluation (precision, recall, F1)

### Module 3: Real-Time Fraud Detection Engine
- Risk scoring algorithm
- Anomaly detection
- Real-time alert generation

### Module 4: Deployment and Integration Layer
- REST API for model serving
- Integration with monitoring systems
- Performance testing and monitoring

## ✨ NEW: Premium UI with Authentication!

**SafeBank AI now includes TWO professional options:**

### 🔐 Option 1: With Secure Authentication (Recommended)
```bash
# Launch with login/signup system
run_with_auth.bat

# Or manually
streamlit run app_with_auth.py
```

**Features:**
- 🔐 Secure login/signup with SQLite database
- 👤 User profiles and session management
- 🔒 SHA-256 password hashing
- 📧 Email validation
- 🎨 Professional fintech design
- ✅ All fraud detection features after login

**Documentation:**
- **Quick Start**: See `AUTH_QUICK_START.md`
- **Full Guide**: See `AUTH_GUIDE.md`

### 🎨 Option 2: Premium UI (No Authentication)
```bash
# Launch the premium dashboard
run_premium_ui.bat

# Or manually
streamlit run app_premium.py
```

**Features:**
- 🎨 Fintech-inspired design (Navy blue, white, gold accents)
- 🏠 Single transaction analysis with real-time detection
- 📊 Batch processing with interactive visualizations
- 📈 Comprehensive analytics dashboard
- 🔧 System monitoring and performance metrics
- 📱 Fully responsive design

**Documentation:**
- **Quick Start**: See `LAUNCH_GUIDE.md`
- **Full Guide**: See `UI_GUIDE.md`
- **Features**: See `PREMIUM_UI_README.md`

---

## 🚀 Quick Start (5 Minutes)

### Installation
```bash
# Navigate to project directory
cd c:\Users\megha\FRAUD_DETECTION

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Run Complete Pipeline
```bash
# Option 1: Run everything at once
python run_all.py

# Option 2: Run individual modules
python src/module1_preprocessing/preprocess_data.py        # Module 1
python src/module2_predictive/train_model.py               # Module 2
python src/module3_fraud_detection/train_fraud_detector.py # Module 3
```

### Start API Server
```bash
python src/module4_deployment/api_server.py
```

### Test the API
```bash
# In another terminal
python src/module4_deployment/test_api.py

# Or visit: http://localhost:8000/docs
```

## API Endpoints

- `POST /predict/transaction` - Predict next transaction
- `POST /detect/fraud` - Detect fraud in real-time
- `GET /health` - Health check
- `GET /metrics` - Model performance metrics

## Dataset
- **Source**: Card transaction data
- **Size**: 100,000 transactions
- **Features**: 16 columns including transaction amount, location, time, velocity, etc.
- **Target**: isFraud (binary classification)
- **Balance**: 50% fraud, 50% legitimate

## 📊 Performance Metrics
- **Accuracy**: 85-95%
- **Precision**: 80-90%
- **Recall**: 80-90%
- **F1 Score**: 80-90%
- **AUC-ROC**: 90-95%
- **API Latency**: <100ms
- **Throughput**: 100+ requests/second

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICK_START.md](QUICK_START.md) | 5-minute quick start guide |
| [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) | Complete technical documentation |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Production deployment guide |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project summary and outcomes |

## 🛠️ Technology Stack

- **Python 3.8+**: Core language
- **Machine Learning**: XGBoost, LightGBM, Scikit-learn
- **Deep Learning**: PyTorch, Transformers (optional)
- **API**: FastAPI, Uvicorn
- **Data**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly

## 🎯 Project Status

✅ **All Modules Completed**
- ✅ Module 1: Data Preprocessing
- ✅ Module 2: Predictive Modeling
- ✅ Module 3: Fraud Detection Engine
- ✅ Module 4: API Deployment

🚀 **Production Ready**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - See LICENSE file for details

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Built with ❤️ for BFSI Fraud Detection**
