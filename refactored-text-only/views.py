from tkinter import Button, Label, Tk, Frame, StringVar
from typing import Tuple, List, Union

from coordinate import Coordinate
from controller import Controller
from cellEntry import Entry, EntryValue

# TODO: Use JavaScript, HTML, CSS for game display and Python board and controller as API


class TextView:
    """Creates a text interface of the minesweeper game."""

    def __init__(self,
                 width: int,
                 height: int,
                 num_mines: int,
                 ):
        """
        :param width: The horizontal span of the array
        :param height: The vertical span of the array
        :param num_mines: The number of mines to be seeded
        :param controller: A controller class instance
        """
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.controller = Controller(self.width, self.height, self.num_mines)
        self.reveal_dict = {
            0: ' 0  ', 1: ' 1  ', 2: ' 2  ',
            3: ' 3  ', 4: ' 4  ', 5: ' 5  ',
            6: ' 6  ', 7: ' 7  ', 8: ' 8  ',
            -1: "mine"
        }
        self.cell_value = "cell"
        self.flag_value = "FLAG"
        self.cell_view = None
        self.create_cell_view()
        self.main()

    def create_cell_view(self) -> List[List[str]]:
        """Create text view of cells."""

        self.cell_view = [[self.cell_value for _ in range(
            self.width)] for _ in range(self.height)]

    def show_grid(self) -> None:
        """Prints text grid to console. Includes column numbers."""
        mines_left = self.controller.get_num_mines()
        top_row = [str(i) + ":" for i in range(self.width)]
        print("Wins: " + str(self.controller.get_wins()))
        print("Losses: " + str(self.controller.get_losses()))
        print(" ", *top_row, sep=" " * 4)
        for row in range(len(self.cell_view)):
            if row > 9:
                sep = ":"
            else:
                sep = " :"
            print(str(row) + sep, *self.cell_view[row], sep="  ")
        self.update_mines_left(mines_left)

    def reveal_cell(self, index: Coordinate, value: EntryValue) -> None:
        """Reveals a cell's value in the text view"""

        self.cell_view[index.row][index.col] = self.reveal_dict[value.value]

    def flag_cell(self, index: Coordinate) -> None:
        """Flags cell in cell_view"""

        self.cell_view[index.row][index.col] = self.flag_value

    def unflag_cell(self, index: Coordinate) -> None:
        """Unflags cell in cell_view"""

        self.cell_view[index.row][index.col] = self.cell_value

    def update_mines_left(self, mines: int) -> None:
        """Updates mine counter."""

        print("Mines remaining: " + str(mines))

    def display_loss(self) -> None:
        """Displays the loss label when loss condition is reached."""

        print("YOU LOSE!")

    def display_win(self) -> None:
        """Displays the win label when win condition is reached."""

        print("YOU WIN!")

    def main(self) -> None:
        self.show_grid()
        while True:
            # try:
            cmd, *coords = input(
                "Choose a cell in the space separated format: "
                + "flag/reveal row col. Type END to quit.  ").split()
            print()
            if cmd.lower()[0] == "e":
                break
            input_coord = Coordinate(int(coords[0]), int(coords[1]))
            if cmd.lower()[0] == "f":
                is_flagged = self.controller.update_flagged_cell(input_coord)
                if is_flagged == 1:
                    self.flag_cell(input_coord)
                elif is_flagged == -1:
                    self.unflag_cell(input_coord)
            elif cmd.lower()[0] == "r":
                result = self.controller.reveal_decision(input_coord)
                mine_found = False
                for output_coord, value in result:
                    if value.isMine():
                        mine_found = True
                        break
                    self.reveal_cell(output_coord, value)
                if mine_found:
                    for output_coord, value in self.controller.reveal_all_cells():
                        self.reveal_cell(output_coord, value)
            else:
                print("Unknown command")

            self.show_grid()

            # Check for win condition
            game_state = self.controller.get_game_state()
            if game_state.finished:
                if game_state.win:
                    self.controller.increment_wins()
                    self.display_win()
                else:
                    self.controller.increment_losses()
                    self.display_loss()
                print()
                input("Enter any key to play again ")
                print()
                self.controller.reset()
                self.create_cell_view()
                self.show_grid()

            # except Exception:
            #     print("Incorrect selection or format")
