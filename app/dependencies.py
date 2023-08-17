from fastapi import Depends
from app.db.services.mongodbservice import AsyncMongoDBService
from app.db.repositories.userrepository import UserRepository


def get_db_service() -> AsyncMongoDBService:
    return AsyncMongoDBService()

def get_user_repository(db_service: AsyncMongoDBService = Depends(get_db_service)) -> UserRepository:
    return UserRepository(db_service)


