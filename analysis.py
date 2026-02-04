import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Setup successful")

# Load data
sentiment = pd.read_csv("data/fear_greed_index_1.csv")
trader = pd.read_csv("data/historical_data_2.csv")


print("Sentiment shape:", sentiment.shape)
print("Trader shape:", trader.shape)

print("\nSentiment Columns:")
print(sentiment.columns)

print("\nTrader Columns:")
print(trader.columns)

# Convert sentiment date
sentiment['date'] = pd.to_datetime(sentiment['date']).dt.date

# Convert trader timestamp
trader['Timestamp IST'] = pd.to_datetime(trader['Timestamp IST'], dayfirst=True)
trader['date'] = trader['Timestamp IST'].dt.date


# Keep only needed columns
sentiment = sentiment[['date', 'classification']]

# Merge
df = trader.merge(sentiment, on='date', how='inner')

print("Merged shape:", df.shape)

# Data Quality Check
print("\nMissing Values in Trader:")
print(trader.isnull().sum())

print("\nDuplicate Rows in Trader:", trader.duplicated().sum())


#Real Work Started here

print("\nUnique Sentiment Types:")
print(df['classification'].unique())

# Create simplified sentiment
def simplify_sentiment(x):
    if "Fear" in x:
        return "Fear"
    elif "Greed" in x:
        return "Greed"
    else:
        return "Neutral"

df['sentiment_group'] = df['classification'].apply(simplify_sentiment)

print(df['sentiment_group'].value_counts())

#Fear vs Greed PnL compare
pnl_by_sentiment = df.groupby('sentiment_group')['Closed PnL'].mean()
print("\nAverage PnL by Sentiment:")
print(pnl_by_sentiment)
#Long vs Short Ratio
df['is_long'] = df['Side'] == 'BUY'

long_ratio = df.groupby('sentiment_group')['is_long'].mean()

print("\nLong Ratio by Sentiment:")
print(long_ratio)

#Trade Frequency
trades_per_day = df.groupby(['date','sentiment_group'])['Account'].count().reset_index()

avg_trades = trades_per_day.groupby('sentiment_group')['Account'].mean()

print("\nAverage Trades Per Day by Sentiment:")
print(avg_trades)

# Count trades per trader
trader_counts = df.groupby('Account')['Closed PnL'].count()

median_trades = trader_counts.median()

df['trader_segment'] = df['Account'].map(
    lambda x: "Frequent" if trader_counts[x] > median_trades else "Infrequent"
)

segment_perf = df.groupby(['trader_segment','sentiment_group'])['Closed PnL'].mean()

print("\nSegment Performance:")
print(segment_perf)

#checking Leverage Ahe ka 
print("\nStart Position Sample:")
print(df['Start Position'].head())

# Create size-based segment (risk proxy)
median_size = df['Size USD'].median()

df['size_segment'] = df['Size USD'].apply(
    lambda x: "High Size" if x > median_size else "Low Size"
)

size_perf = df.groupby(['size_segment','sentiment_group'])['Closed PnL'].mean()

print("\nSize Segment Performance:")
print(size_perf)

# ==============================
# WIN RATE
# ==============================

df['win'] = df['Closed PnL'] > 0

win_rate = df.groupby('sentiment_group')['win'].mean()

print("\nWin Rate by Sentiment:")
print(win_rate)


# ==============================
# DRAWDOWN PROXY (Volatility)
# ==============================

drawdown_proxy = df.groupby('sentiment_group')['Closed PnL'].std()

print("\nPnL Volatility (Drawdown Proxy):")
print(drawdown_proxy)


# ==============================
# CHARTS
# ==============================

import matplotlib.pyplot as plt

# 1️⃣ Avg PnL Chart
df.groupby('sentiment_group')['Closed PnL'].mean().plot(kind='bar')
plt.title("Average PnL by Sentiment")
plt.ylabel("Average PnL")
plt.show()

# 2️⃣ Trades per Day Chart
trades_per_day.groupby('sentiment_group')['Account'].mean().plot(kind='bar')
plt.title("Average Trades per Day")
plt.ylabel("Trades per Day")
plt.show()

# 3️⃣ Size Segment Performance Chart
df.groupby(['size_segment','sentiment_group'])['Closed PnL'].mean().unstack().plot(kind='bar')
plt.title("PnL by Size Segment & Sentiment")
plt.ylabel("Average PnL")
plt.show()