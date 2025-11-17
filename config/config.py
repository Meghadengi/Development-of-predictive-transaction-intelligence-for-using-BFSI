"""
Configuration file for Fraud Detection System
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FEATURES_DATA_DIR = DATA_DIR / "features"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
for dir_path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, FEATURES_DATA_DIR, MODELS_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Data configuration
RAW_DATA_FILE = "card_fraud.csv_processed.csv"
TRAIN_DATA_FILE = PROCESSED_DATA_DIR / "train_data.csv"
TEST_DATA_FILE = PROCESSED_DATA_DIR / "test_data.csv"
VAL_DATA_FILE = PROCESSED_DATA_DIR / "val_data.csv"

# Model configuration
PREDICTIVE_MODEL_PATH = MODELS_DIR / "predictive" / "transaction_predictor.pkl"
FRAUD_MODEL_PATH = MODELS_DIR / "fraud_detection" / "fraud_detector.pkl"
LLM_MODEL_NAME = "distilbert-base-uncased"  # Lightweight LLM for transaction analysis

# Training configuration
RANDOM_SEED = 42
TEST_SIZE = 0.2
VAL_SIZE = 0.1
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.001

# Feature engineering
NUMERICAL_FEATURES = [
    'Transaction_Amount',
    'Previous_Transaction_Count',
    'Distance_Between_Transactions_km',
    'Time_Since_Last_Transaction_min',
    'Transaction_Velocity',
    'Log_Transaction_Amount',
    'Velocity_Distance_Interact'
]

CATEGORICAL_FEATURES = [
    'Transaction_Location',
    'Card_Type',
    'Transaction_Currency',
    'Transaction_Status',
    'Authentication_Method',
    'Transaction_Category'
]

TIME_FEATURES = [
    'Transaction_Date',
    'Transaction_Time'
]

TARGET_COLUMN = 'isFraud'

# Fraud detection thresholds
FRAUD_THRESHOLD = 0.5
HIGH_RISK_THRESHOLD = 0.7
MEDIUM_RISK_THRESHOLD = 0.4

# API configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
API_WORKERS = 4

# Monitoring
ENABLE_LOGGING = True
LOG_LEVEL = "INFO"
METRICS_ENABLED = True

# Real-time processing
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
QUEUE_NAME = "fraud_detection_queue"
