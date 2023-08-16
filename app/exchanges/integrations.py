import ccxt
from abc import ABC, abstractmethod
from app.db.models import PlaceOrderBase

class AbstractExchange(ABC):

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    @staticmethod
    def create(name: str, api_key: str, api_secret: str) -> "AbstractExchange":
        if name == "bitget":
            return BitgetExchange(api_key, api_secret)
        elif name == "bybit":
            return BybitExchange(api_key, api_secret)
        else:
            raise ValueError(f"Unsupported exchange: {name}")    

    @abstractmethod
    def place_order(self, order:PlaceOrderBase) -> dict:
        pass

    @abstractmethod
    def get_balance(self) -> dict:
        pass

    @abstractmethod
    def set_leverage(self, leverage: int) -> dict:
        pass

class BitgetExchange(AbstractExchange):
    def __init__(self, api_key: str, api_secret: str):
        super().__init__(api_key, api_secret)
        self.exchange = ccxt.bitget({
            'apiKey': self.api_key,
            'secret': self.api_secret,
        })

    def place_order(self, order: PlaceOrderBase) -> dict:
        # Implement the method using ccxt's functions for Bitget
        pass

    def get_balance(self) -> dict:
        # Implement the method using ccxt's functions for Bitget
        pass

    def set_leverage(self, leverage: int) -> dict:
        # Implement the method using ccxt's functions for Bitget
        pass

class BybitExchange(AbstractExchange):
    def __init__(self, api_key: str, api_secret: str):
        super().__init__(api_key, api_secret)
        self.exchange = ccxt.bybit({
            'apiKey': self.api_key,
            'secret': self.api_secret,
    })
    
    def place_order(self, order: PlaceOrderBase) -> dict:
        # Use `ccxt` to construct the order and send it to the Bitget exchange
        # Convert the response into a standard format (e.g., {"status": OrderStatus.OPEN})
        pass

    def get_balance(self) -> dict:
        # Implement the method using ccxt's functions for Bitget
        pass

    def set_leverage(self, leverage: int) -> dict:
        # Implement the method using ccxt's functions for Bitget
        pass