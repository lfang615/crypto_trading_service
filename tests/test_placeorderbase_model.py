import pytest
from pydantic import ValidationError
from app.db.models import PlaceOrderBase, OrderType, OrderSide, PositionAction, Exchange, TimeInForce

def test_valid_limit_order():
    # Valid Limit Order
    data = {
        "symbol": "BTC/USD",
        "type": OrderType.LIMIT,
        "side": OrderSide.BUY,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN,
        "exchange": Exchange.BITGET,
        "price": 35000.00
    }
    assert PlaceOrderBase(**data)


def test_invalid_limit_order_missing_price():
    # Limit Order missing price
    data = {
        "symbol": "BTC/USD",
        "type": OrderType.LIMIT,
        "side": OrderSide.BUY,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN,
        "exchange": Exchange.BITGET
    }
    with pytest.raises(ValidationError):
        PlaceOrderBase(**data)


def test_valid_market_order():
    # Valid Market Order
    data = {
        "symbol": "BTC/USD",
        "type": OrderType.MARKET,
        "side": OrderSide.BUY,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN,
        "exchange": Exchange.BITGET
    }
    assert PlaceOrderBase(**data)


def test_invalid_market_order_with_price():
    # Market Order with price
    data = {
        "symbol": "BTC/USD",
        "type": OrderType.MARKET,
        "side": OrderSide.BUY,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN,
        "exchange": Exchange.BITGET,
        "price": 35000.00
    }
    with pytest.raises(ValidationError):
        PlaceOrderBase(**data)


def test_valid_stop_limit_order():
    # Valid Stop Limit Order
    data = {
        "symbol": "BTC/USD",
        "type": OrderType.STOP_LIMIT,
        "side": OrderSide.BUY,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN,
        "exchange": Exchange.BITGET,
        "price": 35000.00,
        "triggerPrice": 34000.00
    }
    assert PlaceOrderBase(**data)


def test_invalid_stop_limit_order_missing_trigger_price():
    # Stop Limit Order missing trigger price
    data = {
        "symbol": "BTC/USD",
        "type": OrderType.STOP_LIMIT,
        "side": OrderSide.BUY,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN,
        "exchange": Exchange.BITGET,
        "price": 35000.00
    }
    with pytest.raises(ValidationError):
        PlaceOrderBase(**data)

def test_valid_stop_market_order():
    # Valid Stop Market Order
    data = {
        "symbol": "BTC/USD",
        "type": OrderType.STOP_MARKET,
        "side": OrderSide.BUY,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN,
        "exchange": Exchange.BITGET,
        "triggerPrice": 34000.00
    }
    assert PlaceOrderBase(**data)

def test_invalid_stop_market_order_missing_trigger_price():
    # Stop Market Order missing trigger price
    data = {
        "symbol": "BTC/USD",
        "type": OrderType.STOP_MARKET,
        "side": OrderSide.BUY,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN,
        "exchange": Exchange.BITGET
    }
    with pytest.raises(ValidationError):
        PlaceOrderBase(**data)


def test_valid_take_profit_stop_loss_order():
    # Valid Take Profit Stop Loss Order
    data = {
        "symbol": "BTC/USD",
        "type": OrderType.TAKE_PROFIT_STOP_LOSS,
        "side": OrderSide.BUY,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN,
        "exchange": Exchange.BITGET,
        "takeProfit": 36000.00
    }
    assert PlaceOrderBase(**data)


def test_invalid_take_profit_stop_loss_order_missing_required_value():
    # Take Profit Stop Loss Order missing trigger price
    data = {
        "symbol": "BTC/USD",
        "type": OrderType.TAKE_PROFIT_STOP_LOSS,
        "side": OrderSide.BUY,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN,
        "exchange": Exchange.BITGET,
        "triggerPrice": 34000.00
    }
    with pytest.raises(ValidationError):
        PlaceOrderBase(**data)

