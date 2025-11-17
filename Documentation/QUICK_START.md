# Quick Start Guide

Get your fraud detection system up and running in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies (2 minutes)
```bash
# Navigate to project directory
cd c:\Users\megha\FRAUD_DETECTION

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Run Complete Pipeline (3 minutes)
```bash
python run_all.py
```

This will:
- ✅ Preprocess data and engineer features
- ✅ Train predictive models
- ✅ Train fraud detection engine
- ✅ Generate analysis and visualizations

### 3. Start API Server
```bash
python src/module4_deployment/api_server.py
```

### 4. Test the API
Open another terminal and run:
```bash
python src/module4_deployment/test_api.py
```

## 📊 View Results

### API Documentation
Open in browser: http://localhost:8000/docs

### Visualizations
Check: `notebooks/figures/` directory

### Models
Saved in: `models/` directory

## 🎯 Quick Test

### Test Fraud Detection via API

**Normal Transaction:**
```bash
curl -X POST http://localhost:8000/detect/fraud -H "Content-Type: application/json" -d "{\"Transaction_Amount\": 25000, \"Transaction_Date\": \"2024-01-15\", \"Transaction_Time\": \"14:30:00\", \"Transaction_Location\": \"Mumbai\", \"Card_Type\": \"Visa\", \"Transaction_Currency\": \"INR\", \"Transaction_Status\": \"Completed\", \"Previous_Transaction_Count\": 25, \"Distance_Between_Transactions_km\": 5.0, \"Time_Since_Last_Transaction_min\": 120, \"Authentication_Method\": \"PIN\", \"Transaction_Velocity\": 2, \"Transaction_Category\": \"Shopping\"}"
```

**Suspicious Transaction:**
```bash
curl -X POST http://localhost:8000/detect/fraud -H "Content-Type: application/json" -d "{\"Transaction_Amount\": 95000000, \"Transaction_Date\": \"2024-01-15\", \"Transaction_Time\": \"02:30:00\", \"Transaction_Location\": \"Unknown\", \"Card_Type\": \"Mastercard\", \"Transaction_Currency\": \"USD\", \"Transaction_Status\": \"Pending\", \"Previous_Transaction_Count\": 2, \"Distance_Between_Transactions_km\": 800.0, \"Time_Since_Last_Transaction_min\": 1, \"Authentication_Method\": \"Failed\", \"Transaction_Velocity\": 15, \"Transaction_Category\": \"Transfer\"}"
```

## 📁 Project Structure
```
FRAUD_DETECTION/
├── src/
│   ├── module1_preprocessing/     # Data preprocessing
│   ├── module2_predictive/        # Predictive modeling
│   ├── module3_fraud_detection/   # Fraud detection
│   └── module4_deployment/        # API deployment
├── models/                        # Trained models
├── data/                          # Data files
├── notebooks/                     # Analysis notebooks
├── config/                        # Configuration
├── tests/                         # Unit tests
└── logs/                          # Application logs
```

## 🔧 Individual Module Execution

### Run Only Preprocessing
```bash
python src/module1_preprocessing/preprocess_data.py
```

### Run Only Model Training
```bash
python src/module2_predictive/train_model.py
```

### Run Only Fraud Detection Training
```bash
python src/module3_fraud_detection/train_fraud_detector.py
```

### Run Only EDA
```bash
python notebooks/01_exploratory_analysis.py
```

## 📈 Expected Performance

- **Accuracy**: 85-95%
- **Precision**: 80-90%
- **Recall**: 80-90%
- **F1 Score**: 80-90%
- **API Latency**: <100ms

## 🆘 Common Issues

### Issue: Module not found
**Solution**: Make sure you're in the project root directory and virtual environment is activated.

### Issue: Data file not found
**Solution**: Ensure `card_fraud.csv_processed.csv` is in the project root.

### Issue: Port already in use
**Solution**: Change port in `config/config.py` or kill existing process.

## 📚 Next Steps

1. **Explore API**: Visit http://localhost:8000/docs
2. **Review Metrics**: Check model performance in console output
3. **Customize**: Modify `config/config.py` for your needs
4. **Deploy**: Follow `DEPLOYMENT_GUIDE.md` for production deployment

## 💡 Tips

- **Faster Training**: Reduce `n_estimators` in model configs
- **Better Accuracy**: Increase ensemble models
- **Production Ready**: Add authentication and HTTPS
- **Scale Up**: Use multiple API workers

## 📖 Documentation

- **Full Documentation**: `PROJECT_DOCUMENTATION.md`
- **Deployment Guide**: `DEPLOYMENT_GUIDE.md`
- **README**: `README.md`

## 🎉 Success!

If everything works, you should see:
- ✅ Models trained and saved
- ✅ API server running
- ✅ Test results showing fraud detection
- ✅ Visualizations generated

**Congratulations! Your fraud detection system is ready!** 🚀

---

**Need Help?** Check the troubleshooting section in `DEPLOYMENT_GUIDE.md`
