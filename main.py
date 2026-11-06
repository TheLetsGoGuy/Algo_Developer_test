import os
import pandas as pd
import numpy as np
from strategies.strategy_a import StrategyA
from strategies.strategy_b import StrategyB
from core.engine import EventDrivenBacktestEngine

def generate_synthetic_data(n_rows=500):
    """Bina broker API ya historical CSV ke test karne ke liye synthetic intraday data generator."""
    np.random.seed(42)
    start_time = pd.Timestamp("2026-11-06 09:15:00")
    # 2-minute interval timestamps for intraday trading
    timestamps = [start_time + pd.Timedelta(minutes=2*i) for i in range(n_rows)]
    
    # Random walk price generation starting around 71000 (like SENSEX/NIFTY options)
    price_changes = np.random.normal(loc=0.0, scale=15.0, size=n_rows)
    close_prices = 71000 + np.cumsum(price_changes)
    
    high_prices = close_prices + np.random.uniform(2, 10, size=n_rows)
    low_prices = close_prices - np.random.uniform(2, 10, size=n_rows)
    open_prices = close_prices + np.random.normal(loc=0.0, scale=5.0, size=n_rows)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        'volume': np.random.randint(1000, 50000, size=n_rows)
    })
    df.set_index('timestamp', inplace=True)
    return df

def main():
    print("--- Deteroid AlgoDesk Assessment Pipeline Starting ---")
    
    # 1. Load or generate historical data
    print("Generating synthetic historical market data...")
    df = generate_synthetic_data(n_rows=600)
    
    # Ensure data/ folder exists
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/market_data.csv')
    
    # 2. Run Strategy A (Advanced Options Scalping)
    print("\nRunning Strategy A (Advanced Options)...")
    strat_a = StrategyA()
    engine_a = EventDrivenBacktestEngine(strat_a)
    trades_a = engine_a.run_backtest(df)
    
    os.makedirs('reports', exist_ok=True)
    trades_a.to_csv('reports/strategy_a_signals.csv', index=False)
    print(f"Strategy A executed. Total Trades Generated: {len(trades_a)}")
    print(trades_a.head())

    # 3. Run Strategy B (Multi-EMA Indicator-based)
    print("\nRunning Strategy B (Multi-EMA)...")
    strat_b = StrategyB()
    engine_b = EventDrivenBacktestEngine(strat_b)
    trades_b = engine_b.run_backtest(df)
    
    trades_b.to_csv('reports/strategy_b_signals.csv', index=False)
    print(f"Strategy B executed. Total Trades Generated: {len(trades_b)}")
    print(trades_b.head())
    
    print("\n--- Pipeline Completed Successfully! Signal CSVs saved in 'reports/' folder ---")

if __name__ == "__main__":
    main()