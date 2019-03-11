from typing import Set, Tuple


def get_adjacent(index: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """Returns adjacent coordinates for input index"""

    x, y = index

    return (
        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
        (x - 1, y),                 (x + 1, y),
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
    )
