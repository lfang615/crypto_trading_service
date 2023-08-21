import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from typing import Optional
from app.main import app as fastapi_app
from app.db.models import UserInDB, PlaceOrderBase, OrderSide, OrderType, PositionAction, Exchange, TimeInForce, ExchangeCredentials
from app.auth.jwt import create_access_token
from unittest.mock import AsyncMock, MagicMock, patch
from app.db.services.mongodbservice import AsyncMongoDBService
from app.db.repositories.userrepository import UserRepository
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
    
