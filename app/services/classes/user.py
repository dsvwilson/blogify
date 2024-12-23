# security module imports
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

# external module imports
import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone

# internal module imports
from app.database.user_db import get_user
from app.services.schema.user import LoginData


class User:
    # authentication and authorisation variables
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 574
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")

    def __init__(self):
        pass

    #for now, only for use internally to generate a hashed password
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return User.pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def authenticate_user(username, password):
        user = get_user(username)
        if not user or not User.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, User.SECRET_KEY, algorithm=User.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, User.SECRET_KEY, algorithms=[User.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = LoginData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    
    
