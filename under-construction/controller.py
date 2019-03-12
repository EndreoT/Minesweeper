from typing import List, Tuple

from getAdjacent import get_adjacent
from board import Board, GameState
from coordinate import Coordinate
from cellEntry import Entry, EntryValue


class Controller:
    """Sets up minesweeper game logic."""

    def __init__(self, width: int, height: int, num_mines: int):
        """
        :param width: The horizontal span of the array
        :param height: The vertical span of the array
        :param num_mines: The number of mines to be seeded
        """
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.total_cells = self.width * self.height
        self.board = Board(self.width, self.height, self.num_mines)

    def get_wins(self):
        return self.board.wins
    
    def get_losses(self):
        return self.board.losses
    
    def increment_wins(self):
        self.board.increment_wins() 
    
    def increment_losses(self):
        self.board.increment_losses()

    def update_game_state(self) -> GameState:
        cells_unrevealed = self.total_cells - self.num_cells_revealed()
        game_state = self.board.get_game_state()
        if cells_unrevealed == self.num_mines:
            self.board.get_game_state().set_game_state(True, True, False)
        return game_state

    def num_cells_revealed(self) -> int:
        return len(self.board.cells_revealed())

    def reset(self) -> None:
        """Resets the game"""

        self.board.reset()

    def reveal_decision(self, index: Coordinate):
        """Main decision method determining how to reveal cell."""

        cell_value = self.board.get_cell_value(index)
        if index in self.board.cells_flagged().union(self.board.cells_revealed()):
            return []
        if cell_value.isZero():
            return self.reveal_zeroes(index)
        elif cell_value.isNum():
            return [self.reveal_cell(index, cell_value)]
        else: 
            # Found mine. Game over
            self.board.get_game_state().set_game_state(True, False, False)
            return [self.reveal_cell(index, cell_value)]

    def reveal_cell(self, index: Coordinate, value: EntryValue) -> Tuple[Coordinate, EntryValue]:
        # """Obtains cell value from model and passes the value to view."""

        if index not in self.board.cells_flagged() and index not in self.board.cells_revealed():
            self.board.add_to_revealed_cells(index)
            return (index, value)

    def reveal_zeroes(self, index: Coordinate):
        """Reveals all adjacent cells just until a mine is reached."""
        result = []
        def reveal_helper(index: Coordinate) -> None:
            if index in self.board.cells_flagged():
                return
            val = self.board.get_cell_value(index)
            if val.is_num_and_g_t_zero():
                result.append(self.reveal_cell(index, val))
                return
            if val.isZero():
                result.append(self.reveal_cell(index, val))
                for coord in get_adjacent(index):
                    if self.board.is_valid_cell(coord) and coord not in self.board.cells_revealed():
                        reveal_helper(coord)
        reveal_helper(index)
        return result
       
    def update_flagged_cell(self, index: Coordinate) -> int:
        """Flag/unflag cells for possible mines. Does not reveal cell."""
        if index in self.board.cells_revealed():
            return 0 # Don't flag
        if index not in self.board.cells_flagged():
            self.board.add_to_cells_flagged(index)
            return 1 # Flag
        else:
            self.board.remove_from_cells_flagged(index)
            return -1 # Unflag

        self.update_mines()

    def update_mines(self) -> None:
        """Update mine counter."""

        mines_left = self.num_mines - len(self.board.cells_flagged())

        if mines_left >= 0:
            return mines_left

    def reveal_all_cells(self):
        result = []
        for row in range(self.height):
            for col in range(self.width):
                coord = Coordinate(row, col)
                cell_value = self.board.get_cell_value(coord)
                self.board.add_to_revealed_cells(coord)
                result.append((coord, cell_value))
        return result