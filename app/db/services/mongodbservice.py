from app.core.logging import AsyncLogger
from app.core import config
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Dict, Any
import traceback

class AsyncMongoDBService:
    
    def __init__(self, uri=config.MONGODB_URI, database_name=config.MONGODB_DB):
        self._client = AsyncIOMotorClient(uri)
        self._db: AsyncIOMotorDatabase = self._client[database_name]
        self._logger = AsyncLogger().get_logger()

    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        return self._db[collection_name]

    async def insert_one(self, collection_name: str, data: Dict[str, Any]) -> Any:
        try:
            collection = self.get_collection(collection_name)
            result = await collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            self._logger.error(f"Error inserting document into {collection_name}: {traceback.format_exc()}")
            raise e

    async def find_one(self, collection_name: str, filter: Dict[str, Any], projection: Dict[str, Any] = None) -> Dict[str, Any]:
        try:
            collection = self.get_collection(collection_name)
            return await collection.find_one(filter, projection)
        except Exception as e:
            self._logger.error(f"Error finding document in {collection_name}: {traceback.format_exc()}")
            raise e

    async def update_one(self, collection_name: str, filter: Dict[str, Any], update: Dict[str, Any]) -> None:
        try:
            collection = self.get_collection(collection_name)
            await collection.update_one(filter, update)
        except Exception as e:
            self._logger.error(f"Error updating document in {collection_name}: {traceback.format_exc()}")
            raise e

    async def delete_one(self, collection_name: str, filter: Dict[str, Any]) -> None:
        try:
            collection = self.get_collection(collection_name)
            await collection.delete_one(filter)
        except Exception as e:
            self._logger.error(f"Error deleting document from {collection_name}: {traceback.format_exc()}")
            raise e

    async def close(self) -> None:
        try:
            await self._client.close()
        except Exception as e:
            self._logger.error(f"Error closing MongoDB client: {traceback.format_exc()}")
            raise e
