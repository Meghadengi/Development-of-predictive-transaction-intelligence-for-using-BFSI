import pandas as pd

# Load the dataset
df = pd.read_csv('card_fraud.csv_processed.csv')

print('Shape:', df.shape)
print('\nColumns:', df.columns.tolist())
print('\nFirst few rows:')
print(df.head())
print('\nData types:')
print(df.dtypes)
print('\nBasic statistics:')
print(df.describe())

# Check for fraud column
if 'fraud' in df.columns:
    print('\nFraud distribution:')
    print(df['fraud'].value_counts())
    print(f'\nFraud percentage: {df["fraud"].mean() * 100:.2f}%')
else:
    print('\nLooking for fraud-related columns:')
    fraud_cols = [col for col in df.columns if 'fraud' in col.lower()]
    print(fraud_cols)

print('\nMissing values:')
print(df.isnull().sum())
