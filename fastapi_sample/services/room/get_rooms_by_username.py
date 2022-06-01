from typing import List, Optional

from fastapi import Depends

from fastapi_sample import models
from fastapi_sample.cruds import RoomRepository, UserRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.services.exceptions import NotFoundException


class GetUsersRoomsService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
        user_repository: UserRepository = Depends(get_repository(UserRepository)),
    ):
        self.__room_repository = room_repository
        self.__user_repository = user_repository

    def get_rooms_by_username(
        self,
        current_user: models.User,
        username: Optional[str] = None,
    ) -> List[models.Room]:
        user: Optional[models.User]

        if username is None:
            user = current_user
        else:
            user = self.__user_repository.get_user_by_username(username)

        if user is None:
            raise NotFoundException("username not found")

        rooms_list = self.__room_repository.get_room_by_user_id(user.id)
        if not rooms_list:
            raise NotFoundException("room not found")

        return rooms_list
