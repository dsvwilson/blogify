# external module imports
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, status

# internal module imports
from app.services.schema.user import Login
from app.services.classes.user import User

router = APIRouter()

# endpoint to generate a login token after authenticating username and password
@router.post("/login")
async def login_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Login:
    user = User.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=User.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = User.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Login(access_token=access_token, token_type="bearer")