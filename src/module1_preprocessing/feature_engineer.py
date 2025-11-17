"""
Feature Engineering for Transaction Data
Creates advanced features for fraud detection and prediction
"""
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler, LabelEncoder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Engineer features from transaction data"""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.feature_names = []
        
    def extract_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract time-based features from transaction date and time
        
        Args:
            df: DataFrame with transaction data
            
        Returns:
            DataFrame with additional time features
        """
        logger.info("Extracting time features...")
        
        df = df.copy()
        
        # Parse date and time
        if 'Transaction_Date' in df.columns:
            df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], errors='coerce')
            df['Day_of_Week'] = df['Transaction_Date'].dt.dayofweek
            df['Day_of_Month'] = df['Transaction_Date'].dt.day
            df['Month'] = df['Transaction_Date'].dt.month
            df['Is_Weekend'] = df['Day_of_Week'].isin([5, 6]).astype(int)
        
        if 'Transaction_Time' in df.columns:
            # Convert time to hour
            df['Hour'] = pd.to_datetime(df['Transaction_Time'], format='%H:%M:%S', errors='coerce').dt.hour
            df['Is_Night'] = df['Hour'].apply(lambda x: 1 if x >= 22 or x <= 6 else 0)
            df['Is_Business_Hours'] = df['Hour'].apply(lambda x: 1 if 9 <= x <= 17 else 0)
        
        logger.info(f"Created {len([c for c in df.columns if c not in ['Transaction_Date', 'Transaction_Time']])} time features")
        return df
    
    def create_aggregated_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create aggregated features based on transaction patterns
        
        Args:
            df: DataFrame with transaction data
            
        Returns:
            DataFrame with aggregated features
        """
        logger.info("Creating aggregated features...")
        
        df = df.copy()
        
        # Transaction amount statistics
        df['Amount_Zscore'] = (df['Transaction_Amount'] - df['Transaction_Amount'].mean()) / df['Transaction_Amount'].std()
        df['Amount_Percentile'] = df['Transaction_Amount'].rank(pct=True)
        
        # Velocity features
        if 'Transaction_Velocity' in df.columns:
            df['High_Velocity'] = (df['Transaction_Velocity'] > df['Transaction_Velocity'].quantile(0.75)).astype(int)
        
        # Distance features
        if 'Distance_Between_Transactions_km' in df.columns:
            df['Long_Distance'] = (df['Distance_Between_Transactions_km'] > df['Distance_Between_Transactions_km'].quantile(0.75)).astype(int)
        
        # Time since last transaction
        if 'Time_Since_Last_Transaction_min' in df.columns:
            df['Quick_Succession'] = (df['Time_Since_Last_Transaction_min'] < 5).astype(int)
            df['Time_Gap_Category'] = pd.cut(df['Time_Since_Last_Transaction_min'], 
                                             bins=[0, 5, 30, 60, 1440, np.inf],
                                             labels=['Very_Short', 'Short', 'Medium', 'Long', 'Very_Long'])
        
        logger.info("Aggregated features created")
        return df
    
    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create interaction features between existing features
        
        Args:
            df: DataFrame with transaction data
            
        Returns:
            DataFrame with interaction features
        """
        logger.info("Creating interaction features...")
        
        df = df.copy()
        
        # Amount and velocity interaction (already exists as Velocity_Distance_Interact)
        if 'Transaction_Amount' in df.columns and 'Transaction_Velocity' in df.columns:
            df['Amount_Velocity_Ratio'] = df['Transaction_Amount'] / (df['Transaction_Velocity'] + 1)
        
        # Amount and distance interaction
        if 'Transaction_Amount' in df.columns and 'Distance_Between_Transactions_km' in df.columns:
            df['Amount_Distance_Product'] = df['Transaction_Amount'] * df['Distance_Between_Transactions_km']
        
        # Previous transaction count and amount
        if 'Previous_Transaction_Count' in df.columns and 'Transaction_Amount' in df.columns:
            df['Amount_Per_Previous_Txn'] = df['Transaction_Amount'] / (df['Previous_Transaction_Count'] + 1)
        
        logger.info("Interaction features created")
        return df
    
    def encode_categorical_features(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        Encode categorical features
        
        Args:
            df: DataFrame with transaction data
            fit: Whether to fit encoders (True for training, False for inference)
            
        Returns:
            DataFrame with encoded categorical features
        """
        logger.info("Encoding categorical features...")
        
        df = df.copy()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Remove date/time columns if they exist
        categorical_cols = [col for col in categorical_cols if col not in ['Transaction_Date', 'Transaction_Time']]
        
        for col in categorical_cols:
            if fit:
                self.encoders[col] = LabelEncoder()
                df[f'{col}_Encoded'] = self.encoders[col].fit_transform(df[col].astype(str))
            else:
                if col in self.encoders:
                    # Handle unseen categories
                    df[f'{col}_Encoded'] = df[col].apply(
                        lambda x: self.encoders[col].transform([str(x)])[0] 
                        if str(x) in self.encoders[col].classes_ else -1
                    )
        
        logger.info(f"Encoded {len(categorical_cols)} categorical features")
        return df
    
    def scale_numerical_features(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        Scale numerical features
        
        Args:
            df: DataFrame with transaction data
            fit: Whether to fit scalers (True for training, False for inference)
            
        Returns:
            DataFrame with scaled numerical features
        """
        logger.info("Scaling numerical features...")
        
        df = df.copy()
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Exclude target and already scaled features
        exclude_cols = ['isFraud', 'Log_Transaction_Amount', 'Amount_Zscore']
        numerical_cols = [col for col in numerical_cols if col not in exclude_cols]
        
        if fit:
            self.scalers['standard'] = StandardScaler()
            df[numerical_cols] = self.scalers['standard'].fit_transform(df[numerical_cols])
        else:
            if 'standard' in self.scalers:
                df[numerical_cols] = self.scalers['standard'].transform(df[numerical_cols])
        
        logger.info(f"Scaled {len(numerical_cols)} numerical features")
        return df
    
    def create_risk_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create risk indicator features
        
        Args:
            df: DataFrame with transaction data
            
        Returns:
            DataFrame with risk indicators
        """
        logger.info("Creating risk indicators...")
        
        df = df.copy()
        
        # High amount flag
        if 'Transaction_Amount' in df.columns:
            amount_threshold = df['Transaction_Amount'].quantile(0.95)
            df['High_Amount_Flag'] = (df['Transaction_Amount'] > amount_threshold).astype(int)
        
        # Unusual location (high distance)
        if 'Distance_Between_Transactions_km' in df.columns:
            distance_threshold = df['Distance_Between_Transactions_km'].quantile(0.90)
            df['Unusual_Location_Flag'] = (df['Distance_Between_Transactions_km'] > distance_threshold).astype(int)
        
        # Rapid transactions
        if 'Time_Since_Last_Transaction_min' in df.columns:
            df['Rapid_Transaction_Flag'] = (df['Time_Since_Last_Transaction_min'] < 2).astype(int)
        
        # Combined risk score
        risk_cols = [col for col in df.columns if 'Flag' in col]
        if risk_cols:
            df['Risk_Score'] = df[risk_cols].sum(axis=1)
        
        logger.info("Risk indicators created")
        return df
    
    def engineer_all_features(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        Apply all feature engineering steps
        
        Args:
            df: DataFrame with transaction data
            fit: Whether to fit transformers (True for training, False for inference)
            
        Returns:
            DataFrame with all engineered features
        """
        logger.info("Starting feature engineering pipeline...")
        
        df = self.extract_time_features(df)
        df = self.create_aggregated_features(df)
        df = self.create_interaction_features(df)
        df = self.create_risk_indicators(df)
        df = self.encode_categorical_features(df, fit=fit)
        
        # Store feature names (excluding target)
        if fit:
            self.feature_names = [col for col in df.columns if col != 'isFraud']
        
        logger.info(f"Feature engineering completed. Total features: {len(df.columns)}")
        return df


if __name__ == "__main__":
    # Example usage
    from data_loader import TransactionDataLoader
    
    loader = TransactionDataLoader("card_fraud.csv_processed.csv")
    df = loader.load_data()
    
    engineer = FeatureEngineer()
    df_engineered = engineer.engineer_all_features(df, fit=True)
    
    print("\n=== Engineered Features ===")
    print(f"Original features: {len(loader.df.columns)}")
    print(f"Engineered features: {len(df_engineered.columns)}")
    print(f"\nNew features created: {len(df_engineered.columns) - len(loader.df.columns)}")
    print("\nSample of engineered data:")
    print(df_engineered.head())
