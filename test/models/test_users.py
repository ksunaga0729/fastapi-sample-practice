from fastapi_sample import models
from fastapi_sample.utils.password import get_password_hash


def test_verify_password():
    user_model = models.User()
    hash_password = get_password_hash("password")
    user_model.password = hash_password
    verify_password = user_model.verify_password(password="password")
    assert verify_password is True


def test_wrong_verify_password():
    user_model = models.User()
    hash_password = get_password_hash("password")
    user_model.password = hash_password
    verify_password = user_model.verify_password(password="password123")
    assert verify_password is False
