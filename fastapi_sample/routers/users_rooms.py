from typing import List

from fastapi import APIRouter, Depends

from fastapi_sample import models
from fastapi_sample.services import GetUsersRoomsService, authentication

router = APIRouter(
    prefix="/user_rooms",
    responses={404: {"description": "Not found"}},
)

category = "user_rooms"


@router.get(
    "/",
    tags=[category],
)
def get_rooms_by_username(
    username: str = None,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: GetUsersRoomsService = Depends(GetUsersRoomsService),
) -> List[models.Room]:
    return service.get_rooms_by_username(current_user, username)
