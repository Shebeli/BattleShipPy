from typing import Optional

from fastapi import FastAPI, Header, Request
from pydantic import BaseModel
from api.endpoints import users, lobby, game


app = FastAPI()

app.include_router(users.router)
app.include_router(lobby.router)
app.include_router(game.router)

@app.get("/")
async def root():
    return {"messageee": "Hellowwww"}
