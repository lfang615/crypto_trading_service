from unittest.mock import AsyncMock
import pytest
from app.db.repositories.userrepository import UserRepository
from app.db.services.mongodbservice import AsyncMongoDBService

# Sample data for testing
sample_user_id = "testuser123"
sample_exchange_name = "binance"
sample_credentials = {
    "user_id": sample_user_id,
    "name": sample_exchange_name,
    "api_key": "sample_api_key",
    "api_secret": "sample_api_secret"
}

@pytest.fixture
def mock_db_service():
    mock_service = AsyncMock(spec=AsyncMongoDBService)
    mock_service.find_one.return_value = sample_credentials
    return mock_service

@pytest.mark.asyncio
async def test_get_exchange_credentials(mock_db_service):
    # Instantiate the UserRepository with the mocked database service
    user_repo = UserRepository(mock_db_service)

    # Call the method
    credentials = await user_repo.get_exchange_credentials(sample_user_id, sample_exchange_name)

    # Verify the results
    assert credentials == sample_credentials
    mock_db_service.find_one.assert_called_once_with(UserRepository.EXCHANGE_COLLECTION_NAME, {"user_id": sample_user_id, "name": sample_exchange_name})

