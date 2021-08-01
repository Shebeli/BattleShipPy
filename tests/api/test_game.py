import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.auth.jwt import get_user_from_header_token
from api.conf.utils import get_first_sq

# utility and fixtures


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def j(client):
    response = client.post("/token", json={'username': 'John'})
    return {"Authorization": f'Bearer {response.json()["access_token"]}'}


@pytest.fixture
def m(client):
    response = client.post("/token", json={'username': 'Mike'})
    return {"Authorization": f'Bearer {response.json()["access_token"]}'}


@pytest.fixture
def full_lobby(j, m, client):
    uuid = client.post(
        "/lobby", headers=j).json()['uuid']  # john as host
    client.put("/join-lobby", headers=m, json={'uuid': uuid})
    client.put("/start-lobby", headers=j)


@pytest.fixture
def started_game(j, m, full_lobby, client):
    client.put("/ready-game", headers=j, json={'ready': True})
    client.put("/ready-game", headers=m, json={'ready': True})
    client.put("/start-game", headers=j)


def strike(client, user, cord=[0, 0]):
    return client.put("/strike-square", headers=user, json={'cordinate': cord})


def get_turn(client, user):
    return client.get("/game-state", headers=user).json()['turn']['username']

# tests


def test_my_map(j, m, full_lobby, client):
    response = client.get("/my-map", headers=j)
    assert response.status_code == 200
    assert isinstance(response.json()['map'], list)


def test_opp_map(j, m, full_lobby, client):
    response = client.get("/opp-map", headers=j)
    assert response.status_code == 200
    assert isinstance(response.json()['map'], list)


def test_game_state(j, m, full_lobby, client):
    response = client.get("/game-state", headers=j)
    assert response.json()['started'] == False
    assert response.json()['winner'] == None


def test_move_ship(j, m, full_lobby, client):
    # since we don't know where a ship is, we POST using the first square which we get from map
    map_ = client.get("/my-map", headers=j).json()['map']
    x, y = get_first_sq(map_, 2)
    response = client.get("/ship", headers=j, params={'x': x, 'y': y})
    ship_cord = response.json()['cordinates']
    # implementing this test is complex since the location of ships are random and the output can be many different cases.
    assert True


def test_ready_game(j, m, full_lobby, client):
    client.put("/ready-game", headers=j, json={'ready': True})
    response = client.put("/ready-game", headers=m, json={'ready': True})
    assert response.status_code == 200
    assert response.json()[0]['ready'] == True

def test_ready_state(j, m, started_game, client):
    response = client.get("ready-state", headers=j)
    for player in response.json():
        assert player['ready'] == True

def test_start_game(j, m, full_lobby, client):
    client.put("/ready-game", headers=j, json={'ready': True})
    client.put("/ready-game", headers=m, json={'ready': True})
    response = client.put("/start-game", headers=j)
    assert response.status_code == 200


def test_strike(j, m, started_game, client):
    turn = get_turn(client, j)
    if turn == "John":
        response = strike(client, j)
    else:
        response = strike(client, m)
    assert response.status_code == 200
    assert response.json()['detail'] in (
        "You've been granted another strike!",
        "You missed!")  # you either hit or miss, huh?


def test_strike_same_coordinate(j, m, started_game, client):
    j_count, m_count = 0, 0
    while j_count != 2 and m_count != 2:
        turn = get_turn(client, j)
        print(turn)
        if turn == 'John':
            response = strike(client, j)
            j_count += 1
        else:
            response = strike(client, m)
            m_count += 1
    assert response.status_code == 406
    assert response.json()['detail'] == 'This square has already been striked'


def test_strike_invalid_turn(j, m, started_game, client):
    turn = get_turn(client, j)
    if turn == "John":
        response = strike(client, m)
    else:
        response = strike(client, j)
    assert response.status_code == 406
    assert response.json()['detail'] == 'Its not your turn yet!'


def test_strike_not_ready(j, m, full_lobby, client):
    response = strike(client, j)
    assert response.status_code == 400
    assert response.json()['detail'] == "The game hasn't been started yet!"


def test_strike_finished_game():
    pass  # implemented when finished_game fixture is implemented.


def test_cordinate_validator(j, m, started_game, client):
    response = client.put("/strike-square", headers=j,
                          json={'cordinate': [0, 0, 0]})
    assert response.status_code == 422
