# Trader Sentiment Analysis

## Project Overview

This project analyzes trader performance under different market sentiment conditions (Fear, Greed, Neutral).

The goal is to understand:
- How sentiment affects profitability (PnL)
- Whether traders change behavior during Fear vs Greed
- Which trader segments perform better under specific conditions

---

## Dataset

1. Fear & Greed Index dataset (daily sentiment)
2. Historical trader data (trade-level information)

Total trades analyzed: 211,218

---

## Part A — Data Preparation

- Loaded both datasets
- Checked missing values and duplicates (none found)
- Converted timestamps to datetime
- Merged datasets on daily date
- Created key metrics:
  - Average PnL
  - Win rate
  - Long/Short ratio
  - Trade frequency
  - Size segmentation

---

## Part B — Key Insights

### 1️⃣ Performance by Sentiment
- Greed days show highest average PnL
- Fear days slightly lower but stable
- Neutral days lowest performance

### 2️⃣ Behavior Changes
- Traders trade more frequently during Fear days
- Slight long bias during Neutral days
- Win rate highest during Greed days

### 3️⃣ Segment Analysis
- Infrequent traders perform extremely well during Greed
- High-size traders outperform low-size traders significantly
- Volatility (risk proxy) higher during Fear and Greed

---

## Part C — Strategy Recommendations

1. During Greed days:
   - Increase position size selectively
   - Focus on high-performing segments

2. During Fear days:
   - Maintain moderate exposure
   - Avoid excessive leverage due to volatility

---
