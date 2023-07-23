import random
from re import X
from tkinter import Button, Label
import ctypes
import sys

class Cell:
    all = []
    cell_count_label_obj = None
    cell_count = 27
    def __init__(self, x, y, is_mine = False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_cell = False
        self.cell_btn = None
        self.x = x 
        self.y = y

        #append the objects to the Cell.all list to store all the instances of the Cell class
        Cell.all.append(self)

    def create_btn(self, location):
        btn = Button(location, width =9, height=3)
        
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)

        self.cell_btn = btn 

    @staticmethod
    def create_cell_count(location):
        label = Label(
            location,
            bg='#ffcc99',
            text = f"Cells left = {Cell.cell_count}",
            width = 12,
            height = 3,
            font=("", 18)
        )
        Cell.cell_count_label_obj = label
    
    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.mines_len == 0:
                for obj in self.surround_cells:
                    obj.show_cell()
            self.show_cell()
            if Cell.cell_count == 0:
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won!', 'Game over', 0)



        self.cell_btn.unbind('<Button-1>')
        self.cell_btn.unbind('<Button-3>')

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surround_cells(self):
        surrounding_cells = [
            self.get_cell_by_axis(self.x - 1, self.y -1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
            ]

        surrounding_cells = [cell for cell in surrounding_cells if cell is not None]
        #print(surrounding_cells)
        return surrounding_cells

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn.configure(text=self.mines_len)

            if Cell.cell_count_label_obj:
                Cell.cell_count_label_obj.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            
            self.cell_btn.configure(bg='SystemButtonFace')
        self.is_opened = True

    
    @property
    def mines_len(self):
        i = 0
        for cell in self.surround_cells:
            if cell.is_mine:
                i += 1
        return i

    def show_mine(self):
        self.cell_btn.configure(bg = 'red')
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game over', 0)
        sys.exit()
        

    def right_click_actions(self, event):
        if not self.is_mine_cell:
            self.cell_btn.configure(bg='orange')
            self.is_mine_cell = True

        else:
            self.cell_btn.configure(bg='SystemButtonFace')
            self.is_mine_cell = False



    @staticmethod
    def randomize_mines():
        picked_as_mines = random.sample(Cell.all, 9)
        
        for picked_mine in picked_as_mines:
            picked_mine.is_mine = True

        

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
