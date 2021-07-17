from fastapi import APIRouter, Depends, HTTPException, status

from api.schemas.game import Map
from game.core import Player, BattleShipGame
from api.auth.jwt import lobbies, get_user_from_header_token, get_lobby_from_user

router = APIRouter()

@router.post("/start-game")
def start_game(user: Depends(get_user_from_header_token), lobby: Depends(get_lobby_from_user)):
    if lobby.has_started:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game for lobby is already started")
    if not lobby.is_full:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lobby is not full")
    if lobby.host != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only host can start the game")
    players = iter(lobby.players)
    game = BattleShipGame.start_game(next(players), next(players))
    lobby.game = game
    lobby.has_started = True
    return {"detail": "game has been started!"}

@router.get("/my-map", response_model=Map)
def my_map(user: Depends(get_user_from_header_token), lobby: Depends(get_lobby_from_user)):
    game = lobby.game
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The game has not been started yet")
    return game.player_map(user) # battlshipclass should be refactored

@router.get("/opp-map", response_model=Map)
def opponent_map(user: Depends(get_user_from_header_token), lobby: Depends(get_lobby_from_user)):
    game = lobby.game
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The game has not been started yet!")
    return game.oh(user) # battlshipclass should be refactored

    