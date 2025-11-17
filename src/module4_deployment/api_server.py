"""
FastAPI Server for Fraud Detection System
Provides REST API endpoints for real-time fraud detection
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import sys
import logging
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.module3_fraud_detection.fraud_detector import FraudDetector
from src.module1_preprocessing.feature_engineer import FeatureEngineer
from config.config import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Predictive Transaction Intelligence API",
    description="AI-driven fraud detection and transaction prediction for BFSI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for models
fraud_detector = None
feature_engineer = None
model_loaded = False


# Pydantic models for request/response
class Transaction(BaseModel):
    """Transaction data model"""
    Transaction_Amount: float = Field(..., description="Transaction amount")
    Transaction_Date: str = Field(..., description="Transaction date (YYYY-MM-DD)")
    Transaction_Time: str = Field(..., description="Transaction time (HH:MM:SS)")
    Transaction_Location: str = Field(..., description="Transaction location")
    Card_Type: str = Field(..., description="Card type (e.g., Visa, Mastercard)")
    Transaction_Currency: str = Field(..., description="Currency code")
    Transaction_Status: str = Field(..., description="Transaction status")
    Previous_Transaction_Count: int = Field(..., description="Number of previous transactions")
    Distance_Between_Transactions_km: float = Field(..., description="Distance from last transaction")
    Time_Since_Last_Transaction_min: int = Field(..., description="Time since last transaction in minutes")
    Authentication_Method: str = Field(..., description="Authentication method used")
    Transaction_Velocity: int = Field(..., description="Transaction velocity")
    Transaction_Category: str = Field(..., description="Transaction category")
    
    class Config:
        schema_extra = {
            "example": {
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
        }


class FraudDetectionResponse(BaseModel):
    """Fraud detection response model"""
    is_fraud: bool
    ml_risk_score: float
    rule_risk_score: float
    combined_risk_score: float
    risk_level: str
    triggered_rules: List[str]
    recommendation: str
    timestamp: str
    processing_time_ms: float


class BatchTransaction(BaseModel):
    """Batch of transactions"""
    transactions: List[Transaction]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    timestamp: str


class MetricsResponse(BaseModel):
    """Metrics response"""
    total_requests: int
    fraud_detected: int
    fraud_rate: float
    avg_processing_time_ms: float
    uptime_seconds: float


# Global metrics
metrics = {
    'total_requests': 0,
    'fraud_detected': 0,
    'processing_times': [],
    'start_time': datetime.now()
}


@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    global fraud_detector, feature_engineer, model_loaded
    
    logger.info("Starting Fraud Detection API...")
    
    try:
        # Load fraud detection model
        fraud_model_path = FRAUD_MODEL_PATH
        if fraud_model_path.exists():
            fraud_detector = FraudDetector(str(fraud_model_path))
            logger.info("Fraud detection model loaded successfully")
        else:
            logger.warning(f"Fraud model not found at {fraud_model_path}")
            fraud_detector = FraudDetector()  # Initialize without model
        
        # Load feature engineer
        engineer_path = MODELS_DIR / "preprocessing" / "feature_engineer.pkl"
        if engineer_path.exists():
            feature_engineer = joblib.load(engineer_path)
            logger.info("Feature engineer loaded successfully")
        else:
            logger.warning(f"Feature engineer not found at {engineer_path}")
            feature_engineer = FeatureEngineer()
        
        model_loaded = True
        logger.info("API startup completed successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        model_loaded = False


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Predictive Transaction Intelligence API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "detect_fraud": "/detect/fraud",
            "batch_detect": "/detect/batch",
            "metrics": "/metrics",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        model_loaded=model_loaded,
        timestamp=datetime.now().isoformat()
    )


@app.post("/detect/fraud", response_model=FraudDetectionResponse, tags=["Fraud Detection"])
async def detect_fraud(transaction: Transaction):
    """
    Detect fraud in a single transaction
    
    Args:
        transaction: Transaction data
        
    Returns:
        Fraud detection result
    """
    start_time = datetime.now()
    
    try:
        # Convert to DataFrame
        transaction_dict = transaction.dict()
        transaction_df = pd.DataFrame([transaction_dict])
        
        # Engineer features
        if feature_engineer:
            transaction_df = feature_engineer.engineer_all_features(transaction_df, fit=False)
        
        # Detect fraud
        if fraud_detector:
            result = fraud_detector.detect_fraud(transaction_df, transaction_dict)
        else:
            raise HTTPException(status_code=503, detail="Fraud detection model not available")
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        result['processing_time_ms'] = processing_time
        
        # Update metrics
        metrics['total_requests'] += 1
        metrics['processing_times'].append(processing_time)
        if result['is_fraud']:
            metrics['fraud_detected'] += 1
        
        logger.info(f"Fraud detection completed in {processing_time:.2f}ms - Risk: {result['risk_level']}")
        
        return FraudDetectionResponse(**result)
        
    except Exception as e:
        logger.error(f"Error in fraud detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/detect/batch", tags=["Fraud Detection"])
async def batch_detect_fraud(batch: BatchTransaction):
    """
    Detect fraud in multiple transactions
    
    Args:
        batch: Batch of transactions
        
    Returns:
        List of fraud detection results
    """
    start_time = datetime.now()
    
    try:
        results = []
        
        for transaction in batch.transactions:
            transaction_dict = transaction.dict()
            transaction_df = pd.DataFrame([transaction_dict])
            
            # Engineer features
            if feature_engineer:
                transaction_df = feature_engineer.engineer_all_features(transaction_df, fit=False)
            
            # Detect fraud
            if fraud_detector:
                result = fraud_detector.detect_fraud(transaction_df, transaction_dict)
                results.append(result)
            else:
                raise HTTPException(status_code=503, detail="Fraud detection model not available")
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Update metrics
        metrics['total_requests'] += len(batch.transactions)
        metrics['processing_times'].append(processing_time / len(batch.transactions))
        fraud_count = sum(1 for r in results if r['is_fraud'])
        metrics['fraud_detected'] += fraud_count
        
        logger.info(f"Batch detection completed: {len(results)} transactions in {processing_time:.2f}ms")
        
        return {
            "total_transactions": len(results),
            "fraud_detected": fraud_count,
            "processing_time_ms": processing_time,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error in batch fraud detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics", response_model=MetricsResponse, tags=["Monitoring"])
async def get_metrics():
    """Get API metrics"""
    uptime = (datetime.now() - metrics['start_time']).total_seconds()
    
    return MetricsResponse(
        total_requests=metrics['total_requests'],
        fraud_detected=metrics['fraud_detected'],
        fraud_rate=metrics['fraud_detected'] / metrics['total_requests'] if metrics['total_requests'] > 0 else 0,
        avg_processing_time_ms=np.mean(metrics['processing_times']) if metrics['processing_times'] else 0,
        uptime_seconds=uptime
    )


@app.post("/predict/transaction", tags=["Prediction"])
async def predict_transaction(transaction: Transaction):
    """
    Predict next transaction behavior
    
    Args:
        transaction: Current transaction data
        
    Returns:
        Prediction result
    """
    # This endpoint can be extended with transaction prediction logic
    return {
        "message": "Transaction prediction endpoint",
        "status": "not_implemented",
        "note": "This endpoint will predict next transaction patterns"
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Fraud Detection API Server...")
    logger.info(f"Host: {API_HOST}")
    logger.info(f"Port: {API_PORT}")
    
    uvicorn.run(
        "api_server:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )
