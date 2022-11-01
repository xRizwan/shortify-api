from fastapi.testclient import TestClient
from main import app
from db_setup import test_db

client = TestClient(app)


def test_create_user(test_db):
    test_username = "testeruser1"
    test_password = "testpassword123"
    response = client.post(
        '/api/users', json={"username": test_username, "password": test_password})

    assert response.status_code == 200
    assert response.json()['username'] == test_username
