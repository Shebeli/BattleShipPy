from fastapi import HTTPException, status
from api.models.user import User
from api.models.lobby import LobbySet

def check_user_lobby(user: User, lobbies: LobbySet):
    """Raises HTTP Exception if the given user is already in a lobby"""
    for lobby in lobbies:
        if user in lobby.players:
            raise HTTPException(status=status.HTTP_400_BAD_REQUEST, detail='The given user is already in a lobby')