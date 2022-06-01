import pytest

from fastapi_sample.cruds import ThreadRepository


@pytest.fixture
def thread_repository(session):
    return ThreadRepository(session)


@pytest.fixture
def seed_data(factory, test_user):
    user1 = test_user
    room1 = factory.Room(name="room1")
    message1 = factory.Message(content="message1", user=user1, room=room1)
    message2 = factory.Message(content="message2", user=user1, room=room1)
    thread1 = factory.Thread(content="thread1", user=user1, message=message1)
    factory.Thread(content="thread2", user=user1, message=message1)
    factory.Thread(content="thread3", user=user1, message=message2)
    factory.Thread(content="thread4", user=user1, message=message2)
    return user1, thread1


class TestThread:
    def test_get_thread_by_thread_id(self, thread_repository, seed_data):
        thread = thread_repository.get_thread_by_thread_id(thread_id=1)
        assert thread.content == "thread1"

    def test_create_thread(self, thread_repository, seed_data):
        thread_list = thread_repository.create_thread(
            message_id=1, content="message2", user=seed_data[0]
        )
        assert thread_list.content == "message2"

    def test_update_thread_by_message_id_and_thread_id(
        self, thread_repository, seed_data
    ):
        thread = thread_repository.update_thread_by_thread_and_user_id(
            seed_data[1], content="update-message1"
        )
        assert thread.content == "update-message1"

    def test_get_threads(self, thread_repository, seed_data):
        threads_list = thread_repository.get_threads()
        assert len(threads_list) == 4
        assert set(threads.content for threads in threads_list) == {
            "thread1",
            "thread2",
            "thread3",
            "thread4",
        }

    def test_get_threads_message_id(self, thread_repository, seed_data):
        threads_list = thread_repository.get_threads_message_id(message_id=2)
        assert len(threads_list) == 2
        assert set(threads.content for threads in threads_list) == {
            "thread3",
            "thread4",
        }

    def test_delete_thread(self, thread_repository, seed_data):
        thread = thread_repository.get_thread_by_thread_id(thread_id=1)
        del_thread = thread_repository.delete_thread(thread)
        assert del_thread is None
