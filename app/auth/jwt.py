from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core import config

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

# For verifying the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# For hashing the password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

if __name__ == "__main__":
    print(get_password_hash("password"))
