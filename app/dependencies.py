from fastapi import Depends
from typing import Union
from app.core import config
import app.main as main
from app.db.models import UserInDB, PlaceOrderBase, ExchangeCredentials
from app.db.services.mongodbservice import AsyncMongoDBService
from app.db.repositories.userrepository import UserRepository
from app.auth.jwt import oauth2_scheme, TokenData, JWTError, jwt, HTTPException, status


def get_db_service() -> AsyncMongoDBService:
    return AsyncMongoDBService()

def get_user_repository(db_service: AsyncMongoDBService = Depends(get_db_service)) -> UserRepository:
    return UserRepository(db_service)

# To get the current user from the token
async def get_current_user(token: str = Depends(oauth2_scheme), user_repository = Depends(get_user_repository)) -> Union[UserInDB, None]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:        
        main.logger_instance.with_traceback("Error while decoding token")
        raise credentials_exception
    user = await user_repository.get(username=token_data.username)
    if user is None:
        main.logger_instance.with_traceback("User not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def get_exchange_credentials(order: PlaceOrderBase, 
                             current_user: UserInDB = Depends(get_current_user)
) -> ExchangeCredentials:
    exchange_name = order.exchange.value
    matching_exchange = next((exchange for exchange in current_user.exchanges if exchange.name == exchange_name), None)
    
    if not matching_exchange:
        raise HTTPException(status_code=404, detail="Exchange credentials not found")
    return matching_exchange


