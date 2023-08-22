import pytest
from app.exchanges.integrations import AbstractExchange, BitgetExchange, BybitExchange, PlaceOrderBase, OrderType, OrderStructure

def test_create_exchange():
    # Test creation of BitgetExchange
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
    "order_type, expected_id, price, trigger_price",
    [
        (OrderType.MARKET, "market", None, None),
        (OrderType.LIMIT, "limit", 25400, None),
        (OrderType.STOP_LIMIT, "stop_limit", 25400, 25000),
        (OrderType.STOP_MARKET, "stop_market", None, 25000),
        (OrderType.TAKE_PROFIT_STOP_LOSS, "tpsl", 20000, 25000),
    ]
)
async def test_place_order(order_type, expected_id, price, trigger_price):
    mock_exchange = MockExchange("api_key", "api_secret")
    # mock_exchange.name = "bitget"
    order = PlaceOrderBase(type=order_type, symbol="BTCUSDT", side="buy", amount=1, positionAction="open", exchange="bitget", price=price, triggerPrice=trigger_price)    
    result = await mock_exchange.place_order(order)
    assert result.id == expected_id