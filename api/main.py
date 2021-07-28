from fastapi import FastAPI
from api.endpoints import users, lobby, game


app = FastAPI()

app.include_router(users.router)
app.include_router(lobby.router)
app.include_router(game.router)
