import pytest
from fastapi import FastAPI, status
from starlette.testclient import TestClient

from fastapi_sample.schemas import message as message_schema
from fastapi_sample.schemas import thread as thread_schema


@pytest.fixture
def seed_data(factory, test_user):
    user1 = test_user
    user2 = factory.User(username="Satoh", email="satoh@xample.com")
    room1 = factory.Room(name="room1")
    room2 = factory.Room(name="room2")
    message1 = factory.Message(content="message1", user=user1, room=room1)
    factory.Message(content="message2", user=user2, room=room1)
    message3 = factory.Message(content="message3", user=user2, room=room2)
    factory.Member(user=user1, room=room1)
    factory.Member(user=user2, room=room1)
    factory.Member(user=user2, room=room2)
    factory.Thread(content="thread1", user=user1, message=message1)
    factory.Thread(content="thread2", user=user2, message=message1)
    factory.Thread(content="thread3", user=user2, message=message3)


@pytest.fixture
def new_message():
    return message_schema.MessageCreate(
        content="message3",
        room_id=1,
    )


@pytest.fixture
def update_message():
    return message_schema.MessageUpdate(
        content="edit_message",
    )


@pytest.fixture
def new_thread():
    return thread_schema.ThreadPublic(content="new_threads")


@pytest.fixture
def update_thread():
    return thread_schema.ThreadPublic(content="message3")


class TestMessage:
    def test_get_messages(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        response = client.get(app.url_path_for("get_messages"), headers=token_header)
        assert response.status_code == status.HTTP_200_OK
        message = response.json()
        assert len(message) > 0

    def test_create_message(
        self,
        app: FastAPI,
        client: TestClient,
        new_message: message_schema.MessageCreate,
        token_header,
        seed_data,
    ):
        response = client.post(
            app.url_path_for("create_message"),
            json=new_message.dict(),
            headers=token_header,
        )
        assert response.status_code == status.HTTP_200_OK

    def test_delete_message(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        message_id = 2
        response = client.delete(f"/messages/{message_id}", headers=token_header)
        assert response.status_code == status.HTTP_200_OK

    def test_get_message_by_message_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        message_id = 1
        response = client.get(f"/messages/{message_id}", headers=token_header)
        assert response.status_code == status.HTTP_200_OK

    def test_update_message(
        self,
        app: FastAPI,
        client: TestClient,
        update_message: message_schema.MessageUpdate,
        token_header,
        seed_data,
    ):
        message_id = 1
        response = client.put(
            f"/messages/{message_id}",
            json=update_message.dict(),
            headers=token_header,
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_messages_content_and_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 1
        response = client.get(
            "/messages/content/search",
            params={"content": "message", "room_id": room_id},
            headers=token_header,
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_messages_content_and_none(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        response = client.get(
            "/messages/content/search",
            params={"content": "message", "room_id": None},
            headers=token_header,
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_threads(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        response = client.get("/messages/threads", headers=token_header)
        assert response.status_code == status.HTTP_200_OK
        threads_list = response.json()
        assert len(threads_list) > 0

    def test_get_threads_message_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        message_id = 1
        response = client.get(f"/messages/{message_id}/threads", headers=token_header)
        assert response.status_code == status.HTTP_200_OK
        threads_list = response.json()
        assert len(threads_list) == 2

    def test_get_thread_by_thread_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        thread_id = 1
        thread = client.get(f"/messages/threads/{thread_id}", headers=token_header)
        results = thread.json()
        assert thread.status_code == status.HTTP_200_OK
        assert results["content"] == "thread1"

    def test_create_thread(
        self, app: FastAPI, client: TestClient, token_header, seed_data, new_thread
    ):
        message_id = 1
        response = client.post(
            f"/messages/{message_id}/threads",
            json=new_thread.dict(),
            headers=token_header,
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_thread(
        self, app: FastAPI, client: TestClient, token_header, seed_data, update_thread
    ):
        thread_id = 1
        response = client.put(
            f"/messages/threads/{thread_id}",
            json=update_thread.dict(),
            headers=token_header,
        )
        assert response.status_code == status.HTTP_200_OK

    def test_delete_thread(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        thread_id = 1
        response = client.delete(f"/messages/threads/{thread_id}", headers=token_header)
        assert response.status_code == status.HTTP_200_OK


class TestMessageError:
    def test_get_message_by_message_id_404_message_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        message_id = 4
        response = client.get(f"/messages/{message_id}", headers=token_header)
        error_message = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert error_message["message"] == "message_id not found"

    def test_delete_message_404_message_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        message_id = 5
        response = client.delete(f"/messages/{message_id}", headers=token_header)
        error_message = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert error_message["message"] == "message_id not found"

    def test_create_message_404_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        response = client.post(
            app.url_path_for("create_message"),
            json={"content": "test", "room_id": "5"},
            headers=token_header,
        )
        error_message = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert error_message["message"] == "room_id not found"

    def test_create_message_403_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        response = client.post(
            app.url_path_for("create_message"),
            json={"content": "message3", "room_id": "2"},
            headers=token_header,
        )
        error_message = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert error_message["message"] == "You don't belong to the specified room"

    def test_update_message_404_message_id(
        self,
        app: FastAPI,
        client: TestClient,
        update_message: message_schema.MessageUpdate,
        token_header,
        seed_data,
    ):
        message_id = 5
        response = client.put(
            f"/messages/{message_id}",
            json=update_message.dict(),
            headers=token_header,
        )
        error_message = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert error_message["message"] == "message_id not found"

    def test_update_message_403_message_id(
        self,
        app: FastAPI,
        client: TestClient,
        update_message: message_schema.MessageUpdate,
        token_header,
        seed_data,
    ):
        message_id = 3
        response = client.put(
            f"/messages/{message_id}",
            json=update_message.dict(),
            headers=token_header,
        )
        error_message = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert error_message["message"] == "It's not a message you sent."

    @pytest.mark.parametrize(
        "content, room_id",
        (
            (
                "message4444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444",
                1,
            ),
            ("", 1),
        ),
    )
    def test_create_message_422_max_min_length_content(
        self,
        app: FastAPI,
        client: TestClient,
        token_header,
        seed_data,
        content,
        room_id,
    ):
        response = client.post(
            app.url_path_for("create_message"),
            json={"content": content, "room_id": room_id},
            headers=token_header,
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_messages_content_and_room_id_404_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 5
        response = client.get(
            "/messages/content/search",
            params={"content": "message", "room_id": room_id},
            headers=token_header,
        )
        error_message = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert error_message["message"] == "room_id not found"

    def test_get_messages_content_and_room_id_403_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        room_id = 2
        response = client.get(
            "/messages/content/search",
            params={"content": "message", "room_id": room_id},
            headers=token_header,
        )
        error_message = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert error_message["message"] == "You don't belong to the specified room"

    def test_get_thread_by_thread_id_404_thread_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        thread_id = 5
        thread = client.get(f"/messages/threads/{thread_id}", headers=token_header)
        error_message = thread.json()
        assert thread.status_code == status.HTTP_404_NOT_FOUND
        assert error_message["message"] == "thread_id not found"

    def test_get_thread_by_thread_id_403_thread_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        thread_id = 3
        thread = client.get(f"/messages/threads/{thread_id}", headers=token_header)
        error_message = thread.json()
        assert thread.status_code == status.HTTP_403_FORBIDDEN
        assert error_message["message"] == "You don't belong to the specified room"

    def test_create_thread_404_message_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data, new_thread
    ):
        message_id = 4
        response = client.post(
            f"/messages/{message_id}/threads",
            json=new_thread.dict(),
            headers=token_header,
        )
        error_message = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert error_message["message"] == "message_id not found"

    def test_create_thread_403_message_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data, new_thread
    ):
        message_id = 3
        response = client.post(
            f"/messages/{message_id}/threads",
            json=new_thread.dict(),
            headers=token_header,
        )
        error_message = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert error_message["message"] == "You don't belong to the specified room"

    def test_update_thread_404_thread_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        thread_id = 5
        response = client.put(
            f"/messages/threads/{thread_id}",
            json={"content": "error_message"},
            headers=token_header,
        )
        error_message = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert error_message["message"] == "thread_id not found"

    def test_update_thread_403_room_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        thread_id = 2
        response = client.put(
            f"/messages/threads/{thread_id}",
            json={"content": "error_message"},
            headers=token_header,
        )
        error_message = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert error_message["message"] == "You don't belong to the specified room"

    def test_delete_thread_404_thread_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        thread_id = 5
        response = client.delete(f"/messages/threads/{thread_id}", headers=token_header)
        error_message = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert error_message["message"] == "thread_id not found"

    def test_get_threads_message_id_404_message_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        message_id = 4
        response = client.get(f"/messages/{message_id}/threads", headers=token_header)
        error_message = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert error_message["message"] == "message_id not found"

    def test_get_threads_message_id_403_message_id(
        self, app: FastAPI, client: TestClient, token_header, seed_data
    ):
        message_id = 3
        response = client.get(f"/messages/{message_id}/threads", headers=token_header)
        error_message = response.json()
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert error_message["message"] == "You don't belong to the specified room"
