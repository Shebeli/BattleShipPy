from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from game.core import Player, BattleShipGame
from game.exceptions import CordinatesValidationError, ShipLengthError, PlayerTurnError, SquareStrikedError
from api.schemas.game import Map, SelectedSquare, SelectedSquares, ReadyGame, StartGame, ReadyOut, GameState
from api.auth.jwt import lobbies, get_user_from_header_token, get_lobby_from_user, get_game_from_lobby
from api.models.user import User
from api.models.lobby import Lobby
from game.core import BattleShipGame

router = APIRouter()


@router.post("/start-lobby")
def start_game(
        user: User = Depends(get_user_from_header_token),
        lobby: Lobby = Depends(get_lobby_from_user)):
    if lobby.has_started:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Game for lobby is already pre-started")
    if not lobby.is_full:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Lobby is not full")
    if lobby.host != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only host can start the lobby")
    players = iter(lobby.players)
    game = BattleShipGame.start_game(next(players), next(players))
    lobby.game = game
    lobby.has_started = True
    return {"detail": "game has been started!"}


@router.get("/my-map", response_model=Map)
def my_map(
        user: User = Depends(get_user_from_header_token),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    return {"map": game.player_map(user)}  # battlshipclass should be refactored


@router.get("/opp-map", response_model=Map)
def opponent_map(
        user: User = Depends(get_user_from_header_token),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    return {"map": game.opponent_map(user)}  # battlshipclass should be refactored


@router.get("/game-state", response_model=GameState)
def game_state(
        user: User = Depends(get_user_from_header_token),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    return GameState(turn=game.turn.username, started=game.started, finished=game.finished, winner=game.winner)


@router.post("/move-ship", status_code=status.HTTP_202_ACCEPTED, response_model=Map)
def move_ship(
        cordinates: SelectedSquares,
        user: User = Depends(get_user_from_header_token),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    print(cordinates)
    if game.started or game.finished:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='The game has already been started or finished! cannot move ship!')
    try:
        # game.p1.board.get_ship(square)
        ship = game.get_ship(cordinates.cordinate, user)
    except CordinatesValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Given cordinates are not within range of X and Y of board!')
    if not ship:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Theres no ship in this square!')
    try:
        game.move_ship(ship, cordinates.cordinate)
    except ShipLengthError:  # another case where SquaresAreNotAttached, MinXMax and if SquaresAreNotEmpty
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Number of cordinates should be equale to the length of the ship!")
    return game.player_map(user)


@router.post("/ready-game", response_model=List[ReadyOut])
def ready_game(
        ready: ReadyGame,
        user: User = Depends(get_user_from_header_token),
        lobby: Lobby = Depends(get_lobby_from_user),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    if game.started:
        raise HTTPException(status=status.HTTP_400_BAD_REQUEST,
                            detail="The game has already been started!")
    player = game.get_player(user)
    player.ready = ready.ready
    players = []
    for p in game.players:
        data = p.user.to_dict()
        data.update({'ready': p.ready})
        players.append(data)
    return players


@router.post("/start-game", response_model=GameState)
def start_game(
        user: User = Depends(get_user_from_header_token),
        lobby: Lobby = Depends(get_lobby_from_user),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    if user != lobby.host:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only host can start the game!")
    if game.started:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Game has already been started!")
    if not game.p1.ready or not game.p2.ready:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="One or both of players are not ready!")
    game.started = True
    return GameState(turn=game.turn.username, started=game.started, finished=game.finished, winner=game.winner)


@router.post("/strike-square", response_model=Map)
def strike_square(
        square: SelectedSquare,
        user: User = Depends(get_user_from_header_token),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    if not game.started:  # players should be ready
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Players are not ready yet!")
    if game.finished:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='The game has already been finished! cannot strike!')
    try:  # CordinatesValidateError, Player not for this game, SquareStrikedError
        game.strike(square, user)
    except (SquareStrikedError, CordinatesValidationError) as e:
        if e == SquareStrikedError:
            detail = "This square has already been striked"
        else:
            detail = "Given cordinates are not within range of X and Y of board!'"
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=detail)
    if game.winner:
        return {"detail": "woooo you won game gg wp"}
    if game.turn != user:
        return game.opponent_map(user)
    return game.opponent_map(user)
