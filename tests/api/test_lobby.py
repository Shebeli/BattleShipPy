import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.auth.jwt import get_user_from_header_token

client = TestClient(app)


@pytest.fixture
def john_header():
    response = client.post("/token", json={'username': 'John'})
    return {"Authorization": f'Bearer {response.json()["access_token"]}'}


@pytest.fixture
def mike_header():
    response = client.post("/token", json={'username': 'Mike'})
    return {"Authorization": f'Bearer {response.json()["access_token"]}'}


def test_lobby_create(john_header):
    response = client.post("/create-lobby", headers=john_header)
    assert response.status_code == 201
    assert response.json()['host']['username'] == 'John'


@pytest.fixture
def lobby(john_header):
    response = client.post("/create-lobby", headers=john_header)
    return response.json()['uuid']

def test_lobby_join(lobby, mike_header):
    response = client.post("/join-lobby", json={'uuid': lobby}, headers=mike_header)
    assert response.status_code == 200
    assert 'Mike' in (player['username'] for player in response.json()['players'])

def test_get_lobbies(lobby):
    response = client.get("/get-lobbies")
    assert response.status_code == 200
    assert response.json()[0]['host']['username'] == 'John'


def test_lobby_leave_empty(john_header):
    response = client.post("/leave-lobby", headers=john_header)
    assert response.status_code == 404

def test_lobby_start(lobby, john_header, mike_header):
    response2 = client.post('/join-lobby', json={'uuid': lobby}, headers=mike_header)
    response = client.post('/start-lobby', headers=john_header)
    assert response.json() == {'detail': 'lobby has been started!'}
    assert response.status_code == 200
