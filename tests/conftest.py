import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from typing import Optional
from app.main import app as fastapi_app
from app.db.models import UserInDB, PlaceOrderBase, OrderSide, OrderType, PositionAction, Exchange, TimeInForce, ExchangeCredentials, OrderStructure
from app.auth.jwt import create_access_token
from unittest.mock import AsyncMock, MagicMock, patch
from app.db.services.mongodbservice import AsyncMongoDBService
from app.db.services.redisservice import AsyncRedisService
from app.db.repositories.userrepository import UserRepository
from app.exchanges.integrations import AbstractExchange
import json


@pytest.fixture
def app() -> FastAPI:
    return fastapi_app

@pytest.fixture
async def client(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def test_user() -> UserInDB:
    return UserInDB(id="test_id",
                    username="testuser", 
                    hashed_password="$2b$12$Kb6vlfMV36Qg1T0DDZJP2uGZyHDUxSjtZJN.MEKEYE3iS1wBxM7Ae", 
                    api_key="test_api_key", 
                    api_secret="test_api_secret",
                    exchanges=[ExchangeCredentials(user_id="test_id", name=Exchange.BITGET, api_key="test_api_key", api_secret="test_api_secret") ])

@pytest.fixture
def test_user_token(test_user: UserInDB) -> str:
    return create_access_token(data={"sub": test_user.username})

@pytest.fixture
def mock_db_service(monkeypatch, test_user:UserInDB) -> AsyncMongoDBService:
    async def _mock_find_one(collection_name:str, username: str) -> UserInDB:
        return test_user.model_dump()
    # Mock AsyncIOMotorClient instantiation
    mock_client = MagicMock()
    mock_client.__getitem__.return_value = MagicMock()  # mock database retrieval using indexing
    monkeypatch.setattr('app.db.services.mongodbservice.AsyncIOMotorClient', lambda x: mock_client)
    # monkeypatch.setattr(AsyncMongoDBService, "find_one", _mock_find_one)
    mock_service = AsyncMongoDBService(uri="mock://mockdb", database_name="mockdb")

    return mock_service

@pytest.fixture
def mock_get_user(test_user: UserInDB):
    async def _mock_get_user(username: str) -> Optional[UserInDB]:
        if username == test_user.username:
            return test_user
        return None

    with patch('app.db.repositories.userrepository.UserRepository.get', new_callable=AsyncMock, side_effect=_mock_get_user) as _mocked:
        yield _mocked

@pytest.fixture
def mock_create_user(monkeypatch, mock_db_service: AsyncMongoDBService):
    async def _mock_create_user(user: UserInDB):
        return "mocked_id"
    # Monkeypatching the create method of UserRepository
    monkeypatch.setattr(UserRepository, "create", _mock_create_user)
    
    # Instantiate and return the UserRepository with the mocked method
    return UserRepository(mock_db_service)

@pytest.fixture
def limit_order() -> json:    
    return {
        "symbol": "BTCUSDT",
        "type": OrderType.LIMIT.value,  # assuming you have the OrderType enum defined
        "side": OrderSide.BUY.value,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN.value,
        "exchange": Exchange.BITGET.value,  # assuming you have the Exchange enum defined
        "price": 35000.00,
        "triggerPrice": None,
        "clientOrderId": "test_order_123",
        "timeInForce": TimeInForce.GoodTillCancel.value,  # assuming you have the TimeInForce enum defined
        "takeProfit": 37000.00,
        "stopLoss": 33000.00        
}

test_position_data = {
    "exchange": Exchange.BITGET,  # Assuming the Exchange enum is already defined with values like 'BITGET'
    "info": {},  # Empty object for simplicity, can be filled with more detailed data if required
    "id": "pos123456",
    "symbol": "BTCUSDT",
    "timestamp": 1628918400,
    "datetime": "2021-08-14T12:00:00Z",
    "isolated": True,
    "hedged": False,
    "side": "buy",
    "contracts": 1,
    "contractSize": 1,
    "entryPrice": 35000.00,
    "markPrice": 36000.00,
    "notional": 36000.00,
    "leverage": 10.0,
    "collateral": 3600.00, 
    "initialMargin": 3600.00,
    "maintenanceMargin": 1800.00,
    "initialMarginPercentage": 0.1,
    "maintenanceMarginPercentage": 0.05,
    "unrealizedPnl": 1000.00,
    "liquidationPrice": 32000.00,
    "marginMode": "isolated",
    "percentage": 0.2778
}
    
# Mock for Redis with no position
@pytest.fixture
def mock_redis_no_position(monkeypatch):
    # Mocking the get_position method to return None
    mock_get_position = AsyncMock(return_value=None)

    # Monkeypatch the RedisWrapper's get_position method
    monkeypatch.setattr(AsyncRedisService, "get_position", mock_get_position)
    return mock_get_position


# Mock for Redis with an open position
@pytest.fixture
def mock_redis_with_position(monkeypatch):
    # Mocking the get_position method to return a simulated position
    mock_get_position = AsyncMock(return_value=test_position_data)

    # Monkeypatch the RedisWrapper's get_position method
    monkeypatch.setattr(AsyncRedisService, "get_position", mock_get_position)
    return mock_get_position

@pytest.fixture
def mock_bitget_close_position_order() -> json:
    return {
       "symbol": "BTCUSDT",
        "type": OrderType.LIMIT,
        "side": OrderSide.SELL,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN,
        "exchange": Exchange.BITGET,  
        "price": 35000.00,        
        "clientOrderId": "test_order_123",
        "timeInForce": TimeInForce.GoodTillCancel            
    }

@pytest.fixture
def mock_bitget_place_order_response() -> OrderStructure:
    mock_order_structure = OrderStructure(
        id="mock_id",
        status="mock_status",
        clientOrderId="mock_client_order_id"
    )

    async def _mock_place_order(*args, **kwargs):
        return mock_order_structure

    with patch('app.exchanges.integrations.BitgetExchange.place_order', new_callable=AsyncMock, return_value=_mock_place_order) as _mocked:
        yield _mocked
    
@pytest.fixture
def mock_bitget_tpsl_order() -> json:
    return {
        "symbol": "BTCUSDT",
        "type": OrderType.TAKE_PROFIT_STOP_LOSS,
        "side": OrderSide.SELL,
        "amount": 0.1,
        "positionAction": PositionAction.OPEN,
        "exchange": Exchange.BITGET,  
        "triggerPrice": 37000.00,
        "takeProfit": 38000.00,
        "stopLoss": 36000.00,
        "clientOrderId": "test_order_123",
        "timeInForce": TimeInForce.GoodTillCancel            
    }