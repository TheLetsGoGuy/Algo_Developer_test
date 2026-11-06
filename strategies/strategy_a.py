import pandas as pd
import numpy as np

class StrategyA:
    def __init__(self):
        self.name = "Strategy_A_Advanced_Options"

    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        # SMA 20 High & Low
        df['sma_high'] = df['high'].rolling(window=20).mean()
        df['sma_low'] = df['low'].rolling(window=20).mean()
        
        # MACD (12, 26, 9)
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.calculate_indicators(df)
        df['signal'] = 0  # 1: Buy (Call), -1: Sell (Put), 0: No Signal
        
        for i in range(21, len(df)):
            # Time filter simulation (e.g., trading hours check can be added via timestamp)
            macd_val = df['macd'].iloc[i]
            macd_sig = df['macd_signal'].iloc[i]
            close_val = df['close'].iloc[i]
            sma_h = df['sma_high'].iloc[i]
            sma_l = df['sma_low'].iloc[i]
            
            # Bullish Crossover & Body Touch Condition
            if macd_val > macd_sig and close_val >= sma_l:
                df.loc[df.index[i], 'signal'] = 1
            # Bearish Crossover Condition
            elif macd_val < macd_sig and close_val <= sma_h:
                df.loc[df.index[i], 'signal'] = -1
                
        return df