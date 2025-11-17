"""
Unit tests for preprocessing module
"""
import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.module1_preprocessing.data_loader import TransactionDataLoader
from src.module1_preprocessing.feature_engineer import FeatureEngineer


class TestDataLoader:
    """Test data loader functionality"""
    
    def test_load_data(self):
        """Test data loading"""
        # Create sample data
        sample_data = pd.DataFrame({
            'Transaction_Amount': [10000, 20000, 30000],
            'isFraud': [0, 1, 0]
        })
        
        # Save to temp file
        temp_file = Path(__file__).parent / "temp_data.csv"
        sample_data.to_csv(temp_file, index=False)
        
        # Load data
        loader = TransactionDataLoader(str(temp_file))
        df = loader.load_data()
        
        assert len(df) == 3
        assert 'Transaction_Amount' in df.columns
        assert 'isFraud' in df.columns
        
        # Cleanup
        temp_file.unlink()
    
    def test_validate_data(self):
        """Test data validation"""
        sample_data = pd.DataFrame({
            'Transaction_Amount': [10000, 20000, 30000],
            'isFraud': [0, 1, 0]
        })
        
        temp_file = Path(__file__).parent / "temp_data.csv"
        sample_data.to_csv(temp_file, index=False)
        
        loader = TransactionDataLoader(str(temp_file))
        loader.load_data()
        stats = loader.validate_data()
        
        assert stats['total_records'] == 3
        assert stats['fraud_rate'] is not None
        
        temp_file.unlink()


class TestFeatureEngineer:
    """Test feature engineering"""
    
    def test_extract_time_features(self):
        """Test time feature extraction"""
        df = pd.DataFrame({
            'Transaction_Date': ['2024-01-15', '2024-01-16'],
            'Transaction_Time': ['14:30:00', '09:15:00'],
            'Transaction_Amount': [10000, 20000]
        })
        
        engineer = FeatureEngineer()
        df_engineered = engineer.extract_time_features(df)
        
        assert 'Day_of_Week' in df_engineered.columns
        assert 'Hour' in df_engineered.columns
        assert 'Is_Weekend' in df_engineered.columns
    
    def test_create_aggregated_features(self):
        """Test aggregated feature creation"""
        df = pd.DataFrame({
            'Transaction_Amount': [10000, 50000, 90000],
            'Transaction_Velocity': [1, 5, 10],
            'Distance_Between_Transactions_km': [5, 50, 500]
        })
        
        engineer = FeatureEngineer()
        df_engineered = engineer.create_aggregated_features(df)
        
        assert 'Amount_Zscore' in df_engineered.columns
        assert 'High_Velocity' in df_engineered.columns
        assert 'Long_Distance' in df_engineered.columns


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
