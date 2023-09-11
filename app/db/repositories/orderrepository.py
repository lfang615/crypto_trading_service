from app.db.models import OrderStructure
from app.db.repositories.base import BaseRepository
from typing import Optional
from app.db.services.mongodbservice import AsyncMongoDBService

class OrderRepository(BaseRepository):

    # Collection name to be used for users in MongoDB
    ORDER_COLLECTION_NAME = "orders"
    EXCHANGE_COLLECTION_NAME = "exchange_credentials"

    def __init__(self, db_service: AsyncMongoDBService):
        self._db_service = db_service

    async def get(self, client_oid: str) -> Optional[OrderStructure]:
        """Retrieve a order by clientOrderId"""
        order_data = await self._db_service.find_one(self.ORDER_COLLECTION_NAME, {"clientOrderId": client_oid})
        if not order_data:
            return None
        
        return OrderStructure(**order_data)

    async def create(self, order: OrderStructure) -> OrderStructure:
        """Create a new order."""
        order_id = await self._db_service.insert_one(self.COLLECTION_NAME, order.model_dump())
        
        return order
    
    async def update(self, order_id: str, order: OrderStructure) -> OrderStructure:
        pass

    async def delete(self, order_id: str) -> None:
        pass