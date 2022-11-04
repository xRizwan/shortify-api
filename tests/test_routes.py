from fastapi.testclient import TestClient
from main import app
from db_setup import test_db
from utils import create_access_token
from .helpers import create_user, login_user, create_url, get_auth_headers, get_user_urls

client = TestClient(app)

test_username = "testeruser1"
test_password = "testpassword123"


def test_create_user(test_db):
    response = create_user(client, test_username, test_password)

    assert response.status_code == 200
    assert response.json()['username'] == test_username


def test_login(test_db):
    create_user(client, test_username, test_password)
    response = login_user(client, test_username, test_password)

    assert response.status_code == 200
    assert response.json()['access_token'] == create_access_token(
        test_username
    )


def test_shorten_url(test_db):
    url = "https://www.google.com"
    response = create_url(client, url)

    assert response.status_code == 200
    assert response.json()['long'] == url


def test_invalid_url(test_db):
    url = "www.google.com"
    response = create_url(client, url)

    assert response.status_code == 400
    assert response.json()['detail'] == "Invalid URL provided."


def test_user_urls(test_db):
    url = "https://www.google.com"

    create_user(client, test_username, test_password)
    headers = get_auth_headers(client, test_username, test_password)

    create_url(client, url, headers)
    response = get_user_urls(client, headers)

    assert response.status_code == 200
    assert response.json()[0]['long'] == url
