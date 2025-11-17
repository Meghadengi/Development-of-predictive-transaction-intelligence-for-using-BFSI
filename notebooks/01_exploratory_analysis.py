"""
Exploratory Data Analysis
Analyze transaction data and visualize patterns
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config.config import *

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def load_data():
    """Load the dataset"""
    print("Loading data...")
    df = pd.read_csv(Path(__file__).parent.parent / "card_fraud.csv_processed.csv")
    print(f"Loaded {len(df)} transactions")
    return df


def basic_statistics(df):
    """Display basic statistics"""
    print("\n" + "="*50)
    print("BASIC STATISTICS")
    print("="*50)
    
    print(f"\nDataset Shape: {df.shape}")
    print(f"Number of Features: {df.shape[1]}")
    print(f"Number of Transactions: {df.shape[0]}")
    
    print("\nFraud Distribution:")
    print(df['isFraud'].value_counts())
    print(f"\nFraud Rate: {df['isFraud'].mean():.2%}")
    
    print("\nNumerical Features Summary:")
    print(df.describe())


def analyze_fraud_patterns(df):
    """Analyze fraud patterns"""
    print("\n" + "="*50)
    print("FRAUD PATTERN ANALYSIS")
    print("="*50)
    
    fraud_df = df[df['isFraud'] == 1]
    normal_df = df[df['isFraud'] == 0]
    
    print("\nTransaction Amount Comparison:")
    print(f"Fraud - Mean: {fraud_df['Transaction_Amount'].mean():.2f}, Median: {fraud_df['Transaction_Amount'].median():.2f}")
    print(f"Normal - Mean: {normal_df['Transaction_Amount'].mean():.2f}, Median: {normal_df['Transaction_Amount'].median():.2f}")
    
    print("\nTransaction Velocity Comparison:")
    print(f"Fraud - Mean: {fraud_df['Transaction_Velocity'].mean():.2f}")
    print(f"Normal - Mean: {normal_df['Transaction_Velocity'].mean():.2f}")
    
    print("\nDistance Comparison:")
    print(f"Fraud - Mean: {fraud_df['Distance_Between_Transactions_km'].mean():.2f} km")
    print(f"Normal - Mean: {normal_df['Distance_Between_Transactions_km'].mean():.2f} km")


def plot_distributions(df):
    """Plot feature distributions"""
    print("\n" + "="*50)
    print("GENERATING VISUALIZATIONS")
    print("="*50)
    
    # Create output directory
    output_dir = Path(__file__).parent / "figures"
    output_dir.mkdir(exist_ok=True)
    
    # 1. Fraud distribution
    plt.figure(figsize=(8, 6))
    df['isFraud'].value_counts().plot(kind='bar', color=['green', 'red'])
    plt.title('Fraud vs Normal Transactions', fontsize=14, fontweight='bold')
    plt.xlabel('Transaction Type (0=Normal, 1=Fraud)')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_dir / 'fraud_distribution.png', dpi=300)
    print(f"✓ Saved: fraud_distribution.png")
    plt.close()
    
    # 2. Transaction amount distribution
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    axes[0].hist(df[df['isFraud']==0]['Transaction_Amount'], bins=50, alpha=0.7, label='Normal', color='green')
    axes[0].hist(df[df['isFraud']==1]['Transaction_Amount'], bins=50, alpha=0.7, label='Fraud', color='red')
    axes[0].set_xlabel('Transaction Amount')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Transaction Amount Distribution')
    axes[0].legend()
    
    axes[1].boxplot([df[df['isFraud']==0]['Transaction_Amount'], 
                     df[df['isFraud']==1]['Transaction_Amount']],
                    labels=['Normal', 'Fraud'])
    axes[1].set_ylabel('Transaction Amount')
    axes[1].set_title('Transaction Amount by Type')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'amount_distribution.png', dpi=300)
    print(f"✓ Saved: amount_distribution.png")
    plt.close()
    
    # 3. Velocity and Distance
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    axes[0].scatter(df[df['isFraud']==0]['Transaction_Velocity'], 
                   df[df['isFraud']==0]['Distance_Between_Transactions_km'],
                   alpha=0.3, label='Normal', color='green', s=10)
    axes[0].scatter(df[df['isFraud']==1]['Transaction_Velocity'], 
                   df[df['isFraud']==1]['Distance_Between_Transactions_km'],
                   alpha=0.5, label='Fraud', color='red', s=10)
    axes[0].set_xlabel('Transaction Velocity')
    axes[0].set_ylabel('Distance (km)')
    axes[0].set_title('Velocity vs Distance')
    axes[0].legend()
    
    axes[1].hist(df[df['isFraud']==0]['Transaction_Velocity'], bins=30, alpha=0.7, label='Normal', color='green')
    axes[1].hist(df[df['isFraud']==1]['Transaction_Velocity'], bins=30, alpha=0.7, label='Fraud', color='red')
    axes[1].set_xlabel('Transaction Velocity')
    axes[1].set_ylabel('Frequency')
    axes[1].set_title('Transaction Velocity Distribution')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'velocity_distance.png', dpi=300)
    print(f"✓ Saved: velocity_distance.png")
    plt.close()
    
    # 4. Correlation heatmap
    plt.figure(figsize=(12, 10))
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    correlation = df[numerical_cols].corr()
    sns.heatmap(correlation, annot=False, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5)
    plt.title('Feature Correlation Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'correlation_heatmap.png', dpi=300)
    print(f"✓ Saved: correlation_heatmap.png")
    plt.close()
    
    print(f"\nAll visualizations saved to: {output_dir}")


def categorical_analysis(df):
    """Analyze categorical features"""
    print("\n" + "="*50)
    print("CATEGORICAL FEATURE ANALYSIS")
    print("="*50)
    
    categorical_cols = ['Card_Type', 'Transaction_Category', 'Authentication_Method', 'Transaction_Status']
    
    for col in categorical_cols:
        if col in df.columns:
            print(f"\n{col}:")
            fraud_rate = df.groupby(col)['isFraud'].mean()
            print(fraud_rate.sort_values(ascending=False))


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("EXPLORATORY DATA ANALYSIS")
    print("Predictive Transaction Intelligence for BFSI")
    print("="*70)
    
    # Load data
    df = load_data()
    
    # Basic statistics
    basic_statistics(df)
    
    # Fraud pattern analysis
    analyze_fraud_patterns(df)
    
    # Categorical analysis
    categorical_analysis(df)
    
    # Generate visualizations
    plot_distributions(df)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETED")
    print("="*70)


if __name__ == "__main__":
    main()
