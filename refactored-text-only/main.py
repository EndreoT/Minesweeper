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

if __name__ == "__main__":
    TextView(10, 10, 1)
           
  



   