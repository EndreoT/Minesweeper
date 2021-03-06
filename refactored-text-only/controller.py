from collections import deque as Deque

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
        self._num_mines = num_mines
        self._total_cells = self.width * self.height
        self.board = Board(self.width, self.height, self._num_mines)

    def get_wins(self) -> int:
        return self.board.wins

    def get_losses(self) -> int:
        return self.board.losses

    def increment_wins(self) -> None:
        self.board.increment_wins()

    def increment_losses(self) -> None:
        self.board.increment_losses()

    def get_game_state(self) -> GameState:
        return self.board.get_game_state()

    def get_num_mines(self) -> int:
        return self.board.mines_left

    def update_game_state(self) -> None:
        cells_unrevealed = self._total_cells - self.num_cells_revealed()
        if cells_unrevealed == self._num_mines:
            self.get_game_state().set_game_state(True, True, False)

    def num_cells_revealed(self) -> int:
        return len(self.board.cells_revealed())

    def reset(self) -> None:
        """Resets the game"""

        self.board.reset()

    def reveal_decision(self, index: Coordinate) -> List[Tuple[Coordinate, EntryValue]]:
        """Main decision method determining how to reveal cell."""

        cell_value = self.board.get_cell_value(index)
        result = None
        if index in self.board.cells_flagged().union(self.board.cells_revealed()):
            result = []
        elif cell_value.isZero():
            result = self.reveal_zeroes(index)
        elif cell_value.isNum():
            result = [self.reveal_cell(index, cell_value)]
        else:
            # Found mine. Game over
            self.board.get_game_state().set_game_state(True, False, False)
            result = [self.reveal_cell(index, cell_value)]
        self.update_game_state()
        return result

    def reveal_cell(self, index: Coordinate, value: EntryValue) -> Tuple[Coordinate, EntryValue]:
        # """Obtains cell value from model."""

        if index not in self.board.cells_flagged() and index not in self.board.cells_revealed():
            self.board.add_to_revealed_cells(index)
            return (index, value)

    def reveal_zeroes(self, index: Coordinate) -> List[Tuple[Coordinate, EntryValue]]:
        """Reveals all adjacent cells if the current Entry has a zero value."""

        # result = []
        # DFS -> Uses call stack
        # def reveal_helper(index: Coordinate) -> None:
        #     if index in self.board.cells_flagged():
        #         return
        #     val = self.board.get_cell_value(index)
        #     if val.is_num_and_g_t_zero():
        #         result.append(self.reveal_cell(index, val))
        #         return
        #     if val.isZero():
        #         result.append(self.reveal_cell(index, val))
        #         for coord in get_adjacent(index):
        #             if self.board.is_valid_cell(coord) and coord not in self.board.cells_revealed():
        #                 reveal_helper(coord)
        # reveal_helper(index)

        # BFS
        queue = Deque()
        queue.appendleft(index)
        result = []
        isBeingExplored = set()
 
        while queue:
            cell = queue.pop()
            val = self.board.get_cell_value(cell)
            if val.is_num_and_g_t_zero(): # val > 0
                if cell in isBeingExplored:
                    isBeingExplored.remove(cell)
                result.append(self.reveal_cell(cell, val))
            else:  # val == 0
                for coord in get_adjacent(cell):
                    if (
                        self.board.is_valid_cell(coord) 
                        and coord not in self.board.cells_revealed() 
                        and coord not in isBeingExplored
                    ):
                        isBeingExplored.add(coord)          
                        queue.appendleft(coord)
                if cell in isBeingExplored:
                    isBeingExplored.remove(cell)
                result.append(self.reveal_cell(cell, val))

        return result

    def update_flagged_cell(self, index: Coordinate) -> int:
        """Adds or removes cell from flagged cells. Returns int indicating view to flag or unflag cell."""
        if index in self.board.cells_revealed():
            return 0  # Don't flag cell
        if index not in self.board.cells_flagged():
            self.board.add_to_cells_flagged(index)
            return 1  # Flag cell
        else:
            self.board.remove_from_cells_flagged(index)
            return -1  # Unflag cell

    def reveal_all_cells(self) -> List[Tuple[Coordinate, EntryValue]]:
        result = []

        for row in range(self.height):
            for col in range(self.width):
                coord = Coordinate(row, col)
                cell_value = self.board.get_cell_value(coord)
                self.board.add_to_revealed_cells(coord)
                result.append((coord, cell_value))
        return result
