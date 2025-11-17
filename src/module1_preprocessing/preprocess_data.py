"""
Main preprocessing pipeline
Orchestrates data loading, cleaning, feature engineering, and splitting
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from pathlib import Path
import joblib
import logging
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.module1_preprocessing.data_loader import TransactionDataLoader
from src.module1_preprocessing.feature_engineer import FeatureEngineer
from config.config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Main preprocessing pipeline"""
    
    def __init__(self, data_path: str):
        """
        Initialize preprocessor
        
        Args:
            data_path: Path to raw data file
        """
        self.data_path = data_path
        self.loader = TransactionDataLoader(data_path)
        self.engineer = FeatureEngineer()
        self.df_processed = None
        
    def run_preprocessing(self, save_artifacts: bool = True) -> dict:
        """
        Run complete preprocessing pipeline
        
        Args:
            save_artifacts: Whether to save processed data and artifacts
            
        Returns:
            Dictionary containing processed datasets
        """
        logger.info("="*50)
        logger.info("Starting Preprocessing Pipeline")
        logger.info("="*50)
        
        # Step 1: Load data
        df = self.loader.load_data()
        
        # Step 2: Validate data
        validation_stats = self.loader.validate_data()
        
        # Step 3: Feature engineering
        df_engineered = self.engineer.engineer_all_features(df, fit=True)
        
        # Step 4: Handle missing values (if any)
        df_engineered = self._handle_missing_values(df_engineered)

        # Step 4.5: Keep only numeric features for modeling to avoid object dtypes
        # This prevents downstream model errors (e.g., XGBoost) on object columns
        non_target_cols = [c for c in df_engineered.columns if c != TARGET_COLUMN]
        numeric_cols = df_engineered[non_target_cols].select_dtypes(include=[np.number]).columns.tolist()
        kept_cols = numeric_cols + ([TARGET_COLUMN] if TARGET_COLUMN in df_engineered.columns else [])
        df_engineered = df_engineered[kept_cols]
        logger.info(f"Filtered to numeric features: {len(numeric_cols)} kept (plus target)")
        
        # Step 5: Split data
        datasets = self._split_data(df_engineered)
        
        # Step 6: Save artifacts
        if save_artifacts:
            self._save_artifacts(datasets)
        
        logger.info("="*50)
        logger.info("Preprocessing Pipeline Completed")
        logger.info("="*50)
        
        return datasets
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values in the dataset
        
        Args:
            df: DataFrame with potential missing values
            
        Returns:
            DataFrame with missing values handled
        """
        logger.info("Handling missing values...")
        
        missing_before = df.isnull().sum().sum()
        
        if missing_before > 0:
            # Fill numerical columns with median
            numerical_cols = df.select_dtypes(include=[np.number]).columns
            for col in numerical_cols:
                if df[col].isnull().sum() > 0:
                    df[col].fillna(df[col].median(), inplace=True)
            
            # Fill categorical columns with mode
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                if df[col].isnull().sum() > 0:
                    df[col].fillna(df[col].mode()[0], inplace=True)
            
            missing_after = df.isnull().sum().sum()
            logger.info(f"Missing values handled: {missing_before} -> {missing_after}")
        else:
            logger.info("No missing values found")
        
        return df
    
    def _split_data(self, df: pd.DataFrame) -> dict:
        """
        Split data into train, validation, and test sets
        
        Args:
            df: DataFrame to split
            
        Returns:
            Dictionary containing train, val, and test datasets
        """
        logger.info("Splitting data into train/val/test sets...")
        
        # Separate features and target
        X = df.drop(columns=['isFraud'])
        y = df['isFraud']
        
        # First split: train+val and test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED, stratify=y
        )
        
        # Second split: train and val
        val_size_adjusted = VAL_SIZE / (1 - TEST_SIZE)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size_adjusted, random_state=RANDOM_SEED, stratify=y_temp
        )
        
        logger.info(f"Train set: {len(X_train)} samples ({len(X_train)/len(df)*100:.1f}%)")
        logger.info(f"Validation set: {len(X_val)} samples ({len(X_val)/len(df)*100:.1f}%)")
        logger.info(f"Test set: {len(X_test)} samples ({len(X_test)/len(df)*100:.1f}%)")
        
        logger.info(f"Train fraud rate: {y_train.mean():.2%}")
        logger.info(f"Val fraud rate: {y_val.mean():.2%}")
        logger.info(f"Test fraud rate: {y_test.mean():.2%}")
        
        return {
            'X_train': X_train,
            'X_val': X_val,
            'X_test': X_test,
            'y_train': y_train,
            'y_val': y_val,
            'y_test': y_test
        }
    
    def _save_artifacts(self, datasets: dict):
        """
        Save processed data and preprocessing artifacts
        
        Args:
            datasets: Dictionary containing processed datasets
        """
        logger.info("Saving preprocessing artifacts...")
        
        # Create directories
        PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        (MODELS_DIR / "preprocessing").mkdir(parents=True, exist_ok=True)
        
        # Save datasets
        train_df = pd.concat([datasets['X_train'], datasets['y_train']], axis=1)
        val_df = pd.concat([datasets['X_val'], datasets['y_val']], axis=1)
        test_df = pd.concat([datasets['X_test'], datasets['y_test']], axis=1)
        
        train_df.to_csv(TRAIN_DATA_FILE, index=False)
        val_df.to_csv(VAL_DATA_FILE, index=False)
        test_df.to_csv(TEST_DATA_FILE, index=False)
        
        logger.info(f"Saved train data to {TRAIN_DATA_FILE}")
        logger.info(f"Saved validation data to {VAL_DATA_FILE}")
        logger.info(f"Saved test data to {TEST_DATA_FILE}")
        
        # Save feature engineer
        joblib.dump(self.engineer, MODELS_DIR / "preprocessing" / "feature_engineer.pkl")
        logger.info("Saved feature engineer")
        
        # Save feature names
        feature_names = datasets['X_train'].columns.tolist()
        joblib.dump(feature_names, MODELS_DIR / "preprocessing" / "feature_names.pkl")
        logger.info(f"Saved {len(feature_names)} feature names")
        
        # Save preprocessing metadata
        metadata = {
            'n_features': len(feature_names),
            'train_size': len(datasets['X_train']),
            'val_size': len(datasets['X_val']),
            'test_size': len(datasets['X_test']),
            'fraud_rate_train': datasets['y_train'].mean(),
            'fraud_rate_val': datasets['y_val'].mean(),
            'fraud_rate_test': datasets['y_test'].mean(),
            'random_seed': RANDOM_SEED
        }
        joblib.dump(metadata, MODELS_DIR / "preprocessing" / "metadata.pkl")
        logger.info("Saved preprocessing metadata")


def main():
    """Main execution function"""
    # Initialize preprocessor
    data_path = Path(__file__).parent.parent.parent / "card_fraud.csv_processed.csv"
    preprocessor = DataPreprocessor(str(data_path))
    
    # Run preprocessing
    datasets = preprocessor.run_preprocessing(save_artifacts=True)
    
    print("\n" + "="*50)
    print("PREPROCESSING SUMMARY")
    print("="*50)
    print(f"Total features: {datasets['X_train'].shape[1]}")
    print(f"Training samples: {len(datasets['X_train'])}")
    print(f"Validation samples: {len(datasets['X_val'])}")
    print(f"Test samples: {len(datasets['X_test'])}")
    print(f"\nFraud rates:")
    print(f"  Train: {datasets['y_train'].mean():.2%}")
    print(f"  Val: {datasets['y_val'].mean():.2%}")
    print(f"  Test: {datasets['y_test'].mean():.2%}")
    print("="*50)


if __name__ == "__main__":
    main()
