from app.db.models import UserInDB
from app.db.repositories.base import BaseRepository
from typing import Optional
from app.db.services.mongodbservice import AsyncMongoDBService

class UserRepository(BaseRepository):

    # Collection name to be used for users in MongoDB
    USER_COLLECTION_NAME = "users"
    EXCHANGE_COLLECTION_NAME = "exchange_credentials"

    def __init__(self, db_service: AsyncMongoDBService):
        self._db_service = db_service

    async def get(self, username: str) -> Optional[UserInDB]:
        """Retrieve a user by username along with their exchange credentials."""
        user_data = await self._db_service.find_one(self.USER_COLLECTION_NAME, {"username": username})
        if not user_data:
            return None

        # Extract user_id from the retrieved user data
        user_id = user_data["_id"]
        exchange_credentials = await self._db_service.find(self.EXCHANGE_COLLECTION_NAME, {"user_id": user_id}).to_list()

        # Convert ObjectId to string for serialization
        user_data["_id"] = str(user_data["_id"])
        
        # Attach the exchange credentials to the user data
        user_data["exchanges"] = exchange_credentials
        return UserInDB(**user_data)

    async def create(self, user: UserInDB) -> UserInDB:
        """Create a new user."""
        user_id = await self._db_service.insert_one(self.COLLECTION_NAME, user.model_dump())
        
        return user
    
    async def update(self, username: str, user: UserInDB) -> UserInDB:
        pass

    async def delete(self, username: str) -> None:
        pass

    async def get_exchange_credentials(self, user_id: str, exchange_name: str) -> Optional[dict]:
        """Retrieve a user's api_key and secret for a given exchange."""
        credentials = await self._db_service.find_one(self.EXCHANGE_COLLECTION_NAME, {"user_id": user_id, "name": exchange_name})
        return credentials