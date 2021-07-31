from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from game.core import BattleShipGame
from game.exceptions import (CordinatesValidationError, ShipLengthError, PlayerTurnError,
                             SquareStrikedError, SquaresNotAttachedError, SquareStateError)
from api.schemas.game import (Map, SelectedCord,  MoveShipCords,
                              ReadyGame,  ReadyOut, GameState, ShipOut)
from api.auth.jwt import get_user_from_header_token, get_lobby_from_user, get_game_from_lobby
from api.conf.utils import players_state
from api.models.user import User
from api.models.lobby import Lobby

router = APIRouter()


@router.put("/start-lobby")
async def start_lobby(
        user: User = Depends(get_user_from_header_token),
        lobby: Lobby = Depends(get_lobby_from_user)):
    if lobby.has_started:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This lobby has already been started!")
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
    return {"detail": "lobby has been started!"}


@router.get("/my-map", response_model=Map)
async def my_map(
        user: User = Depends(get_user_from_header_token),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    return Map(map=game.player_map(user))


@router.get("/opp-map", response_model=Map)
async def opponent_map(
        user: User = Depends(get_user_from_header_token),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    return Map(map=game.opponent_map(user))


@router.get("/get-ship", response_model=ShipOut)
async def get_ship(
        x: int,
        y: int,
        user: User = Depends(get_user_from_header_token),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    cord = (x, y)
    ship = game.get_ship(cord, user)
    if not ship:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No ship found for given cordinate")
    return ShipOut(cordinates=ship.cords)


@router.get("/get-ships", response_model=List[ShipOut])
async def get_ships(
        user: User = Depends(get_user_from_header_token),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    ships = game.get_ships(user)
    if not ships:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No ship for this player")
    return [{'cordinates': ship.cords} for ship in ships]


@router.get("/game-state", response_model=GameState)
async def game_state(
        user: User = Depends(get_user_from_header_token),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    return GameState(readyState=players_state(game),
                     turn=game.turn.user.to_dict(),
                     started=game.started, finished=game.finished,
                     winner=game.winner)


@router.put("/move-ship", status_code=status.HTTP_202_ACCEPTED, response_model=Map,
            description="""Note that since ships might get mixed when near each other,
            use get ship API to confirm each ship exact cordination""")
async def move_ship(
        cordinates: MoveShipCords,
        user: User = Depends(get_user_from_header_token),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    if game.started or game.finished:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Cannot move ships since game is either started or finished.')
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
        game.move_ship(ship, cordinates.cordinates, user)
    # another case where SquaresAreNotAttached, MinXMax and if SquaresAreNotEmpty
    except (ShipLengthError, SquareStateError, SquaresNotAttachedError):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="""Given length of ship is not valid,
                            or selected squares are not empty, 
                            or they are not continues""")
    return Map(map=game.player_map(user))


@router.put("/ready-game", response_model=GameState)
async def ready_game(
        ready: ReadyGame,
        user: User = Depends(get_user_from_header_token),
        lobby: Lobby = Depends(get_lobby_from_user),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    if game.started:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The game has already been started!")
    player = game.get_player(user)
    player.ready = ready.ready
    return GameState(readyState=players_state(game),
                     turn=game.turn.user.to_dict(),
                     started=game.started, finished=game.finished,
                     winner=game.winner)


@router.put("/start-game", response_model=GameState)
async def start_game(
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
    return GameState(readyState=players_state(game),
                     turn=game.turn.user.to_dict(),
                     started=game.started, finished=game.finished,
                     winner=game.winner)


@router.put("/strike-square")
async def strike_square(
        square: SelectedCord,
        user: User = Depends(get_user_from_header_token),
        game: BattleShipGame = Depends(get_game_from_lobby)):
    player = game.get_player(user)
    if not game.started:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The game hasn't been started yet!")
    if game.finished:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='The game has already been finished! cannot strike!')
    try:  # CordinatesValidateError, Player not for this game, SquareStrikedError
        detail = None
        game.strike(square.cordinate, user)
    except SquareStrikedError:
        detail = "This square has already been striked"
    except CordinatesValidationError:
        detail = "Given cordinates are not within range of X and Y of board!'"
    except PlayerTurnError:
        detail = 'Its not your turn yet!'
    if detail:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=detail)
    if game.winner:
        return {"detail": "Congratz u won the game!"}
    if game.turn == player:
        return {"detail": "You've been granted another strike!"}
    return {"detail": "You missed!"}
