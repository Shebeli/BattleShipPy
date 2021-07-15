from uuid import uuid4

class Lobby:
    def __init__(self, host: int):
        self.id = uuid4().hex[:10]
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

    # def delete_lobby(self, player):
    #     if player != self.host:
    #         raise Exception("Only host can delete lobby")
    #     del self