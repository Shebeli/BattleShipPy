# Introduction

BattleShipPy is a python game made using battleship game vector rules. It has an engine that represents the battleship game through the game module, and an API that allows a way to work and play with this engine.

![SHIP](https://media.istockphoto.com/vectors/warship-vector-id123135612?k=6&m=123135612&s=612x612&w=0&h=kWE5pofVJWCVw8JOXxqW4JztamonzGrO1FDkfEoHQN0=)

BattleShip is a game where two players generate a board of squares with ships in them, and their objective is to destroy all their opponent's ships! Whoever destroys all of their opponent's ships first will win.

### Rules and Gameflow:
- Each player is assigned a new board upon game generation
- For each board, there will be some random ships generated through random coordinates
- Players  can reassign their ship positions before the game starts
- Both boards have the same number of ships and for each ship on the player's board, there's a ship with the same length on the opponent's board.
- After both players are ready, the game can be started.
- One of the players will start the game by striking a square on a map which is their opponent's map but cannot see their ships.
- The game is turn-based which means after each strike the turn will change to the other player, however, the player's turn will not change if they strike an opponent's ship, i.e they are granted another turn.






## Installation

Use the package manager [poetry](https://python-poetry.org/docs/basic-usage/#installing-dependencies) to install packages.

```bash
poetry install
```

## API

You can use FastAPI to run a local server and access the endpoints:

```bash
uvicorn api.main:app --reload
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## Features to be added

- Update the output of each board map into object based data rather than numbers.
- Keep track of logged out users and update them if necessary.
- Add a new setting for lobby for defining size of the board before pre-game.
- Add a new setting for lobby for defining number of ships and their length pre-game
- Add a new setting for lobby that doesn't generate random ships with random locations.


## License
[MIT](https://choosealicense.com/licenses/mit/)
