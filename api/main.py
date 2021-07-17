from typing import Optional

from fastapi import FastAPI, Header, Request
from pydantic import BaseModel
from api.endpoints import users, lobby


app = FastAPI()

app.include_router(users.router)
app.include_router(lobby.router)

@app.get("/")
async def root():
    return {"messageee": "Hellowwww"}
