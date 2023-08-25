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
    id: str
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
    price: Optional[float] = Field(default=None)    
    triggerPrice: Optional[float] = Field(default=None)
    clientOrderId: str = Field(default_factory=lambda: str(uuid4()))
    timeInForce: Optional[TimeInForce] = Field(default=TimeInForce.GoodTillCancel)
    takeProfit: Optional[float] = Field(default=None)
    stopLoss: Optional[float] = Field(default=None)

    @model_validator(mode='before')
    def check_order_validations(cls, values):
        order_type = values.get("type")
        amount = values.get("amount")
        price = values.get("price")
        trigger_price = values.get("triggerPrice")
        takeProfit = values.get("takeProfit")
        stopLoss = values.get("stopLoss")
        
        # If the order_type == limit and 'amount' is None or 'price' is None
        if order_type == OrderType.LIMIT and (amount is None or price is None):
            raise ValueError("For LIMIT order type, both amount and price must be provided.")
        
        # If order_type is 'market' and 'price' is not None
        if order_type == OrderType.MARKET and price is not None:
            raise ValueError("For MARKET order type, price should not be provided.")
        
        # If order_type is stop_limit or stop_market and amount is None or price is None or trigger_price is None
        if order_type == OrderType.STOP_LIMIT and (amount is None or price is None or trigger_price is None):
            raise ValueError("For STOP_LIMIT or STOP_MARKET order types, amount, price, and trigger price must all be provided.")
        
        if order_type == OrderType.STOP_MARKET and (amount is None or trigger_price is None):
            raise ValueError("For STOP_MARKET order type, amount and trigger price must be provided.")
        
        # If order_type is take_profit_stop_loss and trigger_price is None
        if order_type == OrderType.TAKE_PROFIT_STOP_LOSS and (takeProfit is None and stopLoss is None):
            raise ValueError("For TAKE_PROFIT_STOP_LOSS order type, takeProfit or stopLoss must be provided.")
        
        return values
    
class OrderStructure(BaseModel):
    id: str
    clientOrderId: str
    datetime: Optional[str] = Field(None)
    timestamp: Optional[int] = Field(None)
    lastTradeTimestamp: Optional[int] = Field(None)
    status: Optional[str] = Field(None)
    symbol: str = Field(None)
    type: Optional[str] = Field(None)
    timeInForce: Optional[str] = Field(None)
    side: Optional[str] = Field(None)
    price: Optional[float] = Field(None)
    average: Optional[float] = Field(None)
    amount: Optional[float] = Field(None)
    filled: Optional[float] = Field(None)
    remaining: Optional[float] = Field(None)
    cost: Optional[float] = Field(None)
    trades: Optional[list] = Field(None)
    fee: Optional[dict] = Field(None)
    info: Optional[dict] = Field(None)

class PositionStructure(BaseModel):
    exchange: Exchange
    info: object
    id: str
    symbol: str
    timestamp: int
    datetime: str
    isolated: bool
    hedged: bool
    side: str
    contracts: int
    contractSize: int
    entryPrice: float
    markPrice: float
    notional: float # the value of the position in the settlement currency
    leverage: float
    collateral: float
    initialMargin: float
    maintenanceMargin: float
    initialMarginPercentage: float
    maintenanceMarginPercentage: float
    unrealizedPnl: float # differncebetween the market price and entry price * qty
    liquidationPrice: float # price at which collateral < maintenanceMargin (NUKED)
    marginMode: str # crossed or isolated
    percentage: float # represents unrealizedPnl / initialMargin