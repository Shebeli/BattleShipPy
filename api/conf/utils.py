from typing import Union, Tuple, Dict, List


def get_first_sq(arr: list, value: int) -> Union[None, Tuple[int, int]]:
    for i, item in enumerate(arr):
        if value in item:
            return i, item.index(value)
    return None


def players_state(game) -> List[Dict]:
    players = []
    for player in game.players:
        data = player.user.to_dict()
        data.update({'ready': player.ready})
        players.append(data)
    return players
