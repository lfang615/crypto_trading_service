from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


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
    clientOrderId: Optional[str] = Field(None)
    timeInForce: Optional[TimeInForce] = Field(None)
    takeProfit: Optional[float] = Field(None)
    stopLoss: Optional[float] = Field(None)
    exchangeSpecificParams: Optional[dict] = Field(None)