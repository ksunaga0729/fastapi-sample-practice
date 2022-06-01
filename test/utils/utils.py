from typing import Dict

from fastapi.testclient import TestClient

from fastapi_sample import models


def create_token_header(client: TestClient, user: models.User) -> Dict:
    login_data = {
        "username": user.username,
        "password": "password",
    }
    response = client.post("/authentication/sign_in", data=login_data)
    result = response.json()
    token = result["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers
