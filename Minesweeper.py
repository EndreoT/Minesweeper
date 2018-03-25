"""
Minesweeper

Creates a basic minesweeper game using tkinter. 
Uses Model-View-Controller architecture.
"""

import tkinter as tk
import random


class Model(object):
    """Crates a minsweeper board and adds mines to it"""
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.create_grid()       
        self.add_mines()
   
    def create_grid(self):
        """Create a self.width by self.height grid of elements with value 0"""
        self.grid = [[0]*self.width for i in range(self.height)]
    
    def add_mines(self):
        """Randomly adds the amount of self.num_mines to grid"""
        def get_coords():
            row = random.randint(0, self.width - 1)
            col = random.randint(0, self.width - 1)
            return row, col
        for i in range(self.num_mines):
            row, col = get_coords()
            while self.grid[row][col] == "b":
                row, col = get_coords()
            self.grid[row][col] = "b"
        for i in self.grid:
            print (i)


class View(tk.Frame):
    """Creates a main window and grid of button cells"""
    def __init__(self, master, width, height, num_mines):
        tk.Frame.__init__(self, master)
        self.master = master    
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.master.title("Minesweeper")
        self.grid()
        self.top_panel = TopPanel(self.master, self.height, 
                                  self.width, self.num_mines)
        self.create_widgets()
        
    def create_widgets(self):
        """Create cell button widgets"""
        self.buttons = {} 
        for i in range(self.height): 
            for j in range(self.width):
                self.buttons[str(i) + "," + str(j)] = tk.Button(
                        self.master, width=5, bg="grey")                                                          
                self.buttons[str(i) + "," + str(j)].grid(row=i+1, column=j+1)                          
        
    def disp_loss(self):
        """Display the loss label when loss condition is reached""" 
        self.top_panel.loss_label.grid(row=0, columnspan=5)
     
    def disp_win(self):
        """Display the win label when win condition is reached""" 
        self.top_panel.win_label.grid(row=0, columnspan=5)
    
    def hide_labels(self, condition=None):
        """Hides labels based on condition argument"""
        if condition:
            self.top_panel.mines_left.grid_remove()
        else: 
            self.top_panel.loss_label.grid_remove()
            self.top_panel.win_label.grid_remove()
            
            
class TopPanel(tk.Frame):
    """Create top panel which houses reset button and win/loss labels"""
    def __init__(self, master, width, height, num_mines):
        tk.Frame.__init__(self, master)
        self.master = master
        self.height = height
        self.width = width
        self.num_mines = num_mines
        self.grid()
        self.create_widgets()
   
    def create_widgets(self):
        self.reset_button = tk.Button(self.master, width = 7, text="Reset")
        self.reset_button.grid(row=0, columnspan=int((self.width*7)/2))
#        Create win and loss labels
        self.loss_label = tk.Label(text="You Lose!", bg="red")
        self.win_label = tk.Label(text="You Win!", bg="green")
#        Create number of mines remaining label
        self.mine_count = tk.StringVar()
        self.mine_count.set("Mines remaining: " + str(self.num_mines))
        self.mines_left = tk.Label(textvariable=self.mine_count)
        self.mines_left.grid(row=0, columnspan=5)
    
   
class Controller(object):
    """Sets up button bindings and minsweeper game logic.
    
    The act of revealing cells is delegated to the methods: give_val(), 
    reveal_cell(), reveal_adj(), and reveal_cont(). End conditions are handled
    by the loss() and win() methods.
    """
    def __init__(self, width, height, num_mines):        
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.model = Model(self.width, self.height, self.num_mines)
        self.root = tk.Tk()
        self.view = View(self.root, self.width, self.height, self.num_mines)        
#        self.color_dict is used to assign colors to cells
        self.color_dict = {
            0: "white", 1:"blue", 2:"green", 
            3:"red", 4:"orange", 5:"purple", 
            6: "grey", 7:"grey", 8: "grey"
            }         
#        Self.count keeps track of cells with value of 0 so that they
#        get revealed with self.reveal_adj call only once
        self.count = []
        self.cells_revealed = []
        self.cells_flagged = []
        self.game_state = None
        self.bindings()
        self.root.mainloop()  
   
    def bindings(self):
        """Set up reveal and flag key bindings for each cell"""
        for i in range(self.height):
            for j in range(self.width):
#                Right click bind to reveal decision method
                self.view.buttons[str(i) + "," + str(j)].bind(
                        "<Button-1>", 
                        lambda event, index=[i, j]:self.reveal(event, index))
#                Left click bind to flag method
                self.view.buttons[str(i) + "," + str(j)].bind(
                        "<Button-3>", 
                        lambda event, index=[i, j]:self.flag(event, index))
#        Set up reset button
        self.view.top_panel.reset_button.bind("<Button>", self.reset)
    
    def reset(self, event): 
        """Resets game. Currently, game setup gets slower with each reset call,
        and window height slightly increases"""
        self.view.hide_labels()
        self.count = []
        self.cells_revealed = []    
        self.cells_flagged = [] 
        self.game_state = None
        self.model = Model(self.width, self.height, self.num_mines)
        self.view = View(self.root, self.width, 
                                     self.height, self.num_mines)
        self.bindings()
    
    def reveal(self, event, index):
        """Main decision method determining how to reveal cell"""
        val = self.give_val(index)
        if val in [x for x in range(1, 9)]:
            self.reveal_cell(val, index)
            self.count.append(index)
        if val == "b" and self.game_state != "win":
            self.game_state = "Loss"
            self.loss()
#        Begin the revealing recursive method when cell value is 0
        if val == 0:            
            self.reveal_cont(index)
    
    def give_val(self, index):
        """Returns the number of adjacent mine. Returns "b" if cell is mine"""
        i = index[0]
        j = index[1]               
        num_mines = 0
        try:
            if self.model.grid[i][j] == "b":
                return "b"
        except IndexError:
            pass                
        def increment():
            try:
                if self.model.grid[pos[0]][pos[1]] == "b":
                    return 1
            except IndexError:
                pass
            return 0       
        additions = [
            [i,j+1], [i+1,j], [i+1,j+1], [i,j-1],
            [i+1,j-1], [i-1,j], [i-1,j+1], [i-1,j-1]
            ]                   
        #Adds 1 to num_mines if cell is adjacent to a mine
        for pos in additions:
            if 0 <= pos[0] <= self.height -1 and 0 <= pos[1] <= self.width - 1:
                num_mines += increment()           
        return num_mines
    
    def reveal_cell(self, value, index):
        """Reveals cell value and assigns an associated color for that value"""
        i = index[0]
        j = index[1]
        cells_unrev = self.height * self.width - len(self.cells_revealed) - 1
        button_key = str(i) + "," + str(j)
        if self.view.buttons[button_key]["text"] == "FLAG":
            pass
        elif value == "b":
            self.view.buttons[button_key].configure(bg="black")
        else:
#           Checks if cell is in the board limits
            if (0 <= i <= self.height - 1 and 
                    0 <= j <= self.width - 1 and 
                    [button_key] not in self.cells_revealed):
                self.view.buttons[button_key].configure(
                        text=value, bg=self.color_dict[value])                     
                self.count.append(button_key)
                self.cells_revealed.append([button_key])               
#            Removes cell from flagged list when the cell gets revealed
            if button_key in self.cells_flagged:
                self.cells_flagged.remove(button_key)
                self.update_mines()
#            Check for win condition
            if (cells_unrev == self.num_mines and not self.game_state):
                self.win()       
    
    def reveal_adj(self, index):        
        """Reveals the 8 adjacent cells to the input cell"""
        org_val = self.give_val(index)
        self.reveal_cell(org_val, index)
        i = index[0]
        j = index[1]
        additions = [
            [i,j+1], [i+1,j], [i+1,j+1], [i,j-1],
            [i+1,j-1], [i-1,j], [i-1,j+1], [i-1,j-1]
            ]        
        for pos in additions:
            if (0 <= pos[0] <= self.height - 1 and 
                    0 <= pos[1] <= self.width - 1):
                new_val = self.give_val(pos)
                self.reveal_cell(new_val, pos) 
    
    def reveal_cont(self, index):
        """Recursive formula that reveals all adjacent cells only if the 
        selected cell has no adjacent mines. 
        (meaning self.give_val(index) == 0)"""     
        i = index[0]
        j = index[1]
        additions = [
            [i,j+1], [i+1,j], [i+1,j+1], [i,j-1],
            [i+1,j-1], [i-1,j], [i-1,j+1], [i-1,j-1]
            ]
        val = self.give_val(index)
        self.reveal_adj(index)
        if val != 0:
            return None
        else:            
            for pos in additions:
                if (0 <= pos[0] <= self.height - 1 and 
                        0 <= pos[1] <= self.width -1 and 
                        self.give_val(pos) == 0 and pos not in self.count):
                    self.count.append(pos)
                    self.reveal_cont(pos)
        
    def win(self):
        """Display win"""
        self.view.hide_labels("mine")
        self.view.disp_win()
        self.game_state = "win"
        
    def loss(self):
        """Display loss. Reveal all cells when a mine is clicked"""
        self.view.hide_labels("mine")
        for i in range(self.height):
            for j in range(self.width):
                val = self.give_val([i, j])
                self.reveal_cell(val, [i, j]) 
        self.view.disp_loss()
    
    def flag(self, event, index):
        """Allows player to flag cells for possible mines. 
        Does not reveal cell."""
        i = index[0]
        j = index[1]
        button_key = str(i) + "," + str(j)
        button_val = self.view.buttons[button_key]       
        if button_val["bg"] == "grey":
            button_val.configure(bg="yellow", text="FLAG")
            self.cells_flagged.append(button_key)
        elif button_val["text"] == "FLAG":
            button_val.configure(bg="grey", text="")
            self.cells_flagged.remove(button_key)
        self.update_mines()
    
    def update_mines(self):
        """Update mine counter"""
        mines_left = self.num_mines - len(self.cells_flagged)
        if mines_left >= 0:
            self.view.top_panel.mine_count.set(
                    "Mines remaining: " + str(mines_left))
                                            

if __name__ == "__main__":
#    c = Controller(9, 9, 10)
#    c = Controller(16, 16, 10)
    c = Controller(16, 16, 40)
