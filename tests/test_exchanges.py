import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.exchanges.integrations import AbstractExchange, BitgetExchange, BybitExchange, \
PlaceOrderBase, OrderType, OrderStructure
from app.db.models import OrderSide, PositionAction, Exchange, TimeInForce

def test_create_exchange():
    # Test creation of BitgetExchangey
    exchange = AbstractExchange.create("bitget", "api_key", "api_secret")
    assert isinstance(exchange, BitgetExchange)

    # Test creation of BybitExchange
    exchange = AbstractExchange.create("bybit", "api_key", "api_secret")
    assert isinstance(exchange, BybitExchange)

    # Test invalid exchange name
    with pytest.raises(ValueError, match="Unsupported exchange: invalid"):
        AbstractExchange.create("invalid", "api_key", "api_secret")

class MockExchange(AbstractExchange):

    async def place_market_order(self, order: PlaceOrderBase) -> OrderStructure:
        return OrderStructure(id="market", clientOrderId="test")

    async def place_limit_order(self, order: PlaceOrderBase) -> OrderStructure:
        return OrderStructure(id="limit", clientOrderId="test")

    async def place_stop_limit_order(self, order: PlaceOrderBase) -> OrderStructure:
        return OrderStructure(id="stop_limit", clientOrderId="test")

    async def place_stop_market_order(self, order: PlaceOrderBase) -> OrderStructure:
        return OrderStructure(id="stop_market", clientOrderId="test")

    async def place_tpsl_order(self, order: PlaceOrderBase) -> OrderStructure:
        return OrderStructure(id="tpsl", clientOrderId="test")
    
    async def get_balance(self) -> dict:
        pass

    async def set_leverage(self, leverage: int) -> dict:
        pass

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "order_type, expected_id, price, trigger_price, take_profit, stop_loss",
    [
        (OrderType.MARKET, "market", None, None, None, None),
        (OrderType.LIMIT, "limit", 25400, None, None, None),
        (OrderType.STOP_LIMIT, "stop_limit", 25400, 25000, None, None),
        (OrderType.STOP_MARKET, "stop_market", None, 25000, None, None),
        (OrderType.TAKE_PROFIT_STOP_LOSS, "tpsl", 20000, 25000, None, 19500),
    ]
)
async def test_place_order(order_type, expected_id, price, trigger_price, take_profit, stop_loss):
    mock_exchange = MockExchange("api_key", "api_secret")
    # mock_exchange.name = "bitget"
    order = PlaceOrderBase(type=order_type, symbol="BTCUSDT", side="buy", amount=1, positionAction="open", exchange="bitget", price=price, triggerPrice=trigger_price, takeProfit=take_profit, stopLoss=stop_loss)    
    result = await mock_exchange.place_order(order)
    assert result.id == expected_id

@pytest.mark.asyncio
async def test_bitget_place_market_order():
    with patch("app.exchanges.integrations.ccxt.bitget.create_order", new_callable=AsyncMock) as mock_create_market_order:
        bitget = BitgetExchange('test_key', 'test_secret')
        order = PlaceOrderBase(
            symbol="BTCUSDT",
            type=OrderType.MARKET,
            side=OrderSide.BUY,
            amount=1,
            clientOrderId="test123",
            exchange=Exchange.BITGET,
            positionAction=PositionAction.OPEN,
            timeInForce=TimeInForce.GoodTillCancel      
        )
        await bitget.place_market_order(order)
        
        mock_create_market_order.assert_called_once_with("BTCUSDT", OrderType.MARKET, OrderSide.BUY, 1, params={'clientOrderId': 'test123', 'timeInForce': 'GTC'})

@pytest.mark.asyncio
async def test_bitget_place_limit_order():
    with patch("app.exchanges.integrations.ccxt.bitget.create_order", new_callable=AsyncMock) as mock_create_limit_order:
        bitget = BitgetExchange('test_key', 'test_secret')
        order = PlaceOrderBase(
            symbol="BTCUSDT",
            type=OrderType.LIMIT,
            side=OrderSide.BUY,
            amount=1,
            clientOrderId="test123",
            exchange=Exchange.BITGET,
            positionAction=PositionAction.OPEN,
            price=30000.00,
            timeInForce=TimeInForce.GoodTillCancel      
        )
        await bitget.place_limit_order(order)
        
        mock_create_limit_order.assert_called_once_with("BTCUSDT", OrderType.LIMIT, OrderSide.BUY, 1, 30000.00, params={'clientOrderId': 'test123', 'timeInForce': 'GTC'})

@pytest.mark.asyncio
@pytest.mark.parametrize("position_action, expected_reduce_only", [
    (PositionAction.OPEN, False),
    (PositionAction.CLOSE, True),
])
async def test_bitget_place_stop_limit_order(position_action, expected_reduce_only):
      with patch("app.exchanges.integrations.ccxt.bitget.create_order", new_callable=AsyncMock) as mock_create_stop_limit_order:
        bitget = BitgetExchange('test_key', 'test_secret')
        order = PlaceOrderBase(
            symbol="BTCUSDT",
            type=OrderType.STOP_LIMIT,
            side=OrderSide.BUY,
            amount=1,
            clientOrderId="test123",
            exchange=Exchange.BITGET,
            positionAction=position_action,
            price=30000.00,
            timeInForce=TimeInForce.GoodTillCancel,
            triggerPrice=25000.00    
        )
        await bitget.place_stop_limit_order(order)
        
        mock_create_stop_limit_order.assert_called_once_with("BTCUSDT", 
                                                            OrderType.LIMIT.value,
                                                            OrderSide.BUY.value,
                                                            1,
                                                            30000.00, 
                                                            params={'triggerPrice': 25000.00, 'clientOrderId': 'test123', 'timeInForce': 'GTC', 'reduceOnly': expected_reduce_only})
        
@pytest.mark.asyncio
@pytest.mark.parametrize("position_action, expected_reduce_only", [
    (PositionAction.OPEN, False),
    (PositionAction.CLOSE, True),
])
async def test_bitget_place_stop_market_order(position_action, expected_reduce_only):
    bitget = BitgetExchange('test_key', 'test_secret')
    
    with patch("app.exchanges.integrations.ccxt.bitget.create_order", new_callable=AsyncMock) as mock_create_stop_market_order:
        
        order = PlaceOrderBase(
            symbol="BTCUSDT",
            type=OrderType.STOP_MARKET,
            side=OrderSide.BUY,
            amount=1,
            clientOrderId="test123",
            exchange=Exchange.BITGET,
            positionAction=position_action,
            price=30000.00,
            timeInForce=TimeInForce.GoodTillCancel,
            triggerPrice=25000.00    
        )
        
        await bitget.place_stop_market_order(order)
        
        mock_create_stop_market_order.assert_called_once_with("BTCUSDT", 
                                                            OrderType.MARKET.value,
                                                            OrderSide.BUY.value,
                                                            1,                                                            
                                                            params={'triggerPrice': 25000.00, 
                                                                    'clientOrderId': 'test123', 
                                                                    'timeInForce': 'GTC', 
                                                                    'reduceOnly': expected_reduce_only})
        
@pytest.mark.asyncio
@pytest.mark.parametrize("take_profit, stop_loss", [
    (35000.00, 30000.00),
    (None, 30000.00),
    (35000.00, None),
])
async def test_bitget_place_tpsl_order(take_profit, stop_loss):
    with patch("app.exchanges.integrations.ccxt.bitget.create_order", new_callable=AsyncMock) as mock_create_tpsl_order:
        bitget = BitgetExchange('test_key', 'test_secret')
        order = PlaceOrderBase(
            symbol="BTCUSDT",
            type=OrderType.TAKE_PROFIT_STOP_LOSS,
            side=OrderSide.BUY,
            amount=1,
            clientOrderId="test123",
            exchange=Exchange.BITGET,
            positionAction=PositionAction.OPEN,
            price=30000.00,
            timeInForce=TimeInForce.GoodTillCancel,
            takeProfit=take_profit,
            stopLoss=stop_loss
        )
        await bitget.place_tpsl_order(order)
        
        mock_create_tpsl_order.assert_called_once_with("BTCUSDT",
                                                        OrderType.MARKET, 
                                                        OrderSide.BUY, 
                                                        1,
                                                       params={'stopLossPrice': order.stopLoss,
                                                                'takeProfitPrice': order.takeProfit,
                                                                'clientOrderId': 'test123',
                                                                'timeInForce': 'GTC'})