from enum import Enum
from typing import Optional, List
from uuid import uuid4
from pydantic import BaseModel, Field, model_validator


class Exchange(str, Enum):
    BITGET = "bitget"
    BYBIT = "bybit"

class ExchangeCredentials(BaseModel):
    user_id: str
    name: Exchange
    api_key: str
    api_secret: str

class User(BaseModel):
    username: str

class UserInDB(User):
    _id: str    
    hashed_password: str
    api_key: str
    api_secret: str
    exchanges: List[ExchangeCredentials]

class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"

class OrderType(str, Enum):
    LIMIT = "limit"
    MARKET = "market"
    STOP_LIMIT = "stop_limit"
    STOP_MARKET = "stop_market"
    TAKE_PROFIT_STOP_LOSS = "tpsl_market"

class OrderStatus(str, Enum):
    NEW = "new"
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    REJECTED = "rejected"

class TimeInForce(str, Enum):
    GoodTillCancel = "GTC"
    ImmediateOrCancel = "IOC"
    FillOrKill = "FOK"

class PositionAction(str, Enum):
    OPEN = "open"
    CLOSE = "close"

class PlaceOrderBase(BaseModel):
    symbol: str
    type: OrderType
    side: OrderSide    
    amount: float
    positionAction: PositionAction
    exchange: Exchange
    price: Optional[float] = Field(None)    
    triggerPrice: Optional[float] = Field(None)
    clientOrderId: str = Field(default_factory=lambda: str(uuid4()))
    timeInForce: Optional[TimeInForce] = Field(None)
    takeProfit: Optional[float] = Field(None)
    stopLoss: Optional[float] = Field(None)
    exchangeSpecificParams: Optional[dict] = Field(None)

    @model_validator(mode='before')
    def check_order_validations(cls, values):
        order_type = values.get("type")
        amount = values.get("amount")
        price = values.get("price")
        trigger_price = values.get("triggerPrice")
        
        # If the order_type == limit and 'amount' is None or 'price' is None
        if order_type == OrderType.LIMIT and (amount is None or price is None):
            raise ValueError("For LIMIT order type, both amount and price must be provided.")
        
        # If order_type is 'market' and 'price' is not None
        if order_type == OrderType.MARKET and price is not None:
            raise ValueError("For MARKET order type, price should not be provided.")
        
        # If order_type is stop_limit or stop_market and amount is None or price is None or trigger_price is None
        if order_type in [OrderType.STOP_LIMIT, OrderType.STOP_MARKET] and (amount is None or price is None or trigger_price is None):
            raise ValueError("For STOP_LIMIT or STOP_MARKET order types, amount, price, and trigger price must all be provided.")
        
        # If order_type is take_profit_stop_loss and trigger_price is None
        if order_type == OrderType.TAKE_PROFIT_STOP_LOSS and trigger_price is None:
            raise ValueError("For TAKE_PROFIT_STOP_LOSS order type, trigger price must be provided.")
        
        return values