"""
Train Predictive Transaction Model
Main training script for Module 2
"""
import pandas as pd
import numpy as np
import sys
from pathlib import Path
import joblib
import logging

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.module2_predictive.transaction_predictor import TransactionPredictor, EnsemblePredictor
from src.module2_predictive.llm_embeddings import TransactionEmbedder
from config.config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """Train and evaluate predictive models"""
    
    def __init__(self, use_embeddings: bool = False, use_ensemble: bool = True):
        """
        Initialize model trainer
        
        Args:
            use_embeddings: Whether to use LLM embeddings
            use_ensemble: Whether to use ensemble of models
        """
        self.use_embeddings = use_embeddings
        self.use_ensemble = use_ensemble
        self.embedder = None
        self.predictor = None
        
    def load_data(self) -> dict:
        """
        Load preprocessed data
        
        Returns:
            Dictionary containing train, val, and test datasets
        """
        logger.info("Loading preprocessed data...")
        
        train_df = pd.read_csv(TRAIN_DATA_FILE)
        val_df = pd.read_csv(VAL_DATA_FILE)
        test_df = pd.read_csv(TEST_DATA_FILE)
        
        # Separate features and target
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
            'y_test': y_test
        }
    
    def add_embeddings(self, datasets: dict) -> dict:
        """
        Add LLM embeddings to datasets
        
        Args:
            datasets: Dictionary containing datasets
            
        Returns:
            Dictionary with datasets including embeddings
        """
        logger.info("Adding LLM embeddings...")
        
        self.embedder = TransactionEmbedder()
        
        # Add embeddings to each dataset
        datasets['X_train'] = self.embedder.add_embeddings_to_dataframe(datasets['X_train'])
        datasets['X_val'] = self.embedder.add_embeddings_to_dataframe(datasets['X_val'])
        datasets['X_test'] = self.embedder.add_embeddings_to_dataframe(datasets['X_test'])
        
        logger.info("Embeddings added successfully")
        
        return datasets
    
    def train_models(self, datasets: dict) -> dict:
        """
        Train prediction models
        
        Args:
            datasets: Dictionary containing datasets
            
        Returns:
            Dictionary containing training results
        """
        logger.info("="*50)
        logger.info("Starting Model Training")
        logger.info("="*50)
        
        if self.use_ensemble:
            logger.info("Training ensemble of models...")
            self.predictor = EnsemblePredictor()
            results = self.predictor.train(
                datasets['X_train'], datasets['y_train'],
                datasets['X_val'], datasets['y_val']
            )
        else:
            logger.info("Training single XGBoost model...")
            self.predictor = TransactionPredictor(model_type='xgboost')
            results = self.predictor.train(
                datasets['X_train'], datasets['y_train'],
                datasets['X_val'], datasets['y_val']
            )
        
        logger.info("="*50)
        logger.info("Model Training Completed")
        logger.info("="*50)
        
        return results
    
    def evaluate_on_test(self, datasets: dict) -> dict:
        """
        Evaluate model on test set
        
        Args:
            datasets: Dictionary containing datasets
            
        Returns:
            Dictionary containing test metrics
        """
        logger.info("\n" + "="*50)
        logger.info("Evaluating on Test Set")
        logger.info("="*50)
        
        if self.use_ensemble:
            # Evaluate ensemble
            y_pred = self.predictor.predict(datasets['X_test'])
            y_proba = self.predictor.predict_proba(datasets['X_test'])[:, 1]
        else:
            # Evaluate single model
            y_pred = self.predictor.predict(datasets['X_test'])
            y_proba = self.predictor.predict_proba(datasets['X_test'])[:, 1]
        
        # Calculate metrics
        from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                                     f1_score, roc_auc_score, confusion_matrix, 
                                     classification_report)
        
        test_metrics = {
            'accuracy': accuracy_score(datasets['y_test'], y_pred),
            'precision': precision_score(datasets['y_test'], y_pred, zero_division=0),
            'recall': recall_score(datasets['y_test'], y_pred, zero_division=0),
            'f1_score': f1_score(datasets['y_test'], y_pred, zero_division=0),
            'roc_auc': roc_auc_score(datasets['y_test'], y_proba)
        }
        
        logger.info("\nTest Set Metrics:")
        logger.info(f"  Accuracy:  {test_metrics['accuracy']:.4f}")
        logger.info(f"  Precision: {test_metrics['precision']:.4f}")
        logger.info(f"  Recall:    {test_metrics['recall']:.4f}")
        logger.info(f"  F1 Score:  {test_metrics['f1_score']:.4f}")
        logger.info(f"  ROC AUC:   {test_metrics['roc_auc']:.4f}")
        
        # Confusion matrix
        cm = confusion_matrix(datasets['y_test'], y_pred)
        logger.info("\nConfusion Matrix:")
        logger.info(f"  TN: {cm[0,0]}, FP: {cm[0,1]}")
        logger.info(f"  FN: {cm[1,0]}, TP: {cm[1,1]}")
        
        # Classification report
        logger.info("\nClassification Report:")
        logger.info("\n" + classification_report(datasets['y_test'], y_pred))
        
        return test_metrics
    
    def save_models(self):
        """Save trained models"""
        logger.info("\nSaving models...")
        
        # Create model directories
        (MODELS_DIR / "predictive").mkdir(parents=True, exist_ok=True)
        
        if self.use_ensemble:
            self.predictor.save_ensemble(str(MODELS_DIR / "predictive" / "ensemble"))
        else:
            self.predictor.save_model(str(PREDICTIVE_MODEL_PATH))
        
        # Save embedder if used
        if self.embedder:
            joblib.dump(self.embedder, MODELS_DIR / "predictive" / "embedder.pkl")
            logger.info("Saved embedder")
        
        logger.info("Models saved successfully")
    
    def run_training_pipeline(self):
        """Run complete training pipeline"""
        # Load data
        datasets = self.load_data()
        
        # Add embeddings if requested
        if self.use_embeddings:
            datasets = self.add_embeddings(datasets)
        
        # Train models
        training_results = self.train_models(datasets)
        
        # Evaluate on test set
        test_metrics = self.evaluate_on_test(datasets)
        
        # Save models
        self.save_models()
        
        return {
            'training_results': training_results,
            'test_metrics': test_metrics
        }


def main():
    """Main execution function"""
    print("\n" + "="*50)
    print("PREDICTIVE TRANSACTION MODELING")
    print("Module 2: Training Pipeline")
    print("="*50)
    
    # Initialize trainer
    trainer = ModelTrainer(
        use_embeddings=False,  # Set to True to use LLM embeddings (requires transformers)
        use_ensemble=True      # Use ensemble of models for better performance
    )
    
    # Run training
    results = trainer.run_training_pipeline()
    
    print("\n" + "="*50)
    print("TRAINING COMPLETED SUCCESSFULLY")
    print("="*50)
    print("\nFinal Test Metrics:")
    for metric, value in results['test_metrics'].items():
        print(f"  {metric}: {value:.4f}")
    print("="*50)


if __name__ == "__main__":
    main()
