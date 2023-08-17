from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from typing import Any, Dict
from app.core import config

class AsyncMongoDBService:
    
    def __init__(self, uri = config.MONGODB_URI, database_name = config.MONGODB_DB):
        self._client = AsyncIOMotorClient(uri)
        self._db: AsyncIOMotorDatabase = self._client[database_name]

    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        """Retrieve a specific collection from the database."""
        return self._db[collection_name]

    async def insert_one(self, collection_name: str, data: Dict[str, Any]) -> Any:
        """Insert a single document into a collection."""
        collection = self.get_collection(collection_name)
        result = await collection.insert_one(data)
        return result.inserted_id

    async def find_one(self, collection_name: str, filter: Dict[str, Any], projection: Dict[str, Any] = None) -> Dict[str, Any]:
        """Retrieve a single document from a collection based on a filter."""
        collection = self.get_collection(collection_name)
        return await collection.find_one(filter, projection)

    async def update_one(self, collection_name: str, filter: Dict[str, Any], update: Dict[str, Any]) -> None:
        """Update a single document in a collection based on a filter."""
        collection = self.get_collection(collection_name)
        await collection.update_one(filter, update)

    async def delete_one(self, collection_name: str, filter: Dict[str, Any]) -> None:
        """Delete a single document from a collection based on a filter."""
        collection = self.get_collection(collection_name)
        await collection.delete_one(filter)

    async def close(self) -> None:
        """Close the MongoDB client connection."""
        await self._client.close()