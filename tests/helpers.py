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


def get_user_token(client, username, password) -> Response:
    token = login_user(client, username, password).json()
    return token['access_token']


def get_auth_headers(client, username=None, password=None) -> dict:
    headers = {}
    if (username and password):
        token = get_user_token(client, username, password)
        headers = {"authorization": "Bearer " + token}
    return headers


def create_url(client: TestClient, url, headers={}) -> Response:
    return client.post('/api/shortify', json={"long": url}, headers=headers)


def get_user_urls(client: TestClient, headers={}) -> Response:
    return client.get('/api/shortify', headers=headers)
