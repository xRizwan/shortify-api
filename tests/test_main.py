from fastapi.testclient import TestClient
from fastapi.responses import Response
from main import app
from db_setup import test_db
from utils import create_access_token
from .helpers import create_user, login_user

client = TestClient(app)


def test_create_user(test_db):
    test_username = "testeruser1"
    test_password = "testpassword123"
    response = create_user(client, test_username, test_password)

    assert response.status_code == 200
    assert response.json()['username'] == test_username


def test_login(test_db):
    test_username = "testeruser1"
    test_password = "testpassword123"
    create_user(client, test_username, test_password)
    response = login_user(client, test_username, test_password)

    assert response.status_code == 200
    assert response.json()['access_token'] == create_access_token(
        test_username
    )


def test_shorten_url(test_db):
    url = "www.google.com"
    response = client.post('/api/shortify', json={"long": url})

    assert response.status_code == 200
    assert response.json()['long'] == url
