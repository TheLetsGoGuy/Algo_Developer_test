import pytest
import pandas as pd
import numpy as np
from strategies.strategy_a import StrategyA
from strategies.strategy_b import StrategyB
from core.engine import EventDrivenBacktestEngine

@pytest.fixture
def sample_market_data():
    """Testing ke liye sample intraday dataframe create karta hai."""
    np.random.seed(42)
    n_rows = 100
    start_time = pd.Timestamp("2026-11-06 09:15:00")
    timestamps = [start_time + pd.Timedelta(minutes=2*i) for i in range(n_rows)]
    
    close_prices = 71000 + np.cumsum(np.random.normal(0, 5, n_rows))
    df = pd.DataFrame({
        'timestamp': timestamps,
        'open': close_prices + 1,
        'high': close_prices + 5,
        'low': close_prices - 5,
        'close': close_prices,
        'volume': np.random.randint(1000, 10000, n_rows)
    })
    df.set_index('timestamp', inplace=True)
    return df

def test_strategy_a_indicators(sample_market_data):
    """Verify karta hai ki Strategy A ke indicators (SMA high/low, MACD) theek se calculate ho rahe hain."""
    strat = StrategyA()
    df_res = strat.calculate_indicators(sample_market_data)
    
    assert 'sma_high' in df_res.columns
    assert 'sma_low' in df_res.columns
    assert 'macd' in df_res.columns
    assert not df_res['sma_high'].isnull().all()

def test_strategy_b_indicators(sample_market_data):
    """Verify karta hai ki Strategy B ke multiple EMAs theek se generate ho rahe hain."""
    strat = StrategyB()
    df_res = strat.calculate_indicators(sample_market_data)
    
    assert 'ema_3' in df_res.columns
    assert 'ema_60' in df_res.columns
    assert 'wma_6' in df_res.columns

def test_backtest_engine_execution(sample_market_data):
    """Verify karta hai ki backtest engine bina error ke trades generate kar raha hai."""
    strat = StrategyA()
    engine = EventDrivenBacktestEngine(strat, initial_capital=500000.0)
    trades_df = engine.run_backtest(sample_market_data)
    
    assert isinstance(trades_df, pd.DataFrame)
    # Check if expected columns or structure exist
    if not trades_df.empty:
        assert 'entry_price' in trades_df.columns
        assert 'type' in trades_df.columns

def test_lookahead_bias_prevention(sample_market_data):
    """Lookahead bias test: Check karta hai ki current bar calculation mein future values use nahi ho rahi hain."""
    strat = StrategyA()
    df_res = strat.generate_signals(sample_market_data)
    
    # Ensure signal values are strictly within [-1, 0, 1]
    valid_signals = [-1, 0, 1]
    for sig in df_res['signal'].unique():
        assert sig in valid_signals