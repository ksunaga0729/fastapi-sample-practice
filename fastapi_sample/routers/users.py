from typing import List

from fastapi import APIRouter, Depends

from fastapi_sample import models
from fastapi_sample.cruds import MessageRepository, UserRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.schemas import message as message_schema
from fastapi_sample.schemas import user as user_schema
from fastapi_sample.services import NotFoundException, authentication
from fastapi_sample.utils.pagination import pagination

router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)

category = "users"


@router.get(
    "/",
    response_model=List[user_schema.User],
    tags=[category],
)
def read_users(
    page: int = 1,
    current_user: models.User = Depends(authentication.get_current_active_user),
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
) -> List[models.User]:
    limit, skip = pagination(page)
    users_list = user_repository.get_users(skip=skip, limit=limit)
    return users_list


@router.get(
    "/me",
    response_model=user_schema.User,
    tags=[category],
)
def get_current_user(
    current_user: models.User = Depends(authentication.get_current_active_user),
) -> models.User:
    return current_user


@router.get(
    "/{user_id}",
    response_model=user_schema.User,
    tags=[category],
)
def read_user(
    user_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
) -> models.User:
    user = user_repository.get_user_by_user_id(user_id)
    if user is None:
        raise NotFoundException(message="User not found")

    return user


@router.get(
    "/{user_id}/messages",
    response_model=List[message_schema.Message],
    tags=[category],
)
def get_messages_by_user_id(
    user_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
    message_repository: MessageRepository = Depends(get_repository(MessageRepository)),
) -> List[models.Message]:
    user = user_repository.get_user_by_user_id(user_id)
    if user is None:
        raise NotFoundException(message="user_id not found")
    return message_repository.get_messages_by_userid(user_id)
