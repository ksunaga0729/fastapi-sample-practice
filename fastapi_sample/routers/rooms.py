from typing import List

from fastapi import APIRouter, Depends

from fastapi_sample import models
from fastapi_sample.cruds import RoomRepository, UserRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.schemas import member as member_schema
from fastapi_sample.schemas import room as room_schema
from fastapi_sample.schemas import user as user_schema
from fastapi_sample.services import (
    CreateMemberService,
    DeleteMemberService,
    GetMessagesByRoomAndMessageIdService,
    GetMessagesByRoomIdService,
    JoinMemberService,
    NotFoundException,
    UpdateReadTimeService,
    authentication,
)

router = APIRouter(
    prefix="/rooms",
    responses={404: {"description": "Not found"}},
)

category = "rooms"


@router.post(
    "/",
    response_model=room_schema.Room,
    tags=[category],
)
def create_room_and_member(
    new_room: room_schema.RoomCreate,
    current_user: models.User = Depends(authentication.get_current_active_user),
    room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
) -> models.Room:
    room = room_repository.create_room_and_member(new_room, current_user)
    return room


@router.get("/", response_model=List[room_schema.Room], tags=[category])
def get_rooms(
    current_user: models.User = Depends(authentication.get_current_active_user),
    room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
) -> List[models.Room]:
    return room_repository.get_rooms()


@router.get("/{room_id}", response_model=room_schema.RoomPublic, tags=[category])
def get_room_by_room_id(
    room_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
) -> models.Room:
    room = room_repository.get_room_by_room_id(room_id)
    if room is None:
        raise NotFoundException(message="room_id not found")

    return room


@router.get(
    "/{room_id}/messages",
    response_model=List[room_schema.MessageInRoom],
    tags=[category],
)
def get_messages_by_room_id(
    room_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: GetMessagesByRoomIdService = Depends(GetMessagesByRoomIdService),
) -> List[models.Message]:
    return service.get_messages_by_room_id(room_id, current_user.id)


@router.get(
    "/{room_id}/messages/{message_id}",
    response_model=room_schema.MessageInRoom,
    tags=[category],
)
def get_message_by_room_and_message_id(
    message_id: int,
    room_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: GetMessagesByRoomAndMessageIdService = Depends(
        GetMessagesByRoomAndMessageIdService
    ),
) -> models.Message:
    return service.get_message_by_room_and_message_id(
        room_id, message_id, current_user.id
    )


@router.post(
    "/{room_id}/users",
    response_model=member_schema.MemberCreate,
    tags=[category],
)
def create_member(
    room_id: int,
    user_name: user_schema.UserName,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: CreateMemberService = Depends(CreateMemberService),
) -> models.Member:
    return service.create_member(room_id, user_name.username, current_user)


@router.post(
    "/{room_id}/users/join",
    response_model=member_schema.MemberCreate,
    tags=[category],
)
def join_member(
    room_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: JoinMemberService = Depends(JoinMemberService),
) -> models.Member:
    return service.join_member(room_id, current_user)


@router.get(
    "/{room_id}/users",
    response_model=List[user_schema.UserPublic],
    tags=[category],
)
def get_users_by_room_id(
    room_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
    room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
) -> List[models.User]:
    if not room_repository.get_room_by_room_id(room_id):
        raise NotFoundException(message="room_id not found")
    users_list = user_repository.get_users_by_room_id(room_id)

    return users_list


@router.put(
    "/{room_id}/read",
    tags=[category],
)
def update_read_time(
    room_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: UpdateReadTimeService = Depends(UpdateReadTimeService),
):
    service.update_read_time(room_id, current_user.id)


@router.delete("/{room_id}/{user_id}", tags=[category])
def delete_member(
    room_id: int,
    user_id: int,
    current_user: models.User = Depends(authentication.get_current_active_user),
    service: DeleteMemberService = Depends(DeleteMemberService),
) -> None:
    return service.delete_member(
        room_id=room_id, user_id=user_id, current_user_id=current_user.id
    )
