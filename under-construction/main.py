from enum import Enum
from tkinter import Button, Label, Tk
from typing import Set, Tuple, List, Union

from coordinate import Coordinate
from controller import Controller
from getAdjacent import get_adjacent
from views import TextView


"""
Implements a basic minesweeper game using the tkinter module.
Uses a Model-View-Controller structure.
"""

# TODO: implement Difficult Enum into InitializeGame
# class Difficulty(Enum):

#     EASY = 0
#     MEDIUM = 1
#     HARD = 2

#     def is_easy(self):
#         return self.value == 0
    
#     def is_medium(self):
#         return self.value == 1
    
#     def is_hard(self):
#         return self.value == 2


class InitializeGame:
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
        return TextView(*{
            'E': (10, 10, 10), 
            'M': (16, 16, 40),
            'H': (25, 20, 99)
            }[difficulty[0]]
            )


if __name__ == "__main__":
    game = InitializeGame()
  



   