from fastapi import Depends

from fastapi_sample.cruds import MemberRepository, RoomRepository, UserRepository
from fastapi_sample.dependencies.database import get_repository
from fastapi_sample.services.exceptions import ForbiddenException, NotFoundException


class DeleteMemberService:
    def __init__(
        self,
        room_repository: RoomRepository = Depends(get_repository(RoomRepository)),
        user_repository: UserRepository = Depends(get_repository(UserRepository)),
        member_repository: MemberRepository = Depends(get_repository(MemberRepository)),
    ):
        self.__room_repository = room_repository
        self.__user_repository = user_repository
        self.__member_repository = member_repository

    def delete_member(self, room_id: int, user_id: int, current_user_id: int):
        user = self.__user_repository.get_user_by_user_id(user_id)
        if user is None:
            raise NotFoundException(message="user_id not found")

        room = self.__room_repository.get_room_by_room_id(room_id)
        if room is None:
            raise NotFoundException(message="room_id not found")

        member = self.__room_repository.get_member_by_room_and_user_id(
            room_id=room_id, user_id=current_user_id
        )

        if member is None:
            raise ForbiddenException(message="You don't belong to the specified room")

        if member.member_role == "host" and user_id == current_user_id:
            raise ForbiddenException(
                message="You have the host role in this room,so you cannot delete yourself"
            )

        if member.member_role == "general" and user_id != current_user_id:
            raise ForbiddenException(
                message="You don't have the host role to delete the user"
            )

        del_member = self.__room_repository.get_member_by_room_and_user_id(
            room_id=room_id, user_id=user_id
        )
        if del_member is None:
            raise ForbiddenException(
                message="The user_id don't belong to the specified room"
            )

        return self.__member_repository.delete_member(del_member)
