import pytest
from pydantic import EmailStr

from fastapi_sample.cruds import UserRepository
from fastapi_sample.schemas import user as user_schema


@pytest.fixture
def user_repository(session):
    return UserRepository(session)


@pytest.fixture
def seed_data(factory, test_user):
    user1 = test_user
    user2 = factory.User(username="Satoh", email="satoh@example.com")
    room1 = factory.Room(name="room1")
    factory.Member(user=user1, room=room1, member_role="host")
    factory.Member(user=user2, room=room1)

    return user1


class TestUser:
    def test_get_user_by_email(self, user_repository, seed_data):
        user1 = seed_data
        users_list = user_repository.get_user_by_email(user1.email)
        assert users_list.username == "Yamada"

    def test_create_user(self, user_repository, seed_data):
        user = user_schema.UserCreate(
            username="Tanaka", email=EmailStr("tanaka@example.com"), password="password"
        )
        users_list = user_repository.create_user(user)
        assert users_list.username == "Tanaka"
        assert users_list.password != "password"

    def test_get_users(self, user_repository, seed_data):
        users_list = user_repository.get_users()
        assert len(users_list) == 2
        assert set(users.username for users in users_list) == {"Yamada", "Satoh"}

    def test_get_user_by_user_id(self, user_repository, seed_data):
        users_list = user_repository.get_user_by_user_id(user_id=1)
        assert users_list.username == "Yamada"

    def test_get_user_by_username(self, user_repository, seed_data):
        users_list = user_repository.get_user_by_username(username="Yamada")
        assert users_list.username == "Yamada"

    def test_get_users_by_room_id(self, user_repository, seed_data):
        users_list = user_repository.get_users_by_room_id(room_id=1)
        assert len(users_list) == 2
        assert set(users.username for users in users_list) == {"Yamada", "Satoh"}
