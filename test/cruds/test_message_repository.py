import pytest

from fastapi_sample.cruds import MessageRepository
from fastapi_sample.schemas import message as message_schema


@pytest.fixture
def message_repository(session):
    return MessageRepository(session)


@pytest.fixture
def seed_data(factory, test_user):
    user1 = test_user
    user2 = factory.User(username="Satoh", email="satoh@foo.com")
    room1 = factory.Room(name="room1")
    message1 = factory.Message(content="message1", user=user1, room=room1)
    factory.Message(content="message2", user=user1, room=room1)
    factory.Message(content="message3", user=user2, room=room1)
    factory.Member(user=user1, room=room1, member_role="host")
    factory.Member(user=user2, room=room1)

    return user1, message1


@pytest.fixture
def new_message():
    return message_schema.MessageCreate(room_id=1, content="message4")


class TestMessage:
    def test_get_messages(self, message_repository, seed_data):
        messages_list = message_repository.get_messages()
        assert len(messages_list) == 3
        assert set(messages.content for messages in messages_list) == {
            "message1",
            "message2",
            "message3",
        }

    def test_get_message_by_message_id(self, message_repository, seed_data):
        message = message_repository.get_message_by_message_id(message_id=1)
        assert message.content == "message1"

    def test_get_messages_by_userid(self, message_repository, seed_data):
        messages_list = message_repository.get_messages_by_userid(userid=1)
        assert len(messages_list) == 2
        assert set(messages.content for messages in messages_list) == {
            "message1",
            "message2",
        }

    def test_get_messages_by_room_id(self, message_repository, seed_data):
        messages_list = message_repository.get_messages_by_room_id(room_id=1)
        assert len(messages_list) == 3
        assert set(messages.content for messages in messages_list) == {
            "message1",
            "message2",
            "message3",
        }

    def test_get_message_by_message_and_room_id(self, message_repository, seed_data):
        message = message_repository.get_message_by_message_and_room_id(
            message_id=1, room_id=1
        )
        assert message.content == "message1"

    def test_get_messages_by_content_and_room_id(self, message_repository, seed_data):
        messages_list = message_repository.get_messages_by_content_and_room_id(
            content="message", room_id=1
        )
        assert len(messages_list) == 3
        assert set(messages.content for messages in messages_list) == {
            "message1",
            "message2",
            "message3",
        }

    def test_create_message(self, seed_data, message_repository, new_message):
        user1 = seed_data[0]
        message = message_repository.create_message(new_message, user1)
        assert message.content == "message4"
        assert message.room_id == 1

    def test_delete_message(self, seed_data, message_repository):
        message = seed_data[1]
        assert message_repository.delete_message(message) is None

    def test_update_message_by_message_id(self, seed_data, message_repository):
        new_message = seed_data[1]
        new_message.content = "update_message"
        message = message_repository.update_message_by_message_id(message=new_message)
        assert message.content == "update_message"

    def test_update_read_time(self, seed_data, message_repository):
        assert message_repository.update_read_time(message_id=1) is None
