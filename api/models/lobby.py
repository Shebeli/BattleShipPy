from uuid import uuid4

from api.models.user import User
from api.models.base import AbstractCustomSet


class Lobby:
    def __init__(self, id_, host: User):
        self.id = id_
        self.uuid = uuid4().hex[:10]
        self.players = set()
        self.host = host
        self.has_started = False
        self.players.add(host)
        self.game = None

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
        if self.players:
            self.host = next(iter(self.players))
        else:
            self.host = None  # object should be deleted

    def to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'host': self.host.to_dict(),
            'players': [user.to_dict() for user in self.players],
            'has_started': self.has_started,
            'is_full': self.is_full
        }


class LobbySet(AbstractCustomSet):
    sub_class = Lobby

    def user_get_lobby(self, user: User):
        for lobby in self:
            if user in lobby.players:
                return lobby
        return None

    def user_has_lobby(self, user: User):
        for lobby in self:
            if user in lobby.players:
                return True
        return False
