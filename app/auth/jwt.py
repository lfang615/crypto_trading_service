from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core import config
from app.db.models import UserInDB
from app.dependencies import get_user_repository
from app.main import logger_instance


# For hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# This class is used to get token data
class Token(BaseModel):
    access_token: str
    token_type: str

# This class is used to get user data from the token
class TokenData(BaseModel):
    username: str = None

# This is used to get the token URL (e.g., /token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# For creating the access token
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt



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
        logger_instance.with_traceback("Error while decoding token")
        raise credentials_exception
    user = await user_repository.get(username=token_data.username)
    if user is None:
        logger_instance.with_traceback("User not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# For verifying the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# For hashing the password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

if __name__ == "__main__":
    print(get_password_hash("password"))
