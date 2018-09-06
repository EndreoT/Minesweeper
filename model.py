from itertools import product
from random import sample
from typing import Set, Tuple, List, Union

from get_adjacent import get_adjacent


class Model:
    """Creates an array of dimensions width by height and adds mines to it."""

    def __init__(self, width: int, height: int, num_mines: int):
        """
        :param width: The horizontal span of the array
        :param height: The vertical span of the array
        :param num_mines: The number of mines to be seeded
        """
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.mine = -1
        self.grid = self._create_grid()
        self._add_mines()
        self.grid_coords = self.grid_coords()
        self._set_adjacent_mine_count()
        self._cells_revealed = set()
        self._cells_flagged = set()
        self._revealed_zeroes = set()
        self._game_state = None

    def mine_value(self):
        return self.mine

    def _create_grid(self) -> List[List[int]]:
        """Returns a (width by height) grid of elements with value of 0."""

        return [[0] * self.width for _ in range(self.height)]

    def _add_mines(self) -> None:
        """Randomly adds mines to board grid."""

        for x, y in sample(list(product(range(self.width), range(self.height))), self.num_mines):
            self.grid[y][x] = self.mine

    def grid_coords(self) -> List[Tuple[int, int]]:
        """Returns a list of (x, y) coordinates for every position on grid."""

        return [(x, y) for y in range(self.height) for x in range(self.width)]

    def is_mine(self, coords: Tuple[int, int]) -> bool:
        """Determines if current grid location contains a mine"""

        try:
            if coords[0] >= 0 and coords[1] >= 0:
                return self.grid[coords[1]][coords[0]] == self.mine
            else:
                return False
        except IndexError:
            return False

    def _set_adjacent_mine_count(self) -> None:
        """Sets cell values to the number of their adjacent mines."""

        for position in self.grid_coords:
            x, y = position
            if self.grid[y][x] >= 0:
                grid_value = sum(map(self.is_mine, get_adjacent(position)))
                self.grid[y][x] = grid_value

    def get_cell_value(self, index: Tuple[int, int]) -> Union[int, str]:
        """Returns model's cell value at the given index."""

        x, y = index
        return self.grid[y][x]

    def get_cells_flagged(self) -> Set:
        return self._cells_flagged

    def get_cells_revealed(self):
        return self._cells_revealed

    def get_revealed_zeroes(self):
        return self._revealed_zeroes

    @property
    def game_state(self) -> str:
        return self._game_state

    def change_game_state(self, state: str) -> None:
        self._game_state = state
