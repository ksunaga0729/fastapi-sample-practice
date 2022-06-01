import pytest
from fastapi import FastAPI, status
from starlette.testclient import TestClient


@pytest.fixture
def seed_data(factory, test_user):
    user1 = test_user
    factory.User(username="Satoh", email="satoh@xample.com")
    room1 = factory.Room(name="room1")
    factory.Message(content="message1", user=user1, room=room1)


class TestUsers:
    def test_read_users(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        response = client.get(app.url_path_for("read_users"), headers=token_header)
        assert response.status_code == status.HTTP_200_OK

    def test_read_user(self, app: FastAPI, client: TestClient, token_header, seed_data):
        user_id = 1
        response = client.get(f"/users/{user_id}", headers=token_header)
        assert response.status_code == status.HTTP_200_OK

    def test_get_current_user(
        self, app: FastAPI, client: TestClient, token_header, test_user
    ):
        response = client.get(
            app.url_path_for("get_current_user"), headers=token_header
        )
        current_user = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert current_user["username"] == test_user.username
        assert current_user["email"] == test_user.email

    def test_get_messages_by_user_id(
        self, app: FastAPI, client: TestClient, token_header, test_user
    ):
        user_id = 1
        response = client.get(f"/users/{user_id}/messages", headers=token_header)
        assert response.status_code == status.HTTP_200_OK


class TestUsersError:
    def test_read_user_404_user_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        user_id = 5
        response = client.get(f"/users/{user_id}", headers=token_header)
        assert response.status_code == 404
        assert response.json() == {"message": "User not found"}

    def test_get_messages_by_user_id_404_user_id(
        self, app: FastAPI, client: TestClient, token_header, test_user
    ):
        user_id = 2
        response = client.get(f"/users/{user_id}/messages", headers=token_header)
        results = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert results["message"] == "user_id not found"
