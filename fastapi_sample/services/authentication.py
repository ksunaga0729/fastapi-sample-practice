from datetime import datetime, timedelta
from typing import Any, Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from fastapi_sample import models
from fastapi_sample.config.jwt_config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    SECRET_KEY,
)
from fastapi_sample.cruds import UserRepository
from fastapi_sample.dependencies.database import get_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authentication/sign_in")


def create_access_token(
    username: str,
    secret_key: str = str(SECRET_KEY),
    jwt_algorithm: str = JWT_ALGORITHM,
) -> str:
    data: Union[Any] = {"sub": username}
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, secret_key, algorithm=jwt_algorithm)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = user_repository.get_user_by_username(username=username)

    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
