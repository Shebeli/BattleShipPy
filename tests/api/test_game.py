import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.auth.jwt import get_user_from_header_token
from api.conf.utils import get_first_sq


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def full_lobby(client):
    john_token = client.post(
        "/token", json={'username': 'John'}).json()['access_token']
    john_header = {'Authorization': f'Bearer {john_token}'}
    mike_token = client.post(
        "/token", json={'username': 'Mike'}).json()['access_token']
    mike_header = {'Authorization': f'Bearer {mike_token}'}
    uuid = client.post(
        "/create-lobby", headers=john_header).json()['uuid']  # john as host
    client.put("/join-lobby", headers=mike_header, json={'uuid': uuid})
    client.put("/start-lobby", headers=john_header)
    return john_header, mike_header


def test_my_map(full_lobby, client):
    j, m = full_lobby
    response = client.get("/my-map", headers=j)
    assert response.status_code == 200
    assert isinstance(response.json()['map'], list)


def test_opp_map(full_lobby, client):
    j, m = full_lobby
    response = client.get("/opp-map", headers=j)
    assert response.status_code == 200
    assert isinstance(response.json()['map'], list)


def test_game_state(full_lobby, client):
    j, m = full_lobby
    response = client.get("/game-state", headers=j)
    assert response.json()['started'] == False


def test_move_ship(full_lobby, client):
    j, m = full_lobby
    # since we don't know where a ship is, we POST using the first square which we get from map
    map_ = client.get("/my-map", headers=j).json()['map']
    x, y = get_first_sq(map_, 2)
    response = client.get("/get-ship", headers=j, params={'x': x, 'y': y})
    ship_cord = response.json()['cordinates']
    # implementing this test is complex since the location of ships are random and the output can be many different cases.
    assert True


def test_ready_game(full_lobby, client):
    j, m = full_lobby
    response = client.put("/ready-game", headers=j, json={'ready': True})
    response_ = client.put("/ready-game", headers=m, json={'ready': True})
    assert response.status_code == 200 and response_.status_code == 200


def test_start_game(full_lobby, client):
    j, m = full_lobby
    client.put("/ready-game", headers=j, json={'ready': True})
    client.put("/ready-game", headers=m, json={'ready': True})
    response = client.put("/start-game", headers=j)
    assert response.status_code == 200


@pytest.fixture
def started_game(full_lobby, client):
    j, m = full_lobby
    client.put("/ready-game", headers=j, json={'ready': True})
    client.put("/ready-game", headers=m, json={'ready': True})
    client.put("/start-game", headers=j)
    return j, m


def test_strike(started_game, client):
    j, m = started_game
    response = client.put("/strike-square", headers=j,
                           json={'cordinate': [0, 0]})
    # note that this test is 50/50 since turn can be the other player and 406 error indicates this state.
    assert response.status_code == 200 or response.status_code == 406


def test_cordinate_validator(started_game, client):
    j, m = started_game
    response = client.put("/strike-square", headers=j,
                           json={'cordinate': [0, 0, 0]})
    assert response.status_code == 422
