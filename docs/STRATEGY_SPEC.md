# Deteroid Technologies LLP - Strategy Specifications

## Strategy A: Advanced Options Scalping
- **Timeframe:** 2-Minute Intraday Charts.
- **Indicators:** SMA 20 (High & Low), MACD (12, 26, 9).
- **Entry Rules:**
  - MACD bullish/bearish crossover confirmation.
  - Price action touch with SMA 20 High/Low (50%-70% candle body touch).
- **Exit Rules:** 
  - Partial exit at 1:1 Risk-Reward ratio, trailing stop loss on remaining quantity.
- **Assumptions:** 
  - Exact tick data is simulated via synthetic/historical price bars due to lack of paid broker websocket feeds.

## Strategy B: Multi-EMA Indicator-Based Rules
- **Timeframe:** 5-Minute / 30-Minute flexible intraday.
- **Indicators:** 11 Exponential Moving Averages (3, 5, 8, 12, 15, 30, 35, 40, 45, 50, 60) and WMA 6 (Violet/Black line).
- **Entry Rules:** 
  - Fast EMAs align above/below slow EMAs with WMA 6 confirmation.
- **Exit Rules:** 
  - Opposite cross or major trend breakdown.