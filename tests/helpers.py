from fastapi.testclient import TestClient
from fastapi.responses import Response


def create_user(client: TestClient, username, password) -> Response:
    return client.post(
        '/api/users', json={"username": username, "password": password}
    )


def login_user(client: TestClient, username, password) -> Response:
    return client.post(
        '/login', data={"username": username, "password": password}
    )
