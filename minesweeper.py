"""
Minesweeper

Implements a basic minesweeper game using the tkinter module.
Uses a Model-View-Controller structure.
"""

from itertools import product
from random import sample
from tkinter import Button, Frame, Label, StringVar, Tk
from typing import Set, Tuple, List, Union


def get_adjacent(index: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """Returns adjacent coordinates for input index"""

    x, y = index

    return {
        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
        (x - 1, y),                 (x + 1, y),
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        }


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


class View(Frame):
    """Creates a GUI with a grid of cell buttons."""

    def __init__(self,
                 width: int,
                 height: int,
                 num_mines: int,
                 controller: "Controller"):
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

    def mainloop(self) -> None:
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


class TextView(object):
    """Creates a text interface of the minesweeper game."""

    def __init__(self,
                 width: int,
                 height: int,
                 num_mines: int,
                 controller: "Controller"
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

    def mainloop(self) -> None:
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


class Controller(object):
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
            self.view = View(self.width, self.height,
                             self.num_mines, self)
        elif view_type == "TEXT":
            self.view = TextView(self.width, self.height,
                                 self.num_mines, self)
        self.view.mainloop()

    def reset(self) -> None:
        """Resets the game"""

        self.view.reset_view()
        self.model = Model(self.width, self.height, self.num_mines)
        self.view = View(self.width, self.height,
                         self.num_mines, self)
        self.view.mainloop()

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


class InitializeGame(Frame):
    """Sets up minesweeper game. Allows player to choose difficulty"""

    def __init__(self):
        self.root = Tk()
        self.create_view_choice()
        self.create_difficulty_widgets()
        self.root.mainloop()

    def create_view_choice(self) -> None:
        """Creates widgets allowing player to choose a view type."""

        self.view_label = Label(self.root, text="Choose a view type")
        self.view_label.grid()
        self.view_types = ["GUI", "TEXT"]

        def create_button(view_type: str) -> Button:
            button = Button(self.root, width=7, bg='grey', text=view_type)
            button.grid()
            return button

        self.view_widgets = [
                                create_button(view_type) for view_type in self.view_types
                            ] + [self.view_label]

        for i in range(2):
            def closure_helper(f, view_choice: str):
                def g(_):
                    f(view_choice)

                return g

            self.view_widgets[i].bind("<Button>", closure_helper(
                self.set_up_difficulty_widgets, self.view_types[i]))

    def create_difficulty_widgets(self) -> None:
        """Set up widgets at start of game for difficulty."""

        self.diff_label = Label(self.root, text="Choose a difficulty")
        self.difficulty = ("Easy", "Medium", "Hard")

        def create_button(difficulty: str) -> Button:
            button = Button(self.root, width=7, bg='grey', text=difficulty)
            return button

        self.difficulty_widgets = [create_button(diff)
                                   for diff in self.difficulty]
        self.difficulty_widgets = [self.diff_label] + self.difficulty_widgets

    def set_up_difficulty_widgets(self, view_type: str) -> None:
        """Removes view widgets. Sets up difficulty options for view chosen."""

        for widget in self.view_widgets:
            widget.grid_remove()

        if view_type == "TEXT":
            self.difficulty_widgets[0].grid()
            self.difficulty_widgets[1].grid()
        else:
            for widget in self.difficulty_widgets:
                widget.grid()
        self.bind_difficulty_widgets(view_type)

    def bind_difficulty_widgets(self, view_type: str) -> None:
        """Binds difficulty buttons."""

        for i in range(1, 4):
            def closure_helper(f, difficulty, view_type):
                def g(_):
                    f(difficulty, view_type)

                return g

            self.difficulty_widgets[i].bind(
                "<Button>", closure_helper(
                    self.init_game, self.difficulty[i - 1], view_type))

    def init_game(self, difficulty: str, view_type: str) -> Controller:
        """Begins game."""

        self.root.destroy()
        return Controller(*{
            'E': (10, 10, 10, difficulty, view_type),
            'M': (16, 16, 40, difficulty, view_type),
            'H': (25, 20, 99, difficulty, view_type)
            }[difficulty[0]]
            )


if __name__ == "__main__":
    game = InitializeGame()
