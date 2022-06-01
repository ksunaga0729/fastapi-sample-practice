import pytest
from fastapi import FastAPI, status
from starlette.testclient import TestClient


@pytest.fixture
def seed_data(factory, test_user):
    user1 = test_user
    factory.User(username="Satoh", email="satoh@xample.com")
    room1 = factory.Room(name="room1")
    room2 = factory.Room(name="room2")
    factory.Member(user=user1, room=room1, member_role="host")
    factory.Member(user=user1, room=room2)


class TestUsersRoom:
    @pytest.mark.parametrize("username", ("Yamada", None))
    def test_get_rooms_by_username(
        self, app: FastAPI, client: TestClient, token_header, seed_data, username
    ):
        response = client.get(
            app.url_path_for("get_rooms_by_username"),
            headers=token_header,
            params={"username": username},
        )
        assert response.status_code == status.HTTP_200_OK


class TestUsersRoomError:
    def test_get_rooms_by_username_404_username(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        response = client.get(
            app.url_path_for("get_rooms_by_username"),
            headers=token_header,
            params={"username": "username"},
        )
        results = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert results["message"] == "username not found"

    def test_get_rooms_by_username_404_room(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        response = client.get(
            app.url_path_for("get_rooms_by_username"),
            headers=token_header,
            params={"username": "Satoh"},
        )
        results = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert results["message"] == "room not found"
