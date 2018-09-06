from typing import Tuple

from get_adjacent import get_adjacent
from model import Model
import view

class Controller:
    """Sets up minesweeper game logic."""

    def __init__(self,
                 width: int,
                 height: int,
                 num_mines: int,
                 difficulty: str,
                 view_type: str
                 ):
        """
        :param width: The horizontal span of the array
        :param height: The vertical span of the array
        :param num_mines: The number of mines to be seeded
        :param difficulty: A string choosing game difficulty. Choose from 'Easy', 'Medium', or 'hard'
        :param view_type: A string choosing game type. The choice is either 'GUI', or 'TEXT'
        """
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.difficulty = difficulty
        self.model = Model(self.width, self.height, self.num_mines)
        if view_type == "GUI":
            self.view = view.GUIView(self.width, self.height,
                                self.num_mines, self)
        elif view_type == "TEXT":
            self.view = view.TextView(self.width, self.height,
                                 self.num_mines, self)
        self.view.main()

    def reset(self) -> None:
        """Resets the game"""

        self.view.reset_view()
        self.model = Model(self.width, self.height, self.num_mines)
        self.view = view.GUIView(self.width, self.height,
                            self.num_mines, self)
        self.view.main()

    def reveal_decision(self, index: Tuple[int, int]) -> None:
        """Main decision method determining how to reveal cell."""

        cell_value = self.model.get_cell_value(index)
        if index in self.model.get_cells_flagged():
            return None

        if cell_value in range(1, 9):
            self.reveal_cell(index, cell_value)

        elif (
            self.model.get_cell_value(index) == self.model.mine_value()
            and self.model.game_state != "win"
        ):
            self.loss()
        else:
            self.reveal_zeroes(index)

        #        Check for win condition
        cells_unrevealed = self.height * self.width - len(self.model.get_cells_revealed())
        if cells_unrevealed == self.num_mines and self.model.game_state != "loss":
            self.win()
        self.update_mines()

    def reveal_cell(self, index: Tuple[int, int], value: int or str) -> None:
        """Obtains cell value from model and passes the value to view."""

        if index not in self.model.get_cells_flagged():
            self.model.get_cells_revealed().add(index)
            self.view.reveal_cell(index, value)

    def reveal_zeroes(self, index: Tuple[int, int]) -> None:
        """Reveals all adjacent cells just until a mine is reached."""

        val = self.model.get_cell_value(index)

        if val == 0:
            self.reveal_cell(index, val)
            self.reveal_adjacent(index)

            for coords in get_adjacent(index):
                if (
                        0 <= coords[0] <= self.width - 1
                        and self.height - 1 >= coords[1] >= 0 == self.model.get_cell_value(coords)
                        and coords not in self.model.get_revealed_zeroes()
                ):
                    self.model.get_revealed_zeroes().add(coords)
                    self.reveal_zeroes(coords)

    def reveal_adjacent(self, index: Tuple[int, int]) -> None:
        """Reveals the 8 adjacent cells to the input cell's index."""

        for coords in get_adjacent(index):
            if (
                    0 <= coords[0] <= self.width - 1
                    and 0 <= coords[1] <= self.height - 1
            ):
                cell_value = self.model.get_cell_value(coords)
                self.reveal_cell(coords, cell_value)

    def update_flagged_cell(self, index: Tuple[int, int]) -> None:
        """Flag/unflag cells for possible mines. Does not reveal cell."""

        if (
                index not in self.model.get_cells_revealed()
                and index not in self.model.get_cells_flagged()
        ):
            self.model.get_cells_flagged().add(index)
            self.view.flag_cell(index)

        elif (
                index not in self.model.get_cells_revealed()
                and index in self.model.get_cells_flagged()
        ):
            self.model.get_cells_flagged().remove(index)
            self.view.unflag_cell(index)

        self.update_mines()

    def update_mines(self) -> None:
        """Update mine counter."""

        mines_left = self.num_mines - len(self.model.get_cells_flagged())

        if mines_left >= 0:
            self.view.update_mines_left(mines_left)

    def win(self) -> None:
        """Sweet sweet victory."""

        self.model.change_game_state("win")
        self.view.display_win()

    def loss(self) -> None:
        """Show loss in view, and reveal all cells."""

        self.model.change_game_state("loss")
        self.view.display_loss()

        #        Reveals all cells
        for row in range(self.height):
            for col in range(self.width):
                cell_value = self.model.get_cell_value((col, row))
                self.view.reveal_cell((col, row), cell_value)
