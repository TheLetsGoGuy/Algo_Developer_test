# Edge Cases & Risk Management Documentation

1. **Repainting Prevention:** 
   - All indicators (EMA, SMA, MACD) are calculated strictly on closed candles (`closed` bar values) to avoid lookahead bias and repainting during live backtesting.
2. **Market Gaps & Slippage:** 
   - Engine accounts for a default slippage buffer and transaction costs (brokerage + STT) on every simulated trade execution.
3. **Disconnect & Reconnect Safety:** 
   - State machine tracks positions persistently (`FLAT`, `IN_POSITION`, `PARTIAL_EXIT`). If the script crashes or restarts, it fetches active positions before placing new orders.
4. **Lot Size & Risk Limits:** 
   - Strict stop-loss protection prevents runaway losses during high volatility.