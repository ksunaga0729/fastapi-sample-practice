import pytest

from fastapi_sample.cruds import RoomRepository
from fastapi_sample.schemas import room as room_schema


@pytest.fixture
def room_repository(session):
    return RoomRepository(session)


@pytest.fixture
def seed_data(factory, test_user):
    user1 = test_user
    user2 = factory.User(username="Satoh", email="satoh@example.com")
    room1 = factory.Room(name="room1")
    room2 = factory.Room(name="room2")
    member1 = factory.Member(user=user1, room=room1, member_role="host")
    factory.Member(user=user1, room=room2, member_role="host")
    factory.Member(user=user2, room=room1)

    return user1, user2, member1


@pytest.fixture
def new_room():
    return room_schema.RoomCreate(name="room3")


class TestRoom:
    def test_get_room_by_user_id(self, seed_data, room_repository):
        user1, user2 = seed_data[0], seed_data[1]
        user1_rooms = room_repository.get_room_by_user_id(user1.id)
        assert len(user1_rooms) == 2
        assert set(room.name for room in user1_rooms) == {"room1", "room2"}

        user2_room = room_repository.get_room_by_user_id(user2.id)
        assert len(user2_room) == 1
        assert set(room.name for room in user2_room) == {"room1"}

    def test_update_read_time(self, seed_data, room_repository):
        assert room_repository.update_read_time(seed_data[2]) is None

    def test_get_rooms(self, seed_data, room_repository):
        return_rooms = room_repository.get_rooms()
        assert len(return_rooms) == 2
        assert set(room.name for room in return_rooms) == {"room1", "room2"}

    def test_get_room_by_room_id(self, seed_data, room_repository):
        return_room = room_repository.get_room_by_room_id(room_id=1)
        assert return_room.id == 1
        assert return_room.name == "room1"

    def test_role_check(self, seed_data, room_repository):
        user1 = seed_data[0]
        return_role = room_repository.role_check(room_id=1, user=user1)
        assert return_role.member_role == "host"

    def test_create_member(self, seed_data, room_repository):
        return_member = room_repository.create_member(room_id=1, user_id=3)
        assert return_member.room_id == 1
        assert return_member.user_id == 3
        assert return_member.member_role == "general"

    def test_get_member_by_room_and_user_id(self, seed_data, room_repository):
        return_member = room_repository.get_member_by_room_and_user_id(
            room_id=1, user_id=2
        )
        assert return_member is not None

    def test_create_room_and_member(self, seed_data, room_repository, new_room):
        user1 = seed_data[0]
        return_room = room_repository.create_room_and_member(new_room, user1)
        assert return_room.id == 3
        assert return_room.name == "room3"
