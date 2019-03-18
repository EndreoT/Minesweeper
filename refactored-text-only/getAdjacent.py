from typing import Set

from coordinate import Coordinate

def get_adjacent(index: Coordinate) -> Set[Coordinate]:
    """Returns all 9 adjacent coordinates of an input coordinate"""

    row, col = index.row, index.col

    coordinates = [
        (col - 1, row - 1), (col, row - 1), (col + 1, row - 1),
        (col - 1, row),                     (col + 1, row),
        (col - 1, row + 1), (col, row + 1), (col + 1, row + 1)
    ]
    output = set()
    for coord in coordinates:
        output.add(Coordinate(coord[1], coord[0]))
    return output

