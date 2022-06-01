import pytest

from fastapi_sample.cruds import MemberRepository, RoomRepository


@pytest.fixture
def room_repository(session):
    return RoomRepository(session)


@pytest.fixture
def member_repository(session):
    return MemberRepository(session)


@pytest.fixture
def seed_data(factory, test_user):
    user1 = test_user
    user2 = factory.User(username="Satoh", email="satoh@example.com")
    room1 = factory.Room(name="room1")
    room2 = factory.Room(name="room2")
    factory.Member(user=user1, room=room1, member_role="host")
    factory.Member(user=user1, room=room2, member_role="host")
    factory.Member(user=user2, room=room1)


class TestMember:
    def test_delete_member(self, seed_data, room_repository, member_repository):
        member = room_repository.get_member_by_room_and_user_id(room_id=1, user_id=2)
        del_member = member_repository.delete_member(member)
        assert del_member is None
