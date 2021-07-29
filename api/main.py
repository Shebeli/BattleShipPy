from fastapi import FastAPI
from api.endpoints import users, lobby, game
from fastapi.middleware.cors import CORSMiddleware

origins = [
    'http://localhost',
    "http://localhost:8080",
    "http://localhost:5000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(lobby.router)
app.include_router(game.router)
