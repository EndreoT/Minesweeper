from tkinter import Button, Label, Tk, Frame, StringVar
from typing import Tuple, List, Union

import controller


class GUIView:
    """Creates a GUI with a grid of cell buttons."""

    def __init__(self,
                 width: int,
                 height: int,
                 num_mines: int,
                 controller: "controller.Controller"):
        """
        :param width: The horizontal span of the array
        :param height: The vertical span of the array
        :param num_mines: The number of mines to be seeded
        :param controller: A controller class instance
        """
        self.master = Tk()
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.controller = controller
        self.color_dict = {
            0: 'white', 1: 'blue', 2: 'green',
            3: 'red', 4: 'orange', 5: 'purple',
            6: 'grey', 7: 'grey', 8: 'grey',
            -1: "black"
            }
        self.master.title('Minesweeper')

    def _create_buttons(self) -> list:
        """Create cell button widgets."""

        def create_button(x: int, y: int) -> Button:
            button = Button(self.master, width=5, bg='grey')
            button.grid(row=y + 5, column=x + 1)
            return button

        return [
                [create_button(x, y) for x in range(self.width)]
                for y in range(self.height)
                ]

    def _initialize_bindings(self) -> None:
        """Set up the reveal cell and the flag cell key bindings."""

        for x in range(self.width):
            for y in range(self.height):
                def closure_helper(f, index: tuple):
                    def g(_):
                        f(index)
                    return g

                # Bind reveal decision method to left click
                self.buttons[y][x].bind(
                    '<Button-1>', closure_helper(
                        self.controller.reveal_decision, (x, y)))

                # Bind flag method to right click
                self.buttons[y][x].bind(
                    '<Button-3>', closure_helper(
                        self.controller.update_flagged_cell, (x, y)))

        # Set up reset button
        self.top_panel.reset_button.bind(
            '<Button>', lambda event: self.controller.reset())

    def reset_view(self) -> None:
        """Destroys the GUI. Controller will create a new GUI"""

        self.master.destroy()

    def reveal_cell(self, index: Tuple[int, int], value: Union[int, str]) -> None:
        """Reveals cell's value on GUI."""

        x, y = index
        self.buttons[y][x].configure(text=value, bg=self.color_dict[value])

    def flag_cell(self, index: Tuple[int, int]) -> None:
        """Flag cell in GUI"""

        x, y = index
        self.buttons[y][x].configure(text="FLAG", bg="yellow")

    def unflag_cell(self, index: Tuple[int, int]) -> None:
        """Unflag cell in GUI"""
        x, y = index
        self.buttons[y][x].configure(text="", bg="grey")

    def update_mines_left(self, mines: int) -> None:
        """Updates mine counter widget"""

        self.top_panel.mine_count.set("Mines remaining: " + str(mines))

    def display_loss(self) -> None:
        """Display the loss label when lose condition is reached."""

        self.top_panel.loss_label.grid(row=0, columnspan=10)

    def display_win(self) -> None:
        """Display the win label when win condition is reached."""

        self.top_panel.win_label.grid(row=0, columnspan=10)

    def main(self) -> None:
        self.top_panel = TopPanel(self.master, self.num_mines)
        self.buttons = self._create_buttons()
        self.top_panel.mines_left.grid(row=0, columnspan=5)
        self._initialize_bindings()
        self.master.mainloop()


class TopPanel(Frame):
    """Creates a top panel which contains game information."""

    def __init__(self, master: Tk, num_mines: int):
        Frame.__init__(self, master)
        self.master = master
        self.num_mines = num_mines
        self.grid()

        self.reset_button = Button(self.master, width=7, text='Reset')
        self.reset_button.grid(row=0)

        self.loss_label = Label(text='You Lose!', bg='red')
        self.win_label = Label(text='You Win!', bg='green')

        self.mine_count = StringVar()
        self.mine_count.set('Mines remaining: ' + str(self.num_mines))
        self.mines_left = Label(textvariable=self.mine_count)


class TextView:
    """Creates a text interface of the minesweeper game."""

    def __init__(self,
                 width: int,
                 height: int,
                 num_mines: int,
                 controller: "controller.Controller"
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
        self.controller = controller
        self.reveal_dict = {
            0: ' 0  ', 1: ' 1  ', 2: ' 2  ',
            3: ' 3  ', 4: ' 4  ', 5: ' 5  ',
            6: ' 6  ', 7: ' 7  ', 8: ' 8  ',
            -1: "mine"
        }
        self.cell_view = self.cell_view()
        self.show_grid()

    def cell_view(self) -> List[List[str]]:
        """Create text view of cells."""

        return [["cell" for _ in range(self.width)]
                for _ in range(self.height)
                ]

    def show_grid(self) -> None:
        """Prints text grid to console. Includes column numbers."""

        top_row = [str(i) + ":" for i in range(self.width)]
        print(" ", *top_row, sep=" " * 4)
        for row in range(len(self.cell_view)):
            print(str(row) + ":", *self.cell_view[row], sep="  ")

    def reveal_cell(self, index: Tuple[int, int], value: int) -> None:
        """Reveals a cell's value in the text view"""

        x, y = index
        self.cell_view[y][x] = self.reveal_dict[value]

    def flag_cell(self, index: Tuple[int, int]) -> None:
        """Flags cell in cell_view"""

        x, y = index
        self.cell_view[y][x] = "FLAG"

    def unflag_cell(self, index: Tuple[int, int]) -> None:
        """Unflags cell in cell_view"""

        x, y = index
        self.cell_view[y][x] = "cell"

    @staticmethod
    def update_mines_left(mines) -> None:
        """Updates mine counter."""

        print("Mines remaining: " + str(mines))

    @staticmethod
    def display_loss() -> None:
        """Displays the lose label when loss condition is reached."""

        print("You Lose!")

    @staticmethod
    def display_win() -> None:
        """Displays the win label when win condition is reached."""

        print("You Win!")

    def main(self) -> None:
        while True:
            try:
                cmd, *coords = input(
                    "Choose a cell in the format: "
                    + "flag/reveal x y. Type END to quit.  ").split()
                if cmd.lower()[0] == "e":
                    break
                x, y = coords[0], coords[1]
                if cmd.lower()[0] == "f":
                    self.controller.update_flagged_cell((int(x), int(y)))
                elif cmd.lower()[0] == "r":
                    self.controller.reveal_decision((int(x), int(y)))
                else:
                    print("Unknown command")
                self.show_grid()
            except Exception:
                print("Incorrect selection or format")
