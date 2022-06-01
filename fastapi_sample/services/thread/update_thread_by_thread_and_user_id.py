from fastapi import Depends

from fastapi_sample import models
from fastapi_sample.cruds import RoomRepository, ThreadRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.services.exceptions import ForbiddenException, NotFoundException


class UpdateThreadByThreadAndUserIdService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
        thread_repository: ThreadRepository = Depends(get_repository(ThreadRepository)),
    ):
        self.__thread_repository = thread_repository
        self.__room_repository = room_repository

    def update_thread_by_thread_and_user_id(
        self,
        thread_id: int,
        content: str,
        current_user_id: int,
    ) -> models.Thread:
        thread = self.__thread_repository.get_thread_by_thread_id(thread_id)
        if thread is None:
            raise NotFoundException(message="thread_id not found")

        if (
            self.__room_repository.get_member_by_room_and_user_id(
                room_id=thread.message.room_id, user_id=current_user_id
            )
            is None
            or thread.user_id != current_user_id
        ):
            raise ForbiddenException(message="You don't belong to the specified room")

        return self.__thread_repository.update_thread_by_thread_and_user_id(
            thread, content=content
        )
