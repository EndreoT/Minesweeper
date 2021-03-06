from typing import Set, List
from collections import namedtuple
from itertools import product
from random import sample

from coordinate import Coordinate
from cellEntry import Entry, EntryValue
from getAdjacent import get_adjacent


class GameState:

    def __init__(self, finished=False, win=False, loss=False):
        self.finished = finished
        self.win = win
        self.loss = loss

    def set_game_state(self, finished, win, loss):
        self.finished = finished
        self.win = win
        self.loss = loss

    def reset_game_state(self):
        self.set_game_state(False, False, False)

    def __str__(self):
        return "(" + "Finished " + str(self.finished) + ", " + "Win " + str(self.win) + ", " + "Loss " + str(self.loss) + ")"


class Board:
    """Creates an array of dimensions width by height and adds mines to it."""

    def __init__(self, width: int, height: int, num_mines: int):
        """
        :param width: The horizontal span of the array
        :param height: The vertical span of the array
        :param num_mines: The number of mines to be seeded
        """
        self._width = width
        self._height = height
        self._total_cells = self._width * self._height
        self._num_mines = num_mines
        self._mines_left = num_mines
        self._wins = 0
        self._losses = 0
        self._cells_revealed = set()
        self._cells_flagged = set()
        self._game_state = GameState()
        self._grid = None
        self._init_game_board()

    def _init_game_board(self) -> None:
        self._create_grid()
        self._add_mines()
        self._set_adjacent_mine_count()

    def reset(self) -> None:
        self._cells_revealed = set()
        self._cells_flagged = set()
        self._mines_left = self._num_mines
        self._create_grid()
        self._add_mines()
        self._set_adjacent_mine_count()
        self._game_state.reset_game_state()

    def _create_grid(self) -> None:
        """Creates a grid of elements Entry objects with null values."""

        self._grid = [[Entry(EntryValue.NULL)] * self._width for _ in range(self._height)]

    def _add_mines(self) -> None:
        """Randomly adds mines to board grid."""

        for col, row in sample(list(product(range(self._width), range(self._height))), self._num_mines):
            self._grid[row][col] = Entry(EntryValue.MINE)

    def _set_adjacent_mine_count(self) -> None:
        """Sets cell Entry values to the number of their adjacent mines."""

        for r in range(len(self._grid)):
            for c in range(len(self._grid[0])):
                coord = Coordinate(r, c)
                if not self.get_cell_entry(coord).isMine():
                    mine_count_array = [self.get_cell_entry(index).isMine(
                    ) for index in get_adjacent(coord) if self.is_valid_cell(index)]
                    num_mines = sum(mine_count_array)
                    entry_value = EntryValue(num_mines)
                    self.set_cell(coord, Entry(entry_value))

    def update_mines_left(self) -> None:
        self._mines_left = self._num_mines - len(self.cells_flagged())

    @property
    def game_state(self) -> str:
        return self._game_state

    @property
    def wins(self):
        return self._wins

    @property
    def losses(self):
        return self._losses
    
    @property
    def mines_left(self):
        return self._mines_left

    def increment_wins(self) -> None:
        self._wins += 1

    def increment_losses(self) -> None:
        self._losses += 1

    def get_game_state(self) -> GameState:
        return self._game_state

    def add_to_revealed_cells(self, coord: Coordinate) -> None:
        self._cells_revealed.add(coord)

    def add_to_cells_flagged(self, coord: Coordinate) -> None:
        self._cells_flagged.add(coord)
        self.update_mines_left()

    def remove_from_cells_flagged(self, coord: Coordinate) -> bool:
        if coord in self._cells_flagged:
            self._cells_flagged.remove(coord)
            self.update_mines_left()
            return True
        return False

    def set_cell(self, coord: Coordinate, entry: Entry) -> None:
        self._grid[coord.row][coord.col] = entry

    def get_cell_entry(self, coord: Coordinate) -> Entry:
        """Returns Entry object at the given index."""

        return self._grid[coord.row][coord.col]

    def get_cell_value(self, coord: Coordinate) -> EntryValue:
        """Returns EntryValue at the given index."""

        return self.get_cell_entry(coord).value

    def is_valid_cell(self, coordinate) -> None:
        return (0 <= coordinate.row <= self._height - 1) and (0 <= coordinate.col <= self._width - 1)

    def cells_flagged(self) -> Set[Coordinate]:
        return self._cells_flagged

    def cells_revealed(self) -> Set[Coordinate]:
        return self._cells_revealed

    def change_game_state(self, state: str) -> None:
        self._game_state = state

    def print(self) -> None:
        result = []
        for row in self._grid:
            row_str = []
            for item in row:
                row_str.append(str(item.value.value))
            result.append(" ".join(row_str))
        for i in result:
            print(i)
