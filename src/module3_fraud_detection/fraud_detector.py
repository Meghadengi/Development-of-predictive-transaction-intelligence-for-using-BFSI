"""
Real-Time Fraud Detection Engine
Detects fraudulent transactions using trained models and rule-based systems
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import joblib
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FraudDetector:
    """Real-time fraud detection system"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize fraud detector
        
        Args:
            model_path: Path to trained model
        """
        self.model = None
        self.feature_engineer = None
        self.risk_rules = self._initialize_risk_rules()
        
        if model_path:
            self.load_model(model_path)
    
    def _initialize_risk_rules(self) -> Dict:
        """
        Initialize rule-based fraud detection rules
        
        Returns:
            Dictionary of risk rules
        """
        return {
            'high_amount_threshold': 75000000,  # 75M
            'velocity_threshold': 10,
            'distance_threshold': 500,  # km
            'time_gap_threshold': 1,  # minutes
            'night_transaction_risk': True,
            'weekend_risk_multiplier': 1.2
        }
    
    def load_model(self, model_path: str):
        """
        Load trained fraud detection model
        
        Args:
            model_path: Path to model file
        """
        try:
            self.model = joblib.load(model_path)
            logger.info(f"Model loaded from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def load_feature_engineer(self, engineer_path: str):
        """
        Load feature engineer
        
        Args:
            engineer_path: Path to feature engineer file
        """
        try:
            self.feature_engineer = joblib.load(engineer_path)
            logger.info(f"Feature engineer loaded from {engineer_path}")
        except Exception as e:
            logger.error(f"Failed to load feature engineer: {e}")
            raise
    
    def calculate_ml_risk_score(self, transaction: pd.DataFrame) -> float:
        """
        Calculate ML-based risk score
        
        Args:
            transaction: Transaction data
            
        Returns:
            Risk score (0-1)
        """
        if self.model is None:
            logger.warning("Model not loaded, returning default risk score")
            return 0.5
        
        try:
            # Get prediction probability
            if hasattr(self.model, 'predict_proba'):
                risk_score = self.model.predict_proba(transaction)[0, 1]
            else:
                risk_score = self.model.predict(transaction)[0]
            
            return float(risk_score)
        except Exception as e:
            logger.error(f"Error calculating ML risk score: {e}")
            return 0.5
    
    def calculate_rule_based_risk(self, transaction: Dict) -> Tuple[float, List[str]]:
        """
        Calculate rule-based risk score
        
        Args:
            transaction: Transaction data as dictionary
            
        Returns:
            Tuple of (risk_score, triggered_rules)
        """
        risk_score = 0.0
        triggered_rules = []
        
        # Rule 1: High transaction amount
        if transaction.get('Transaction_Amount', 0) > self.risk_rules['high_amount_threshold']:
            risk_score += 0.3
            triggered_rules.append("High transaction amount")
        
        # Rule 2: High velocity
        if transaction.get('Transaction_Velocity', 0) > self.risk_rules['velocity_threshold']:
            risk_score += 0.25
            triggered_rules.append("High transaction velocity")
        
        # Rule 3: Long distance
        if transaction.get('Distance_Between_Transactions_km', 0) > self.risk_rules['distance_threshold']:
            risk_score += 0.2
            triggered_rules.append("Unusual distance between transactions")
        
        # Rule 4: Quick succession
        if transaction.get('Time_Since_Last_Transaction_min', 999) < self.risk_rules['time_gap_threshold']:
            risk_score += 0.15
            triggered_rules.append("Rapid successive transactions")
        
        # Rule 5: Night transaction
        if self.risk_rules['night_transaction_risk']:
            hour = transaction.get('Hour', 12)
            if hour >= 22 or hour <= 6:
                risk_score += 0.1
                triggered_rules.append("Night time transaction")
        
        # Rule 6: Weekend transaction
        if transaction.get('Is_Weekend', 0) == 1:
            risk_score *= self.risk_rules['weekend_risk_multiplier']
            triggered_rules.append("Weekend transaction")
        
        # Rule 7: Failed authentication
        if transaction.get('Authentication_Method', '') == 'Failed':
            risk_score += 0.4
            triggered_rules.append("Failed authentication")
        
        # Normalize risk score to 0-1
        risk_score = min(risk_score, 1.0)
        
        return risk_score, triggered_rules
    
    def detect_fraud(self, transaction: pd.DataFrame, transaction_dict: Dict = None) -> Dict:
        """
        Detect fraud in a transaction
        
        Args:
            transaction: Transaction data as DataFrame
            transaction_dict: Transaction data as dictionary (for rule-based detection)
            
        Returns:
            Dictionary containing fraud detection results
        """
        # Calculate ML-based risk score
        ml_risk_score = self.calculate_ml_risk_score(transaction)
        
        # Calculate rule-based risk score
        if transaction_dict is None:
            transaction_dict = transaction.iloc[0].to_dict() if len(transaction) > 0 else {}
        
        rule_risk_score, triggered_rules = self.calculate_rule_based_risk(transaction_dict)
        
        # Combined risk score (weighted average)
        combined_risk_score = 0.7 * ml_risk_score + 0.3 * rule_risk_score
        
        # Determine fraud status
        is_fraud = combined_risk_score >= 0.5
        risk_level = self._get_risk_level(combined_risk_score)
        
        result = {
            'is_fraud': bool(is_fraud),
            'ml_risk_score': float(ml_risk_score),
            'rule_risk_score': float(rule_risk_score),
            'combined_risk_score': float(combined_risk_score),
            'risk_level': risk_level,
            'triggered_rules': triggered_rules,
            'timestamp': datetime.now().isoformat(),
            'recommendation': self._get_recommendation(combined_risk_score, triggered_rules)
        }
        
        return result
    
    def _get_risk_level(self, risk_score: float) -> str:
        """
        Get risk level based on score
        
        Args:
            risk_score: Risk score (0-1)
            
        Returns:
            Risk level string
        """
        if risk_score >= 0.7:
            return "HIGH"
        elif risk_score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_recommendation(self, risk_score: float, triggered_rules: List[str]) -> str:
        """
        Get recommendation based on risk assessment
        
        Args:
            risk_score: Combined risk score
            triggered_rules: List of triggered rules
            
        Returns:
            Recommendation string
        """
        if risk_score >= 0.7:
            return "BLOCK - High fraud risk detected. Manual review required."
        elif risk_score >= 0.5:
            return "REVIEW - Moderate fraud risk. Additional verification recommended."
        elif risk_score >= 0.3:
            return "MONITOR - Low-moderate risk. Continue monitoring."
        else:
            return "APPROVE - Low fraud risk. Transaction appears legitimate."
    
    def batch_detect(self, transactions: pd.DataFrame) -> List[Dict]:
        """
        Detect fraud in batch of transactions
        
        Args:
            transactions: DataFrame of transactions
            
        Returns:
            List of fraud detection results
        """
        results = []
        
        for idx, row in transactions.iterrows():
            transaction_df = pd.DataFrame([row])
            transaction_dict = row.to_dict()
            
            result = self.detect_fraud(transaction_df, transaction_dict)
            result['transaction_id'] = idx
            results.append(result)
        
        return results
    
    def generate_alert(self, detection_result: Dict, transaction_data: Dict) -> Dict:
        """
        Generate fraud alert
        
        Args:
            detection_result: Fraud detection result
            transaction_data: Original transaction data
            
        Returns:
            Alert dictionary
        """
        alert = {
            'alert_id': f"ALERT_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'timestamp': detection_result['timestamp'],
            'risk_level': detection_result['risk_level'],
            'risk_score': detection_result['combined_risk_score'],
            'is_fraud': detection_result['is_fraud'],
            'transaction_amount': transaction_data.get('Transaction_Amount'),
            'transaction_location': transaction_data.get('Transaction_Location'),
            'triggered_rules': detection_result['triggered_rules'],
            'recommendation': detection_result['recommendation'],
            'requires_action': detection_result['risk_level'] in ['HIGH', 'MEDIUM']
        }
        
        return alert
    
    def get_fraud_statistics(self, detection_results: List[Dict]) -> Dict:
        """
        Get statistics from fraud detection results
        
        Args:
            detection_results: List of detection results
            
        Returns:
            Dictionary with statistics
        """
        total = len(detection_results)
        fraud_count = sum(1 for r in detection_results if r['is_fraud'])
        
        risk_levels = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for result in detection_results:
            risk_levels[result['risk_level']] += 1
        
        avg_risk_score = np.mean([r['combined_risk_score'] for r in detection_results])
        
        stats = {
            'total_transactions': total,
            'fraud_detected': fraud_count,
            'fraud_rate': fraud_count / total if total > 0 else 0,
            'risk_distribution': risk_levels,
            'average_risk_score': float(avg_risk_score),
            'high_risk_count': risk_levels['HIGH'],
            'medium_risk_count': risk_levels['MEDIUM'],
            'low_risk_count': risk_levels['LOW']
        }
        
        return stats


class AnomalyDetector:
    """Detect anomalies in transaction patterns"""
    
    def __init__(self):
        """Initialize anomaly detector"""
        self.baseline_stats = {}
    
    def learn_baseline(self, transactions: pd.DataFrame):
        """
        Learn baseline statistics from normal transactions
        
        Args:
            transactions: DataFrame of normal transactions
        """
        logger.info("Learning baseline statistics...")
        
        numerical_cols = transactions.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            self.baseline_stats[col] = {
                'mean': transactions[col].mean(),
                'std': transactions[col].std(),
                'q1': transactions[col].quantile(0.25),
                'q3': transactions[col].quantile(0.75),
                'iqr': transactions[col].quantile(0.75) - transactions[col].quantile(0.25)
            }
        
        logger.info(f"Learned baseline for {len(self.baseline_stats)} features")
    
    def detect_anomalies(self, transaction: pd.Series) -> Tuple[bool, List[str]]:
        """
        Detect anomalies in a transaction
        
        Args:
            transaction: Transaction data
            
        Returns:
            Tuple of (is_anomaly, anomalous_features)
        """
        anomalous_features = []
        
        for col, stats in self.baseline_stats.items():
            if col not in transaction:
                continue
            
            value = transaction[col]
            
            # Z-score method
            z_score = abs((value - stats['mean']) / stats['std']) if stats['std'] > 0 else 0
            if z_score > 3:
                anomalous_features.append(f"{col} (z-score: {z_score:.2f})")
            
            # IQR method
            lower_bound = stats['q1'] - 1.5 * stats['iqr']
            upper_bound = stats['q3'] + 1.5 * stats['iqr']
            if value < lower_bound or value > upper_bound:
                if f"{col}" not in str(anomalous_features):
                    anomalous_features.append(f"{col} (outlier)")
        
        is_anomaly = len(anomalous_features) > 0
        
        return is_anomaly, anomalous_features


if __name__ == "__main__":
    logger.info("Fraud Detector module loaded successfully")
