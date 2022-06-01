from fastapi import Depends

from fastapi_sample import models
from fastapi_sample.cruds import RoomRepository, ThreadRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.services.exceptions import ForbiddenException, NotFoundException


class GetThreadByThreadIdService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
        thread_repository: ThreadRepository = Depends(get_repository(ThreadRepository)),
    ):
        self.__room_repository = room_repository
        self.__thread_repository = thread_repository

    def get_thread_by_thread_id(
        self, thread_id: int, current_user_id: int
    ) -> models.Thread:
        thread = self.__thread_repository.get_thread_by_thread_id(thread_id)

        if thread is None:
            raise NotFoundException(message="thread_id not found")
        if (
            self.__room_repository.get_member_by_room_and_user_id(
                thread.message.room_id, current_user_id
            )
            is None
        ):
            raise ForbiddenException(message="You don't belong to the specified room")

        return thread
