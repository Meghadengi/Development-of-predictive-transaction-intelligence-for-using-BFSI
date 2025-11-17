"""
Transaction Prediction Model
Uses ensemble methods and LLM embeddings to predict transaction patterns
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, precision_recall_curve
import xgboost as xgb
import lightgbm as lgb
from typing import Dict, Tuple
import joblib
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransactionPredictor:
    """Predict transaction patterns and behaviors"""
    
    def __init__(self, model_type: str = 'xgboost'):
        """
        Initialize transaction predictor
        
        Args:
            model_type: Type of model to use ('xgboost', 'lightgbm', 'random_forest', 'gradient_boosting')
        """
        self.model_type = model_type
        self.model = None
        self.feature_importance = None
        self.threshold = 0.5
        
    def _initialize_model(self):
        """Initialize the prediction model"""
        if self.model_type == 'xgboost':
            self.model = xgb.XGBClassifier(
                n_estimators=200,
                max_depth=8,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                eval_metric='logloss',
                use_label_encoder=False
            )
        elif self.model_type == 'lightgbm':
            self.model = lgb.LGBMClassifier(
                n_estimators=200,
                max_depth=8,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42
            )
        elif self.model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == 'gradient_boosting':
            self.model = GradientBoostingClassifier(
                n_estimators=200,
                max_depth=8,
                learning_rate=0.05,
                subsample=0.8,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        logger.info(f"Initialized {self.model_type} model")
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series, 
              X_val: pd.DataFrame = None, y_val: pd.Series = None) -> Dict:
        """
        Train the prediction model
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features (optional)
            y_val: Validation labels (optional)
            
        Returns:
            Dictionary containing training metrics
        """
        logger.info(f"Training {self.model_type} model...")
        
        self._initialize_model()
        
        # Train model
        if self.model_type in ['xgboost', 'lightgbm'] and X_val is not None:
            # Some versions of LightGBM's sklearn API don't accept 'verbose'.
            # Fit with eval_set only to avoid TypeError.
            self.model.fit(
                X_train, y_train,
                eval_set=[(X_val, y_val)]
            )
        else:
            self.model.fit(X_train, y_train)
        
        # Get feature importance
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.DataFrame({
                'feature': X_train.columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
        
        # Evaluate on training data
        train_metrics = self.evaluate(X_train, y_train, dataset_name="Training")
        
        # Evaluate on validation data if provided
        val_metrics = None
        if X_val is not None and y_val is not None:
            val_metrics = self.evaluate(X_val, y_val, dataset_name="Validation")
        
        logger.info("Training completed")
        
        return {
            'train_metrics': train_metrics,
            'val_metrics': val_metrics,
            'feature_importance': self.feature_importance
        }
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict transaction classes
        
        Args:
            X: Features to predict
            
        Returns:
            Array of predictions (0 or 1)
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        return self.model.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict transaction probabilities
        
        Args:
            X: Features to predict
            
        Returns:
            Array of probabilities for each class
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        return self.model.predict_proba(X)
    
    def predict_risk_score(self, X: pd.DataFrame) -> np.ndarray:
        """
        Get risk scores (probability of fraud)
        
        Args:
            X: Features to predict
            
        Returns:
            Array of risk scores (0-1)
        """
        proba = self.predict_proba(X)
        return proba[:, 1]  # Probability of fraud class
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series, dataset_name: str = "Test") -> Dict:
        """
        Evaluate model performance
        
        Args:
            X: Features
            y: True labels
            dataset_name: Name of the dataset for logging
            
        Returns:
            Dictionary containing evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Predictions
        y_pred = self.predict(X)
        y_proba = self.predict_proba(X)[:, 1]
        
        # Calculate metrics
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        metrics = {
            'accuracy': accuracy_score(y, y_pred),
            'precision': precision_score(y, y_pred, zero_division=0),
            'recall': recall_score(y, y_pred, zero_division=0),
            'f1_score': f1_score(y, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y, y_proba)
        }
        
        logger.info(f"\n{dataset_name} Metrics:")
        logger.info(f"  Accuracy:  {metrics['accuracy']:.4f}")
        logger.info(f"  Precision: {metrics['precision']:.4f}")
        logger.info(f"  Recall:    {metrics['recall']:.4f}")
        logger.info(f"  F1 Score:  {metrics['f1_score']:.4f}")
        logger.info(f"  ROC AUC:   {metrics['roc_auc']:.4f}")
        
        return metrics
    
    def get_feature_importance(self, top_n: int = 20) -> pd.DataFrame:
        """
        Get top N most important features
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            DataFrame with feature importance
        """
        if self.feature_importance is None:
            raise ValueError("Feature importance not available")
        
        return self.feature_importance.head(top_n)
    
    def save_model(self, path: str):
        """
        Save model to disk
        
        Args:
            path: Path to save the model
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'feature_importance': self.feature_importance,
            'threshold': self.threshold
        }
        
        joblib.dump(model_data, path)
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """
        Load model from disk
        
        Args:
            path: Path to load the model from
        """
        model_data = joblib.load(path)
        
        self.model = model_data['model']
        self.model_type = model_data['model_type']
        self.feature_importance = model_data.get('feature_importance')
        self.threshold = model_data.get('threshold', 0.5)
        
        logger.info(f"Model loaded from {path}")


class EnsemblePredictor:
    """Ensemble of multiple prediction models"""
    
    def __init__(self, model_types: list = None):
        """
        Initialize ensemble predictor
        
        Args:
            model_types: List of model types to use in ensemble
        """
        if model_types is None:
            model_types = ['xgboost', 'lightgbm', 'random_forest']
        
        self.models = {model_type: TransactionPredictor(model_type) for model_type in model_types}
        self.weights = None
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series,
              X_val: pd.DataFrame = None, y_val: pd.Series = None) -> Dict:
        """
        Train all models in the ensemble
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features
            y_val: Validation labels
            
        Returns:
            Dictionary containing training results for all models
        """
        logger.info("Training ensemble models...")
        
        results = {}
        
        for model_name, model in self.models.items():
            logger.info(f"\nTraining {model_name}...")
            result = model.train(X_train, y_train, X_val, y_val)
            results[model_name] = result
        
        # Calculate weights based on validation performance
        if X_val is not None and y_val is not None:
            self.weights = {}
            for model_name, result in results.items():
                self.weights[model_name] = result['val_metrics']['f1_score']
            
            # Normalize weights
            total_weight = sum(self.weights.values())
            self.weights = {k: v/total_weight for k, v in self.weights.items()}
            
            logger.info("\nEnsemble weights:")
            for model_name, weight in self.weights.items():
                logger.info(f"  {model_name}: {weight:.4f}")
        
        return results
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict probabilities using ensemble
        
        Args:
            X: Features to predict
            
        Returns:
            Array of averaged probabilities
        """
        predictions = []
        weights = []
        
        for model_name, model in self.models.items():
            pred = model.predict_proba(X)
            predictions.append(pred)
            weights.append(self.weights.get(model_name, 1.0) if self.weights else 1.0)
        
        # Weighted average
        weighted_pred = np.average(predictions, axis=0, weights=weights)
        return weighted_pred
    
    def predict(self, X: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        """
        Predict classes using ensemble
        
        Args:
            X: Features to predict
            threshold: Classification threshold
            
        Returns:
            Array of predictions
        """
        proba = self.predict_proba(X)
        return (proba[:, 1] >= threshold).astype(int)
    
    def save_ensemble(self, directory: str):
        """
        Save all models in the ensemble
        
        Args:
            directory: Directory to save models
        """
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        for model_name, model in self.models.items():
            model.save_model(f"{directory}/{model_name}_model.pkl")
        
        # Save weights
        if self.weights:
            joblib.dump(self.weights, f"{directory}/ensemble_weights.pkl")
        
        logger.info(f"Ensemble saved to {directory}")


if __name__ == "__main__":
    logger.info("Transaction Predictor module loaded successfully")
