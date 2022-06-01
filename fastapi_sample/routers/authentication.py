from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_sample import models
from fastapi_sample.cruds import UserRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.schemas import token as token_schema
from fastapi_sample.schemas import user as user_schema
from fastapi_sample.services import authentication

router = APIRouter(
    prefix="/authentication",
    responses={404: {"description": "Not found"}},
)

category = "authentication"


@router.post("/sign_up", response_model=user_schema.User, tags=[category])
async def sign_up(
    new_user: user_schema.UserCreate = Body(..., embed=True),
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
) -> models.User:
    created_user = user_repository.create_user(new_user)
    return created_user


@router.post("/sign_in", tags=[category])
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
) -> token_schema.Token:
    user = user_repository.get_user_by_username(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = authentication.create_access_token(user.username)
    return token_schema.Token(access_token=access_token, token_type="bearer")
