"""
Data Loader for Transaction Data
Handles loading and initial validation of transaction data
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransactionDataLoader:
    """Load and validate transaction data"""
    
    def __init__(self, data_path: str):
        """
        Initialize data loader
        
        Args:
            data_path: Path to the transaction data file
        """
        self.data_path = Path(data_path)
        self.df = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load transaction data from CSV
        
        Returns:
            DataFrame containing transaction data
        """
        logger.info(f"Loading data from {self.data_path}")
        
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        self.df = pd.read_csv(self.data_path)
        logger.info(f"Loaded {len(self.df)} transactions with {len(self.df.columns)} features")
        
        return self.df
    
    def validate_data(self) -> dict:
        """
        Validate data quality and return statistics
        
        Returns:
            Dictionary containing validation statistics
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        validation_stats = {
            'total_records': len(self.df),
            'total_features': len(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict(),
            'duplicate_records': self.df.duplicated().sum(),
            'fraud_distribution': self.df['isFraud'].value_counts().to_dict() if 'isFraud' in self.df.columns else None,
            'fraud_rate': self.df['isFraud'].mean() if 'isFraud' in self.df.columns else None,
            'data_types': self.df.dtypes.to_dict()
        }
        
        logger.info("Data validation completed")
        logger.info(f"Total records: {validation_stats['total_records']}")
        logger.info(f"Fraud rate: {validation_stats['fraud_rate']:.2%}" if validation_stats['fraud_rate'] else "No fraud column")
        logger.info(f"Duplicate records: {validation_stats['duplicate_records']}")
        
        return validation_stats
    
    def get_data_summary(self) -> pd.DataFrame:
        """
        Get statistical summary of the data
        
        Returns:
            DataFrame with statistical summary
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        return self.df.describe(include='all')
    
    def get_feature_info(self) -> pd.DataFrame:
        """
        Get information about features
        
        Returns:
            DataFrame with feature information
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        feature_info = pd.DataFrame({
            'Feature': self.df.columns,
            'Type': self.df.dtypes.values,
            'Missing': self.df.isnull().sum().values,
            'Missing_Pct': (self.df.isnull().sum() / len(self.df) * 100).values,
            'Unique': [self.df[col].nunique() for col in self.df.columns]
        })
        
        return feature_info


if __name__ == "__main__":
    # Example usage
    loader = TransactionDataLoader("card_fraud.csv_processed.csv")
    df = loader.load_data()
    stats = loader.validate_data()
    
    print("\n=== Data Validation Statistics ===")
    for key, value in stats.items():
        if key not in ['missing_values', 'data_types']:
            print(f"{key}: {value}")
    
    print("\n=== Feature Information ===")
    print(loader.get_feature_info())
