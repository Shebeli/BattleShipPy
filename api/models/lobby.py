from uuid import uuid4
from api.models.user import User
from itertools import count

class Lobby:
    def __init__(self, id, host: User):
        self.id = id
        self.uuid = uuid4().hex[:10]
        self.players = set().add(host)
        self.host = host
        self.has_started = False

    @property
    def is_full(self):
        if len(self.players) == 2:
            return True
        return False

    def add_player(self, player):
        if self.is_full:
            raise Exception("Lobby is full")
        self.players.add(player)

    def remove_player(self, player):
        if player not in self.players:
            raise Exception("The given player is not in the lobby")
        self.players.remove(player)

    def to_dict(self):
        return {
            'id': self.uuid,
            'players': [user.to_dict() for user in self.players],
            'host': self.host,
            'has_started': self.has_started,
            'is_full': self.is_full
        }

class LobbySet:
    def __init__(self):
        self.counter = count(1)
        self.lobbies = set()

    def create_and_add(self, host: User):
        lobby = Lobby(next(self.counter), host)
        self.lobbies.add(lobby)
        return lobby
    
    def get(self, id):
        for lobby in self.lobbies:
            if lobby.id == id:
                return lobby
        return

    def remove(self, id):
        lobby = self.get(id)
        if lobby:
            self.lobbies.remove(lobby)
        return
            