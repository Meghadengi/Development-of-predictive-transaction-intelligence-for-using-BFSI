"""
LLM-based Transaction Embeddings
Uses transformer models to create contextual embeddings of transaction data
"""
import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransactionEmbedder:
    """Create LLM embeddings for transaction data"""
    
    def __init__(self, model_name: str = "distilbert-base-uncased"):
        """
        Initialize transaction embedder
        
        Args:
            model_name: Name of the transformer model to use
        """
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        logger.info(f"Loading model: {model_name}")
        logger.info(f"Using device: {self.device}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load transformer model: {e}")
            logger.warning("Embeddings will use fallback method")
            self.tokenizer = None
            self.model = None
    
    def create_transaction_text(self, row: pd.Series) -> str:
        """
        Create text representation of a transaction
        
        Args:
            row: Transaction data row
            
        Returns:
            Text description of the transaction
        """
        text_parts = []
        
        # Amount
        if 'Transaction_Amount' in row:
            text_parts.append(f"amount {row['Transaction_Amount']}")
        
        # Location
        if 'Transaction_Location' in row:
            text_parts.append(f"at {row['Transaction_Location']}")
        
        # Card type
        if 'Card_Type' in row:
            text_parts.append(f"using {row['Card_Type']} card")
        
        # Category
        if 'Transaction_Category' in row:
            text_parts.append(f"for {row['Transaction_Category']}")
        
        # Time information
        if 'Hour' in row:
            text_parts.append(f"at hour {row['Hour']}")
        
        # Velocity
        if 'Transaction_Velocity' in row:
            text_parts.append(f"velocity {row['Transaction_Velocity']}")
        
        # Distance
        if 'Distance_Between_Transactions_km' in row:
            text_parts.append(f"distance {row['Distance_Between_Transactions_km']} km")
        
        return " ".join(text_parts)
    
    def get_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Get embeddings for transaction texts
        
        Args:
            texts: List of transaction text descriptions
            batch_size: Batch size for processing
            
        Returns:
            Array of embeddings
        """
        if self.model is None or self.tokenizer is None:
            logger.warning("Using fallback embeddings (hash-based)")
            return self._fallback_embeddings(texts)
        
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            
            # Tokenize
            inputs = self.tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=128,
                return_tensors="pt"
            )
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Use [CLS] token embedding
                batch_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
            
            embeddings.append(batch_embeddings)
        
        return np.vstack(embeddings)
    
    def _fallback_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Fallback method for creating embeddings without transformer model
        
        Args:
            texts: List of transaction text descriptions
            
        Returns:
            Array of simple hash-based embeddings
        """
        embeddings = []
        
        for text in texts:
            # Simple hash-based embedding
            words = text.split()
            embedding = np.zeros(128)
            
            for i, word in enumerate(words[:128]):
                embedding[i % 128] += hash(word) % 1000 / 1000.0
            
            embeddings.append(embedding)
        
        return np.array(embeddings)
    
    def embed_dataframe(self, df: pd.DataFrame, batch_size: int = 32) -> np.ndarray:
        """
        Create embeddings for entire dataframe
        
        Args:
            df: DataFrame with transaction data
            batch_size: Batch size for processing
            
        Returns:
            Array of embeddings
        """
        logger.info(f"Creating embeddings for {len(df)} transactions...")
        
        # Create text representations
        texts = [self.create_transaction_text(row) for _, row in df.iterrows()]
        
        # Get embeddings
        embeddings = self.get_embeddings(texts, batch_size=batch_size)
        
        logger.info(f"Created embeddings with shape {embeddings.shape}")
        
        return embeddings
    
    def add_embeddings_to_dataframe(self, df: pd.DataFrame, batch_size: int = 32) -> pd.DataFrame:
        """
        Add embedding features to dataframe
        
        Args:
            df: DataFrame with transaction data
            batch_size: Batch size for processing
            
        Returns:
            DataFrame with additional embedding columns
        """
        embeddings = self.embed_dataframe(df, batch_size=batch_size)
        
        # Add embeddings as new columns
        df_copy = df.copy()
        for i in range(embeddings.shape[1]):
            df_copy[f'embedding_{i}'] = embeddings[:, i]
        
        logger.info(f"Added {embeddings.shape[1]} embedding features")
        
        return df_copy


class TransactionSequenceAnalyzer:
    """Analyze sequences of transactions for pattern detection"""
    
    def __init__(self):
        """Initialize sequence analyzer"""
        self.sequence_patterns = {}
    
    def extract_sequences(self, df: pd.DataFrame, customer_id_col: str = None, 
                         sequence_length: int = 5) -> List[List[Dict]]:
        """
        Extract transaction sequences
        
        Args:
            df: DataFrame with transaction data
            customer_id_col: Column name for customer ID (if available)
            sequence_length: Length of sequences to extract
            
        Returns:
            List of transaction sequences
        """
        if customer_id_col and customer_id_col in df.columns:
            # Group by customer
            sequences = []
            for customer_id, group in df.groupby(customer_id_col):
                group = group.sort_values('Transaction_Date')
                for i in range(len(group) - sequence_length + 1):
                    seq = group.iloc[i:i+sequence_length].to_dict('records')
                    sequences.append(seq)
        else:
            # Create sequences from sorted data
            df_sorted = df.sort_values('Transaction_Date') if 'Transaction_Date' in df.columns else df
            sequences = []
            for i in range(len(df_sorted) - sequence_length + 1):
                seq = df_sorted.iloc[i:i+sequence_length].to_dict('records')
                sequences.append(seq)
        
        return sequences
    
    def analyze_patterns(self, sequences: List[List[Dict]]) -> Dict:
        """
        Analyze patterns in transaction sequences
        
        Args:
            sequences: List of transaction sequences
            
        Returns:
            Dictionary with pattern analysis
        """
        patterns = {
            'avg_sequence_amount': [],
            'amount_variance': [],
            'location_changes': [],
            'time_gaps': []
        }
        
        for seq in sequences:
            amounts = [t.get('Transaction_Amount', 0) for t in seq]
            patterns['avg_sequence_amount'].append(np.mean(amounts))
            patterns['amount_variance'].append(np.var(amounts))
            
            locations = [t.get('Transaction_Location', '') for t in seq]
            patterns['location_changes'].append(len(set(locations)))
        
        return {
            'avg_amount_per_sequence': np.mean(patterns['avg_sequence_amount']),
            'avg_amount_variance': np.mean(patterns['amount_variance']),
            'avg_location_changes': np.mean(patterns['location_changes']),
            'total_sequences': len(sequences)
        }


if __name__ == "__main__":
    logger.info("LLM Embeddings module loaded successfully")
    
    # Example usage
    embedder = TransactionEmbedder()
    
    # Test with sample transaction
    sample_transaction = pd.Series({
        'Transaction_Amount': 50000,
        'Transaction_Location': 'Mumbai',
        'Card_Type': 'Visa',
        'Transaction_Category': 'Shopping',
        'Hour': 14,
        'Transaction_Velocity': 5,
        'Distance_Between_Transactions_km': 10.5
    })
    
    text = embedder.create_transaction_text(sample_transaction)
    print(f"\nSample transaction text: {text}")
