import pytest
from fastapi import FastAPI, status
from starlette.testclient import TestClient

from fastapi_sample.schemas import room as room_schema
from fastapi_sample.schemas import user as user_schema


@pytest.fixture
def seed_data(factory, test_user):
    user1 = test_user
    user2 = factory.User(username="Satoh", email="satoh@xample.com")
    room1 = factory.Room(name="room1")
    room2 = factory.Room(name="room2")
    room3 = factory.Room(name="room3")
    room4 = factory.Room(name="room4")
    factory.Member(user=user1, room=room1, member_role="host")
    factory.Member(user=user2, room=room2, member_role="host")
    factory.Member(user=user2, room=room1, member_role="host")
    factory.Member(user=user1, room=room3, member_role="host")
    factory.Member(user=user1, room=room4, member_role="general")
    factory.Member(user=user2, room=room4, member_role="general")
    factory.Message(content="message1", user=user1, room=room1)


@pytest.fixture
def new_room():
    return room_schema.RoomCreate(
        name="room5",
    )


@pytest.fixture
def new_member():
    return user_schema.UserName(
        username="Satoh",
    )


@pytest.fixture
def new_member_error():
    return user_schema.UserName(
        username="Satoh_error",
    )


class TestRoom:
    def test_get_rooms(self, app: FastAPI, client: TestClient, token_header, seed_data):
        response = client.get(app.url_path_for("get_rooms"), headers=token_header)
        assert response.status_code == status.HTTP_200_OK
        rooms = response.json()
        assert len(rooms) > 0

    def test_get_room_by_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 1
        response = client.get(f"/rooms/{room_id}", headers=token_header)
        assert response.status_code == status.HTTP_200_OK

    def test_create_room_and_member(
        self,
        app: FastAPI,
        client: TestClient,
        new_room: room_schema.RoomCreate,
        token_header,
        seed_data,
    ):
        response = client.post(
            app.url_path_for("create_room_and_member"),
            json=new_room.dict(),
            headers=token_header,
        )
        assert response.status_code == status.HTTP_200_OK

    def test_create_member(
        self,
        app: FastAPI,
        client: TestClient,
        new_member: user_schema.UserName,
        token_header,
        seed_data,
    ):
        room_id = 3
        response = client.post(
            f"/rooms/{room_id}/users", json=new_member.dict(), headers=token_header
        )
        assert response.status_code == status.HTTP_200_OK

    def test_join_member(
        self,
        app: FastAPI,
        client: TestClient,
        token_header,
        seed_data,
    ):
        room_id = 2
        response = client.post(f"/rooms/{room_id}/users/join", headers=token_header)
        assert response.status_code == status.HTTP_200_OK

    def test_get_messages_by_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 1
        response = client.get(f"rooms/{room_id}/messages", headers=token_header)
        assert response.status_code == status.HTTP_200_OK

    def test_get_message_by_room_and_message_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 1
        message_id = 1
        response = client.get(
            f"rooms/{room_id}/messages/{message_id}", headers=token_header
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_users_by_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 1
        response = client.get(f"rooms/{room_id}/users", headers=token_header)
        assert response.status_code == status.HTTP_200_OK

    def test_update_read_time(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 1
        response = client.put(f"rooms/{room_id}/read", headers=token_header)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_member_host(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 1
        user_id = 2
        response = client.delete(f"rooms/{room_id}/{user_id}", headers=token_header)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_member_general(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 4
        user_id = 1
        response = client.delete(f"rooms/{room_id}/{user_id}", headers=token_header)
        assert response.status_code == status.HTTP_200_OK


class TestRoomError:
    def test_get_room_by_room_id_404_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 5
        response = client.get(f"/rooms/{room_id}", headers=token_header)
        assert response.status_code == 404
        assert response.json() == {"message": "room_id not found"}

    def test_get_messages_by_room_id_404_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 5
        response = client.get(f"rooms/{room_id}/messages", headers=token_header)
        messages_list = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert messages_list["message"] == "room_id not found"

    def test_get_messages_by_room_id_403_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 2
        response = client.get(f"rooms/{room_id}/messages", headers=token_header)
        message_list = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert message_list["message"] == "You don't belong to the specified room"

    @pytest.mark.parametrize(
        "room_id, message_id",
        ((3, 1), (1, 2)),
    )
    def test_get_message_by_room_and_message_id_404_room_and_message_id(
        self,
        app: FastAPI,
        client: TestClient,
        token_header,
        seed_data,
        room_id,
        message_id,
    ):
        response = client.get(
            f"rooms/{room_id}/messages/{message_id}", headers=token_header
        )
        messages_list = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND

        if room_id == 2 and message_id == 1:
            assert messages_list["message"] == "room_id not found"
        elif room_id == 1 and message_id == 2:
            assert messages_list["message"] == "message not found"

    def test_get_message_by_room_and_message_id_403_room_id(
        self,
        app: FastAPI,
        client: TestClient,
        token_header,
        seed_data,
    ):
        room_id = 2
        message_id = 1
        response = client.get(
            f"rooms/{room_id}/messages/{message_id}", headers=token_header
        )
        results = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert results["message"] == "You don't belong to the specified room"

    def test_get_users_by_room_id_404_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 5
        response = client.get(f"rooms/{room_id}/users", headers=token_header)
        users_list = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert users_list["message"] == "room_id not found"

    def test_update_read_time_404_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 5
        response = client.put(f"rooms/{room_id}/read", headers=token_header)
        rooms_list = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert rooms_list["message"] == "room_id not found"

    def test_update_read_time_403_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 2
        response = client.put(f"rooms/{room_id}/read", headers=token_header)
        rooms_list = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert rooms_list["message"] == "You don't belong to the specified room"

    def test_create_member_404_room_id(
        self,
        app: FastAPI,
        client: TestClient,
        new_member_error: user_schema.UserName,
        token_header,
        seed_data,
    ):
        room_id = 5
        response = client.post(
            f"/rooms/{room_id}/users",
            json=new_member_error.dict(),
            headers=token_header,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"message": "room_id not found"}

    def test_create_member_409_room_id_and_user(
        self,
        app: FastAPI,
        client: TestClient,
        new_member: user_schema.UserName,
        token_header,
        seed_data,
    ):
        room_id = 1
        response = client.post(
            f"/rooms/{room_id}/users", json=new_member.dict(), headers=token_header
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == {"message": "user already joined to room"}

    def test_create_member_403_room_id(
        self,
        app: FastAPI,
        client: TestClient,
        new_member: user_schema.UserName,
        token_header,
        seed_data,
    ):
        room_id = 2
        response = client.post(
            f"/rooms/{room_id}/users", json=new_member.dict(), headers=token_header
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"message": "Permission denied"}

    def test_join_member_404_room_id(
        self,
        app: FastAPI,
        client: TestClient,
        token_header,
        seed_data,
    ):
        room_id = 5
        response = client.post(f"/rooms/{room_id}/users/join", headers=token_header)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"message": "room_id not found"}

    def test_join_member_409_conflict(
        self,
        app: FastAPI,
        client: TestClient,
        token_header,
        seed_data,
    ):
        room_id = 1
        response = client.post(f"/rooms/{room_id}/users/join", headers=token_header)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == {"message": "user already joined to room"}

    @pytest.mark.parametrize(
        "name",
        (
            "room1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
            "",
        ),
    )
    def test_schema_room_create_422_max_min_length_name(
        self, app: FastAPI, client: TestClient, token_header, seed_data, name
    ):
        response = client.post(
            app.url_path_for("create_room_and_member"),
            json={"name": name},
            headers=token_header,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_member_404_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 100
        user_id = 1
        response = client.delete(f"rooms/{room_id}/{user_id}", headers=token_header)
        error_message = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert error_message["message"] == "room_id not found"

    def test_delete_member_404_user_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 1
        user_id = 100
        response = client.delete(f"rooms/{room_id}/{user_id}", headers=token_header)
        error_message = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert error_message["message"] == "user_id not found"

    def test_delete_member_403_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 2
        user_id = 1
        response = client.delete(f"rooms/{room_id}/{user_id}", headers=token_header)
        error_message = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert error_message["message"] == "You don't belong to the specified room"

    # hostユーザーが自分自身を削除する場合
    def test_delete_member_403_host_user_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 1
        user_id = 1
        response = client.delete(f"rooms/{room_id}/{user_id}", headers=token_header)
        error_message = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            error_message["message"]
            == "You have the host role in this room,so you cannot delete yourself"
        )

    # generalユーザーが他のユーザーを削除する場合
    def test_delete_member_403_general_user_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 4
        user_id = 2
        response = client.delete(f"rooms/{room_id}/{user_id}", headers=token_header)
        error_message = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            error_message["message"]
            == "You don't have the host role to delete the user"
        )

    def test_delete_member_403_user_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 3
        user_id = 2
        response = client.delete(f"rooms/{room_id}/{user_id}", headers=token_header)
        error_message = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            error_message["message"] == "The user_id don't belong to the specified room"
        )
