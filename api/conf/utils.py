def get_first_sq(arr: list, value: int):
    for i, item in enumerate(arr):
        if value in item:
            return i, item.index(value)
    return

    