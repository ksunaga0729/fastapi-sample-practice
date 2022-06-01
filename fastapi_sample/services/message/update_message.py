from fastapi import Depends

from fastapi_sample import models
from fastapi_sample.cruds import MessageRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.services.exceptions import ForbiddenException, NotFoundException


class UpdateMessageService:
    def __init__(
        self,
        message_repository: MessageRepository = Depends(
            get_repository(MessageRepository)
        ),
    ):
        self.__message_repository = message_repository

    def update_message(
        self, message_id: int, new_content: str, current_user: models.User
    ) -> models.Message:
        message = self.__message_repository.get_message_by_message_id(message_id)

        if message is None:
            raise NotFoundException(message="message_id not found")
        if message.user_id != current_user.id:
            raise ForbiddenException(message="It's not a message you sent.")

        self.__message_repository.update_read_time(message_id)
        message.content = new_content
        return self.__message_repository.update_message_by_message_id(message)
