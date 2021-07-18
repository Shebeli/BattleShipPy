from fastapi import APIRouter, Depends, HTTPException, status

from game.core import Player, BattleShipGame
from game.exceptions import CordinatesValidationError, ShipLengthError, PlayerTurnError, SquareStrikedError
from api.schemas.game import Map, SelectSquare, SelectedSquares
from api.auth.jwt import lobbies, get_user_from_header_token, get_lobby_from_user, get_game_from_lobby

router = APIRouter()


@router.post("/start-game")
def start_game(user: Depends(get_user_from_header_token), lobby: Depends(get_lobby_from_user)):
    if lobby.has_started:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Game for lobby is already started")
    if not lobby.is_full:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Lobby is not full")
    if lobby.host != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only host can start the game")
    players = iter(lobby.players)
    game = BattleShipGame.start_game(next(players), next(players))
    lobby.game = game
    lobby.has_started = True
    return {"detail": "game has been started!"}


@router.get("/my-map", response_model=Map)
def my_map(user: Depends(get_user_from_header_token), game: Depends(get_game_from_lobby)):
    return game.player_map(user)  # battlshipclass should be refactored


@router.get("/opp-map", response_model=Map)
def opponent_map(user: Depends(get_user_from_header_token), game: Depends(get_game_from_lobby)):
    return game.opponent_map(user)  # battlshipclass should be refactored


@router.post("/move-ship", status_code=status.HTTP_202_ACCEPTED, response_model=Map)
def move_ship(
        square: SelectSquare,
        cordinates: SelectedSquares,
        user: Depends(get_user_from_header_token),
        game: Depends(get_game_from_lobby)):
    if game.started or game.finished:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The game has already been started or finished! cannot move ship!')
    try:
        ship = game.get_ship(square, user) # game.p1.board.get_ship(square)
    except CordinatesValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Given cordinates are not within range of X and Y of board!')
    if not ship:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Theres no ship in this square!')
    try:
        game.move_ship(ship, cordinates)
    except ShipLengthError: # another case where SquaresAreNotAttached, MinXMax and if SquaresAreNotEmpty
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Number of cordinates should be equale to the length of the ship!")
    return game.player_map(user)

@router.post("/strike-square", Map)
def strike_square(
    square: SelectSquare,
    user: Depends(get_user_from_header_token),
    game: Depends(get_game_from_lobby)):
    if game.finished:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The game has already been finished! cannot strike!')
    try: # CordinatesValidateError, Player not for this game, SquareStrikedError
        game.strike(square, user)
    except (SquareStrikedError, CordinatesValidationError) as e:
        if e == SquareStrikedError:
            detail = "This square has already been striked"
        else: 
            detail = "Given cordinates are not within range of X and Y of board!'"
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=detail)
    if game.winner:
        return {"detail": "woooo you won game gg wp"}
    if game.turn != user:
        return game.opponent_map(user)
    return game.opponent_map(user)