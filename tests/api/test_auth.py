import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.auth.jwt import get_user_from_header_token

client = TestClient(app)

@pytest.fixture
def auth_token():
    response = client.post("/token", json={"username": "test"})
    return response.json()['access_token']

def test_user(auth_token):
    response = client.get("/token/test_header", headers={'Authorization':f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert response.json()['username'] == 'test'
