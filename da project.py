# ================================
# Finance Risk & Volatility Project
# ================================

# Fix for graph display
import matplotlib
matplotlib.use('TkAgg')

# Step 1: Import Libraries
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Step 2: Download Stock Data
stocks = ['AAPL', 'MSFT', 'GOOG', 'TSLA']

data = yf.download(stocks, start="2020-01-01", end="2024-01-01")

# FIX: Handle new yfinance format
if isinstance(data.columns, pd.MultiIndex):
    data = data['Close']

print("\nStock Data:\n", data.head())

# Step 3: Calculate Daily Returns
returns = data.pct_change().dropna()
print("\nDaily Returns:\n", returns.head())

# Step 4: Calculate Volatility (Risk)
volatility = returns.std()
print("\nVolatility (Risk):\n", volatility)

# Step 5: Plot Stock Prices
data.plot(title="Stock Price Trends")
plt.savefig("fig1_stock_prices.png")
plt.show()

# Step 6: Correlation Heatmap
plt.figure()
sns.heatmap(returns.corr(), annot=True)
plt.title("Stock Correlation Heatmap")
plt.savefig("fig2_heatmap.png")
plt.show()

# Step 7: Value at Risk (VaR)
print("\nValue at Risk (5%):")
for stock in stocks:
    var = np.percentile(returns[stock], 5)
    print(f"{stock}: {var}")

# Step 8: Monte Carlo Simulation (AAPL)
simulations = 1000
days = 252

last_price = data['AAPL'].iloc[-1]
results = []

for i in range(simulations):
    prices = [last_price]
    for j in range(days):
        price = prices[-1] * (1 + np.random.normal(returns['AAPL'].mean(), returns['AAPL'].std()))
        prices.append(price)
    results.append(prices)

# Plot cleaner simulation (only 50 lines)
plt.figure()
for i in range(50):
    plt.plot(results[i])

plt.title("Monte Carlo Simulation (AAPL)")
plt.xlabel("Days")
plt.ylabel("Price")
plt.savefig("fig3_simulation.png")
plt.show()

# ================================
# 🔥 CSV SAVE FIX (IMPORTANT)
# ================================

# Save CSV in SAME folder as your file
script_dir = os.path.dirname(os.path.abspath(__file__))
data.to_csv(os.path.join(script_dir, "stock_prices.csv"))
returns.to_csv(os.path.join(script_dir, "returns.csv"))

print("\n✅ CSV files saved successfully!")
print(f"📁 Check your folder: {script_dir}")