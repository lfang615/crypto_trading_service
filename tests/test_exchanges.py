import pytest
from app.exchanges.integrations import AbstractExchange, BitgetExchange, BybitExchange

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
