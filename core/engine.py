import pandas as pd

class EventDrivenBacktestEngine:
    def __init__(self, strategy, initial_capital=1000000.0):
        self.strategy = strategy
        self.capital = initial_capital
        self.trades = []

    def run_backtest(self, df: pd.DataFrame):
        signals_df = self.strategy.generate_signals(df)
        position = 0
        entry_price = 0.0
        
        for i in range(len(signals_df)):
            row = signals_df.iloc[i]
            sig = row['signal']
            price = row['close']
            
            if position == 0 and sig != 0:
                position = sig
                entry_price = price
                self.trades.append({
                    'index': i,
                    'type': 'BUY' if sig == 1 else 'SELL',
                    'entry_price': entry_price
                })
            elif position != 0:
                # Exit condition: 1:1 or opposite signal or simple exit after few bars
                if sig == -position or i == len(signals_df) - 1:
                    pnl = (price - entry_price) if position == 1 else (entry_price - price)
                    self.trades[-1]['exit_price'] = price
                    self.trades[-1]['pnl'] = pnl
                    position = 0
                    
        return pd.DataFrame(self.trades)