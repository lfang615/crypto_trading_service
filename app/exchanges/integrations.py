import ccxt
from abc import ABC, abstractmethod
from app.db.models import PlaceOrderBase, OrderStructure, OrderType, OrderStatus

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
    
    async def place_order(self, order:PlaceOrderBase) -> OrderStructure:
        match order.type:
            case OrderType.MARKET:
                return await self.place_market_order(order)
            case OrderType.LIMIT:
                return await self.place_limit_order(order)
            case OrderType.STOP_LIMIT:
                return await self.place_stop_limit_order(order)
            case OrderType.STOP_MARKET:
                return await self.place_stop_market_order(order)
            case OrderType.TAKE_PROFIT_STOP_LOSS:
                return await self.place_tpsl_order(order)

    @abstractmethod
    async def place_market_order(self, order: PlaceOrderBase) -> dict:
        pass

    @abstractmethod
    async def place_limit_order(self, order: PlaceOrderBase) -> dict:
        pass

    @abstractmethod
    async def place_stop_limit_order(self, order: PlaceOrderBase) -> dict:
        pass

    @abstractmethod
    async def place_stop_market_order(self, order: PlaceOrderBase) -> dict:
        pass

    @abstractmethod
    async def place_tpsl_order(self, order: PlaceOrderBase) -> dict:
        pass

    @abstractmethod
    async def get_balance(self) -> dict:
        pass

    @abstractmethod
    async def set_leverage(self, leverage: int) -> dict:
        pass

class BitgetExchange(AbstractExchange):
    def __init__(self, api_key: str, api_secret: str):
        super().__init__(api_key, api_secret)
        self.exchange = ccxt.bitget({
            'apiKey': self.api_key,
            'secret': self.api_secret,
        })

    async def place_market_order(self, order: PlaceOrderBase) -> OrderStructure:
        return super().place_market_order(order)
    
    async def place_limit_order(self, order: PlaceOrderBase) -> OrderStructure:
        return super().place_limit_order(order)
    
    async def place_stop_limit_order(self, order: PlaceOrderBase) -> OrderStructure:
        return super().place_stop_limit_order(order)
    
    async def place_stop_market_order(self, order: PlaceOrderBase) -> OrderStructure:
        return super().place_stop_market_order(order)
    
    async def place_tpsl_order(self, order: PlaceOrderBase) -> OrderStructure:
        return super().place_tpsl_order(order)

    async def get_balance(self) -> dict:
        # Implement the method using ccxt's functions for Bitget
        pass

    async def set_leverage(self, leverage: int) -> dict:
        # Implement the method using ccxt's functions for Bitget
        pass

class BybitExchange(AbstractExchange):
    def __init__(self, api_key: str, api_secret: str):
        super().__init__(api_key, api_secret)
        self.exchange = ccxt.bybit({
            'apiKey': self.api_key,
            'secret': self.api_secret,
    })
    
    async def place_market_order(self, order: PlaceOrderBase) -> OrderStructure:
        return super().place_market_order(order)
    
    async def place_limit_order(self, order: PlaceOrderBase) -> OrderStructure:
        return super().place_limit_order(order)
    
    async def place_stop_limit_order(self, order: PlaceOrderBase) -> OrderStructure:
        return super().place_stop_limit_order(order)
    
    async def place_stop_market_order(self, order: PlaceOrderBase) -> OrderStructure:
        return super().place_stop_market_order(order)
    
    async def place_tpsl_order(self, order: PlaceOrderBase) -> OrderStructure:
        return super().place_tpsl_order(order)

    async def get_balance(self) -> dict:
        # Implement the method using ccxt's functions for Bitget
        pass

    async def set_leverage(self, leverage: int) -> dict:
        # Implement the method using ccxt's functions for Bitget
        pass