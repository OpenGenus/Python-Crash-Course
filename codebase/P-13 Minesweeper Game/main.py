from tkinter import *
from cell import Cell   
import configuration

#instantiate a window instance

root = Tk()

#change the dimensions of the window, function accepts string 'widthxheight'
root.geometry(f'{configuration.WIDTH}x{configuration.HEIGHT}')
root.title('Minesweeper')

root.configure(bg='#ffcc99')
#to disable resizing of the main window
root.resizable(False, False)

#frames

top_frame = Frame(root, bg='#ffcc99', width=700, height = 140)
top_frame.place(x = 0, y = 0)

game_title = Label(
    top_frame,
    bg = 'black',
    fg = 'white',
    text = 'Minesweeper',
    font = ('', 30)
)

game_title.place(x=10 , y=10)

left_frame = Frame(root, bg='#ffcc99', width = 200, height = 560)
left_frame.place(x = 0, y = 140)

center_frame = Frame(root, bg='#ffcc99', width = 500, height = 560)
center_frame.place(x=200, y = 140)


for x in range(6):
    for y in range(6):
         c = Cell(x, y)
         c.create_btn(center_frame)
         c.cell_btn.grid(column=x, row=y)

Cell.create_cell_count(left_frame)
Cell.cell_count_label_obj.place(x=12, y=0)
Cell.randomize_mines()


#to run the window
root.mainloop()    
