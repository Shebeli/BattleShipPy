from typing import List

from fastapi import HTTPException, status, APIRouter, Depends

from api.schemas.lobby import LobbyIn, LobbyOut,  LobbyGet
from api.auth.jwt import lobbies, get_user_from_header_token
from api.models.user import User

router = APIRouter()


@router.get("/lobbies", response_model=List[LobbyGet])
async def get_lobbies():
    return [lobby.to_dict() for lobby in lobbies]


@router.get("/lobby/{lobby_id}", response_model=LobbyGet)
async def get_lobby(lobby_id: int):
    lobby = lobbies.get(lobby_id)
    if not lobby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Theres no lobby with given id")
    return lobby.to_dict()


@router.post("/create-lobby", response_model=LobbyOut, status_code=status.HTTP_201_CREATED)
async def create_lobby(user: User = Depends(get_user_from_header_token)):
    if lobbies.user_has_lobby(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='user is already in a lobby')
    lobby = lobbies.create_and_add(user)
    return lobby.to_dict()


@router.delete("/lobby/{lobby_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lobby(lobby_id: int, user: User = Depends(get_user_from_header_token)):
    lobby = lobbies.get(lobby_id)
    if not lobby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Given lobby id does not exist")
    if lobby.host != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only host can delete the lobby")
    lobbies.remove_id(lobby_id)
    return


@router.get("/my-lobby", response_model=LobbyGet)
async def get_my_lobby(user: User = Depends(get_user_from_header_token)):
    lobby = lobbies.user_get_lobby(user)
    if lobby:
        return lobby.to_dict()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No lobby found for this user")


@router.put("/join-lobby", response_model=LobbyOut)
async def join_lobby(lobby_input: LobbyIn, user: User = Depends(get_user_from_header_token)):
    if lobbies.user_has_lobby(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='user is already in a lobby')
    for lobby in lobbies:
        if lobby.uuid == lobby_input.uuid:
            if lobby.is_full:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail='Lobby is full!')
            lobby.add_player(user)
            return lobby.to_dict()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Lobby not found')


@router.put("/leave-lobby", status_code=status.HTTP_204_NO_CONTENT,
            description="Used when current user wants to leave the lobby")
async def leave_lobby(user: User = Depends(get_user_from_header_token)):
    lobby = lobbies.user_get_lobby(user)
    if not lobby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theres no lobby for this user"
        )
    if lobby.has_started:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="the lobby has been started, can't leave")
    if not lobby:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not in lobby")
    lobby.remove_player(user)
    if not lobby.players:
        lobbies.remove(lobby)
    return
