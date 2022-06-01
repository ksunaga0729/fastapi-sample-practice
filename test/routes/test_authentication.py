import pytest
from fastapi import FastAPI, status
from pydantic import EmailStr
from starlette.testclient import TestClient

from fastapi_sample import models
from fastapi_sample.schemas import user as user_schema


@pytest.fixture
def new_user():
    return user_schema.UserCreate(
        username="Tanaka",
        email=EmailStr("tanaka@example.com"),
        password="password",
    )


class TestUser:
    def test_sign_up(
        self, app: FastAPI, client: TestClient, new_user: user_schema.UserCreate
    ):
        response = client.post(
            app.url_path_for("sign_up"), json={"new_user": new_user.dict()}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_sign_in(self, app: FastAPI, client: TestClient, test_user: models.User):
        login_data = {
            "username": test_user.username,
            "password": "password",
        }
        response = client.post(app.url_path_for("sign_in"), data=login_data)
        token = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in token
        assert token["access_token"]


class TestUserError:
    @pytest.mark.parametrize(
        "username, password",
        (("username", "password"), ("Tanaka", "password")),
    )
    def test_sign_in_401_user(
        self,
        app: FastAPI,
        client: TestClient,
        test_user: models.User,
        username,
        password,
    ):
        login_data = {
            "username": username,
            "password": password,
        }
        response = client.post(app.url_path_for("sign_in"), data=login_data)
        results = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert results["detail"] == "Authentication was unsuccessful."
