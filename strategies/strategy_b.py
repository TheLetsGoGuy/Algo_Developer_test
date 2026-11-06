import pandas as pd

class StrategyB:
    def __init__(self):
        self.name = "Strategy_B_Multi_EMA"
        self.emas = [3, 5, 8, 12, 15, 30, 35, 40, 45, 50, 60]

    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        for period in self.emas:
            df[f'ema_{period}'] = df['close'].ewm(span=period, adjust=False).mean()
        # WMA / BWMMA proxy for trend confirmation
        df['wma_6'] = df['close'].rolling(window=6).mean()
        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.calculate_indicators(df)
        df['signal'] = 0
        
        for i in range(61, len(df)):
            # Check alignment of fast EMAs vs slow EMAs
            fast_ema = df['ema_3'].iloc[i]
            slow_ema = df['ema_60'].iloc[i]
            
            if fast_ema > slow_ema and df['wma_6'].iloc[i] > slow_ema:
                df.loc[df.index[i], 'signal'] = 1
            elif fast_ema < slow_ema and df['wma_6'].iloc[i] < slow_ema:
                df.loc[df.index[i], 'signal'] = -1
                
        return df