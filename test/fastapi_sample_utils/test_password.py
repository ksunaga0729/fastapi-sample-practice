from fastapi_sample.utils.password import get_password_hash


def test_get_password_hash():
    password_hash = get_password_hash("password")
    assert type(password_hash) == str
    assert password_hash != "password"
