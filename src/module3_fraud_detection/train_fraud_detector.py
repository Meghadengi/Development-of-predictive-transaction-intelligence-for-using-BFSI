"""
Train Fraud Detection Model
Main training script for Module 3
"""
import pandas as pd
import numpy as np
import sys
from pathlib import Path
import joblib
import logging

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.module3_fraud_detection.fraud_detector import FraudDetector, AnomalyDetector
from src.module2_predictive.transaction_predictor import TransactionPredictor
from config.config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FraudDetectorTrainer:
    """Train fraud detection system"""
    
    def __init__(self):
        """Initialize trainer"""
        self.fraud_detector = FraudDetector()
        self.anomaly_detector = AnomalyDetector()
        self.model = None
    
    def load_data(self) -> dict:
        """
        Load preprocessed data
        
        Returns:
            Dictionary containing datasets
        """
        logger.info("Loading preprocessed data...")
        
        train_df = pd.read_csv(TRAIN_DATA_FILE)
        val_df = pd.read_csv(VAL_DATA_FILE)
        test_df = pd.read_csv(TEST_DATA_FILE)
        
        X_train = train_df.drop(columns=[TARGET_COLUMN])
        y_train = train_df[TARGET_COLUMN]
        
        X_val = val_df.drop(columns=[TARGET_COLUMN])
        y_val = val_df[TARGET_COLUMN]
        
        X_test = test_df.drop(columns=[TARGET_COLUMN])
        y_test = test_df[TARGET_COLUMN]
        
        logger.info(f"Loaded train: {X_train.shape}, val: {X_val.shape}, test: {X_test.shape}")
        
        return {
            'X_train': X_train,
            'y_train': y_train,
            'X_val': X_val,
            'y_val': y_val,
            'X_test': X_test,
            'y_test': y_test,
            'train_df': train_df,
            'test_df': test_df
        }
    
    def train_fraud_model(self, datasets: dict) -> dict:
        """
        Train fraud detection model
        
        Args:
            datasets: Dictionary containing datasets
            
        Returns:
            Training results
        """
        logger.info("="*50)
        logger.info("Training Fraud Detection Model")
        logger.info("="*50)
        
        # Train XGBoost model optimized for fraud detection
        self.model = TransactionPredictor(model_type='xgboost')
        
        results = self.model.train(
            datasets['X_train'], datasets['y_train'],
            datasets['X_val'], datasets['y_val']
        )
        
        logger.info("Fraud detection model trained successfully")
        
        return results
    
    def train_anomaly_detector(self, datasets: dict):
        """
        Train anomaly detector on normal transactions
        
        Args:
            datasets: Dictionary containing datasets
        """
        logger.info("\nTraining anomaly detector...")
        
        # Get normal transactions from training data
        normal_transactions = datasets['train_df'][datasets['train_df'][TARGET_COLUMN] == 0]
        
        self.anomaly_detector.learn_baseline(normal_transactions)
        
        logger.info("Anomaly detector trained successfully")
    
    def evaluate_fraud_detection(self, datasets: dict) -> dict:
        """
        Evaluate fraud detection system
        
        Args:
            datasets: Dictionary containing datasets
            
        Returns:
            Evaluation metrics
        """
        logger.info("\n" + "="*50)
        logger.info("Evaluating Fraud Detection System")
        logger.info("="*50)
        
        # Load model into fraud detector
        self.fraud_detector.model = self.model.model
        
        # Test on sample transactions
        test_sample = datasets['test_df'].head(100)
        
        detection_results = []
        for idx, row in test_sample.iterrows():
            X_row = row.drop(TARGET_COLUMN).to_frame().T
            transaction_dict = row.to_dict()
            
            result = self.fraud_detector.detect_fraud(X_row, transaction_dict)
            result['actual_fraud'] = row[TARGET_COLUMN]
            detection_results.append(result)
        
        # Calculate metrics
        y_true = [r['actual_fraud'] for r in detection_results]
        y_pred = [r['is_fraud'] for r in detection_results]
        
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1_score': f1_score(y_true, y_pred, zero_division=0)
        }
        
        logger.info("\nFraud Detection Metrics:")
        logger.info(f"  Accuracy:  {metrics['accuracy']:.4f}")
        logger.info(f"  Precision: {metrics['precision']:.4f}")
        logger.info(f"  Recall:    {metrics['recall']:.4f}")
        logger.info(f"  F1 Score:  {metrics['f1_score']:.4f}")
        
        # Get statistics
        stats = self.fraud_detector.get_fraud_statistics(detection_results)
        
        logger.info("\nDetection Statistics:")
        logger.info(f"  Total transactions: {stats['total_transactions']}")
        logger.info(f"  Fraud detected: {stats['fraud_detected']}")
        logger.info(f"  Fraud rate: {stats['fraud_rate']:.2%}")
        logger.info(f"  High risk: {stats['high_risk_count']}")
        logger.info(f"  Medium risk: {stats['medium_risk_count']}")
        logger.info(f"  Low risk: {stats['low_risk_count']}")
        
        return {
            'metrics': metrics,
            'statistics': stats,
            'sample_results': detection_results[:5]
        }
    
    def test_real_time_detection(self, datasets: dict):
        """
        Test real-time fraud detection
        
        Args:
            datasets: Dictionary containing datasets
        """
        logger.info("\n" + "="*50)
        logger.info("Testing Real-Time Fraud Detection")
        logger.info("="*50)
        
        # Get a few test transactions
        test_transactions = datasets['test_df'].head(5)
        
        for idx, row in test_transactions.iterrows():
            X_row = row.drop(TARGET_COLUMN).to_frame().T
            transaction_dict = row.to_dict()
            
            # Detect fraud
            result = self.fraud_detector.detect_fraud(X_row, transaction_dict)
            
            # Generate alert if needed
            if result['risk_level'] in ['HIGH', 'MEDIUM']:
                alert = self.fraud_detector.generate_alert(result, transaction_dict)
                
                logger.info(f"\n🚨 ALERT: {alert['alert_id']}")
                logger.info(f"   Risk Level: {alert['risk_level']}")
                logger.info(f"   Risk Score: {alert['risk_score']:.4f}")
                logger.info(f"   Amount: {alert['transaction_amount']}")
                logger.info(f"   Location: {alert['transaction_location']}")
                logger.info(f"   Triggered Rules: {', '.join(alert['triggered_rules'])}")
                logger.info(f"   Recommendation: {alert['recommendation']}")
            else:
                logger.info(f"\n✓ Transaction {idx}: LOW RISK (Score: {result['combined_risk_score']:.4f})")
    
    def save_models(self):
        """Save trained models"""
        logger.info("\nSaving fraud detection models...")
        
        # Create directory
        (MODELS_DIR / "fraud_detection").mkdir(parents=True, exist_ok=True)
        
        # Save fraud detection model
        self.model.save_model(str(FRAUD_MODEL_PATH))
        
        # Save anomaly detector
        joblib.dump(self.anomaly_detector, MODELS_DIR / "fraud_detection" / "anomaly_detector.pkl")
        
        # Save fraud detector configuration
        joblib.dump(self.fraud_detector.risk_rules, MODELS_DIR / "fraud_detection" / "risk_rules.pkl")
        
        logger.info("Models saved successfully")
    
    def run_training_pipeline(self):
        """Run complete training pipeline"""
        # Load data
        datasets = self.load_data()
        
        # Train fraud detection model
        training_results = self.train_fraud_model(datasets)
        
        # Train anomaly detector
        self.train_anomaly_detector(datasets)
        
        # Evaluate fraud detection
        evaluation_results = self.evaluate_fraud_detection(datasets)
        
        # Test real-time detection
        self.test_real_time_detection(datasets)
        
        # Save models
        self.save_models()
        
        return {
            'training_results': training_results,
            'evaluation_results': evaluation_results
        }


def main():
    """Main execution function"""
    print("\n" + "="*50)
    print("FRAUD DETECTION ENGINE")
    print("Module 3: Training Pipeline")
    print("="*50)
    
    # Initialize trainer
    trainer = FraudDetectorTrainer()
    
    # Run training
    results = trainer.run_training_pipeline()
    
    print("\n" + "="*50)
    print("FRAUD DETECTION TRAINING COMPLETED")
    print("="*50)
    print("\nEvaluation Metrics:")
    for metric, value in results['evaluation_results']['metrics'].items():
        print(f"  {metric}: {value:.4f}")
    print("="*50)


if __name__ == "__main__":
    main()
