from abc import ABC, abstractmethod

class BaseBrokerAdapter(ABC):
    @abstractmethod
    def get_historical_data(self, symbol, timeframe):
        pass

    @abstractmethod
    def place_order(self, symbol, qty, side, order_type, price=None, trigger_price=None):
        pass

    @abstractmethod
    def get_position(self, symbol):
        pass

class DummyPaperBroker(BaseBrokerAdapter):
    """Paper trading aur backtesting ke liye simulated broker adapter."""
    def __init__(self, initial_capital=1000000.0):
        self.capital = initial_capital
        self.positions = {}

    def get_historical_data(self, symbol, timeframe):
        # CSV ya file se data load karne ke liye
        pass

    def place_order(self, symbol, qty, side, order_type, price=None, trigger_price=None):
        # Simulated order execution logic
        return {"status": "SUCCESS", "order_id": "ORD12345", "filled_price": price}

    def get_position(self, symbol):
        return self.positions.get(symbol, {"qty": 0, "avg_price": 0.0})