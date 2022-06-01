import itertools
from typing import List, Optional

from fastapi import Depends

from fastapi_sample import models
from fastapi_sample.cruds import MessageRepository, RoomRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.services.exceptions import ForbiddenException, NotFoundException


class GetMessagesByContentAndRoomIdService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
        message_repository: MessageRepository = Depends(
            get_repository(MessageRepository)
        ),
    ):
        self.__room_repository = room_repository
        self.__message_repository = message_repository

    def get_messages_content_and_room_id(
        self, content: str, room_id: Optional[int], current_user_id: int
    ) -> List[models.Message]:
        if room_id is None:
            msgs_list = []
            room_lists = self.__room_repository.get_room_by_user_id(current_user_id)
            for room in room_lists:
                msg_lists_tmp = (
                    self.__message_repository.get_messages_by_content_and_room_id(
                        content, room.id
                    )
                )
                msgs_list.append(msg_lists_tmp)

            return list(itertools.chain.from_iterable(msgs_list))

        if self.__room_repository.get_room_by_room_id(room_id) is None:
            raise NotFoundException(message="room_id not found")

        if not self.__room_repository.get_member_by_room_and_user_id(
            room_id, current_user_id
        ):
            raise ForbiddenException(message="You don't belong to the specified room")

        messages_list = self.__message_repository.get_messages_by_content_and_room_id(
            content, room_id
        )

        return messages_list
