import pandas as pd

df = pd.read_csv('card_fraud.csv_processed.csv')
print(df['isFraud'].value_counts())
print(f'\nFraud rate: {df["isFraud"].mean() * 100:.2f}%')
