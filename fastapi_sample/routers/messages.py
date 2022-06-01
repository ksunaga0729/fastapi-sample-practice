from typing import List

from fastapi import APIRouter, Depends

from fastapi_sample import models
from fastapi_sample.cruds import MessageRepository, ThreadRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.schemas import message as message_schema
from fastapi_sample.schemas import thread as thread_schema
from fastapi_sample.services import (
    CreateMessageService,
    CreateThreadService,
    GetMessagesByContentAndRoomIdService,
    GetThreadByMessageIdService,
    GetThreadByThreadIdService,
    NotFoundException,
    UpdateMessageService,
    UpdateThreadByThreadAndUserIdService,
    authentication,
)

router = APIRouter(
    prefix="/messages",
    responses={404: {"description": "Not found"}},
)

category = "message"


@router.get(
    "/",
    response_model=List[message_schema.MessagePublic],
    tags=[category],
)
def get_messages(
    current_user: models.User = Depends(authentication.get_current_active_user),
    message_repository: MessageRepository = Depends(get_repository(MessageRepository)),
) -> List[models.Message]:
    return message_repository.get_messages()


@router.get(
    "/threads",
    response_model=List[thread_schema.Thread],
    tags=[category],
)
def get_threads(
    current_user: models.User = Depends(authentication.get_current_active_user),
    thread_repository: ThreadRepository = Depends(get_repository(ThreadRepository)),
) -> List[models.Thread]:
    return thread_repository.get_threads()


@router.get(
    "/{message_id}",
    response_model=message_schema.MessagePublic,
    tags=[category],
)
def get_message_by_message_id(
    message_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    message_repository: MessageRepository = Depends(get_repository(MessageRepository)),
) -> models.Message:
    message = message_repository.get_message_by_message_id(message_id)

    if message is None:
        raise NotFoundException(message="message_id not found")

    return message


@router.get(
    "/content/search",
    response_model=List[message_schema.MessagePublic],
    tags=[category],
)
def get_messages_content_and_room_id(
    content: str,
    room_id: int = None,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: GetMessagesByContentAndRoomIdService = Depends(
        GetMessagesByContentAndRoomIdService
    ),
) -> List[models.Message]:
    return service.get_messages_content_and_room_id(content, room_id, current_user.id)


@router.post(
    "/",
    response_model=message_schema.Message,
    tags=[category],
)
def create_message(
    new_message: message_schema.MessageCreate,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: CreateMessageService = Depends(CreateMessageService),
) -> models.Message:
    return service.create_message(new_message, current_user)


@router.delete(
    "/{message_id}",
    tags=[category],
)
def delete_message(
    message_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    message_repository: MessageRepository = Depends(get_repository(MessageRepository)),
) -> None:
    message = message_repository.get_message_by_message_id(message_id)

    if message is None:
        raise NotFoundException(message="message_id not found")

    message_repository.delete_message(message)


@router.put(
    "/{message_id}",
    response_model=message_schema.Message,
    tags=[category],
)
def update_message(
    message_id: int,
    new_content: message_schema.MessageUpdate,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: UpdateMessageService = Depends(UpdateMessageService),
):
    return service.update_message(message_id, new_content.content, current_user)


@router.get(
    "/threads/{thread_id}",
    response_model=thread_schema.Thread,
    tags=[category],
)
def get_thread_by_thread_id(
    thread_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: GetThreadByThreadIdService = Depends(GetThreadByThreadIdService),
) -> models.Thread:
    return service.get_thread_by_thread_id(thread_id, current_user.id)


@router.get(
    "/{message_id}/threads",
    response_model=List[thread_schema.Thread],
    tags=[category],
)
def get_threads_by_message_id(
    message_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: GetThreadByMessageIdService = Depends(GetThreadByMessageIdService),
) -> List[models.Thread]:
    return service.get_threads_by_message_id(message_id, current_user.id)


@router.post(
    "/{message_id}/threads", response_model=thread_schema.Thread, tags=[category]
)
def create_thread(
    message_id: int,
    thread: thread_schema.ThreadPublic,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: CreateThreadService = Depends(CreateThreadService),
) -> models.Thread:
    return service.create_thread(message_id, thread, current_user)


@router.put(
    "/threads/{thread_id}", response_model=thread_schema.Thread, tags=[category]
)
def update_thread(
    thread_id: int,
    thread: thread_schema.ThreadPublic,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: UpdateThreadByThreadAndUserIdService = Depends(
        UpdateThreadByThreadAndUserIdService
    ),
) -> models.Thread:
    return service.update_thread_by_thread_and_user_id(
        thread_id=thread_id, current_user_id=current_user.id, content=thread.content
    )


@router.delete(
    "/threads/{thread_id}", response_model=thread_schema.Thread, tags=[category]
)
def delete_thread(
    thread_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    thread_repository: ThreadRepository = Depends(get_repository(ThreadRepository)),
) -> None:
    thread = thread_repository.get_thread_by_thread_id(thread_id)
    if thread is None:
        raise NotFoundException(message="thread_id not found")

    return thread_repository.delete_thread(thread)
