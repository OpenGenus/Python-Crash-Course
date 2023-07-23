from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser

root = Tk()
root.title("Simple Text Editor")
root.geometry("1000x600")
root.resizable(True,True)

# set variable for open file name
global open_status_name
open_status_name = False

global selected
selected = False

# create a toolbar
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X, pady=5)

# create a main frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# create scrollbar for the textbox
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# horizontal scrollbar
hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

# create text box
my_text = Text(my_frame, width=80, height=20, font=("Helvetica", 16), selectbackground="lightgrey",
               selectforeground="black", undo=True,
               yscrollcommand=text_scroll.set, xscrollcommand=hor_scroll.set, wrap="none")
my_text.pack()

# configure scrollbar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

# create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# add status bar to bottom
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

# ***************************** File Menu ********************************
# create new file function
def new_file(e):
    # Delete previous file
    my_text.delete("1.0", END)
    # Update status bar
    root.title("Untitled")
    status_bar.config(text="New File        ")

    global open_status_name
    open_status_name = False

# openn files
def open_file(e):
    my_text.delete("1.0", END)
    # Grab filename
    text_file = filedialog.askopenfilename(initialdir="E:/", title="Open File",
                filetypes=(
                    ("Text Files", "*.txt"),("HTML Files", "*.html"),
                    ("Python Files", "*.py"),("All Files", "*.*")
                ))
    # check to see if there is a file name
    if text_file:
        global open_status_name
        open_status_name = text_file

    # update status bar
    name = text_file
    status_bar.config(text=f'{name}        ')
    name = name.replace("E:/", "")
    root.title(f'{name}')

    # open file to read
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    # add file to textbox
    my_text.insert(END, stuff)
    # close opened file
    text_file.close()

def save_as_file(e):
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="E:/", title="Save File",
                            filetypes=(
                                        ("Text Files", "*.txt"), ("HTML Files", "*.html"),
                                        ("Python Files", "*.py"), ("All Files", "*.*")
                                    ))
    if text_file:
        name = text_file
        status_bar.config(text=f'Saved: {name}        ')
        name = name.replace("E:/", "")
        root.title(f'{name}')

    # save the file
    text_file = open(text_file, 'w')
    text_file.write(my_text.get(1.0, END))
    # close the file
    text_file.close()

def save_file(e):
    global open_status_name
    if open_status_name:
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        # close the file
        text_file.close()

        status_bar.config(text=f'Saved: {open_status_name}        ')

    else:
        save_as_file(e)


# add file menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="(Ctrl+n)")
file_menu.add_command(label="Open", command=open_file, accelerator="(Ctrl+o)")
file_menu.add_command(label="Save", command=save_file, accelerator="(Ctrl+s)")
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# file bindings
root.bind('<Control-Key-n>', new_file)
root.bind('<Control-Key-o>', open_file)
root.bind('<Control-Key-s>', save_file)


# ************************* Edit Menu *************************

# cut text
def cut_text(e):
    global selected
    # check keyboard shortcuts action
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            # grab selected text
            selected = my_text.selection_get()
            # delete selected text
            my_text.delete("sel.first", "sel.last")
            # clear the clipboard then append
            root.clipboard_clear()
            root.clipboard_append(selected)

# copy text
def copy_text(e):
    global selected
    # check keyboard shortcuts action
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        # grab selected text
        selected = my_text.selection_get()
        # clear the clipboard then append
        root.clipboard_clear()
        root.clipboard_append(selected)


# paste text
def paste_text(e):
    global selected
    # check keyboard shortcuts action
    if e:
        selected = root.clipboard_get()

    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)

# Select all
def select_all(e):
    # add sel tag to select all text
    my_text.tag_add('sel', '1.0', 'end')

# add edit menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="(Ctrl+x)")
edit_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="(Ctrl+c)")
edit_menu.add_command(label="Paste", command=lambda: paste_text(False), accelerator="(Ctrl+v)")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+z)")
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="(Ctrl+y)")
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=lambda: select_all(True), accelerator="(Ctrl+a)")

# edit bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

# select binding
root.bind('Control-A', select_all)
root.bind('Control-a', select_all)

# **************************** Format Menu ******************************

# change bg color
def bg_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)

# change all text color
def all_text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(fg=my_color)

def wrap():
    if word_wrap.get() == True:
        my_text.config(wrap="word")
    else:
        my_text.config(wrap="none")

# find text
def check(value, e):
    my_text.tag_remove('found', "1.0", "end")
    my_text.tag_config('found', foreground='red')
    list_of_words = value.split(' ')
    for word in list_of_words:
        index = "1.0"
        while index:
            index = my_text.search(word, index, nocase=1, stopindex=END)
            if index:
                lastIndex = '%s+%dc' % (index, len(word))
                my_text.tag_add('found', index, lastIndex)
                index = lastIndex

# cancel search
def cancel_search(value):
    my_text.tag_remove('found', "1.0", "end")
    value.destroy()
    return "break"

# create search box
def find_text(e):
    search = Toplevel(root)
    search.title(' Find Text ')
    search.transient(root)
    search.resizable(False, False)
    Label(search, text=' Find All:').grid(row=0, column=0, sticky='e')
    x = search.winfo_x()
    y = search.winfo_y()
    search.geometry("+%d+%d" % (x+500, y+300))
    entry_widget = Entry(search, width=25)
    entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    entry_widget.focus_set()
    Button(search, text='Search', underline=0,
           command=lambda: check(entry_widget.get(), e)).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=5)
    Button(search, text='Cancel', underline=0,
           command=lambda: cancel_search(search)).grid(row=0, column=4, sticky='e'+'w', padx=2, pady=5)


# add format menu
format_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Format", menu=format_menu)
# format_menu.add_command(label="Selected Text Color", command=text_color)
format_menu.add_command(label="All Text Color", command=all_text_color)
format_menu.add_command(label="Background Color", command=bg_color)
format_menu.add_command(label="Search", command=find_text, accelerator="(Ctrl+f)")
format_menu.add_separator()
word_wrap = BooleanVar()
format_menu.add_checkbutton(label="Word Wrap", onvalue=True, offvalue=False, variable=word_wrap, command=wrap)
root.bind('<Control-Key-f>', find_text)

# ***************************** ToolBar *****************************

# bold text
def bold():
    # create a font
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")

    # configure a tag
    my_text.tag_configure("bold", font=bold_font)
    current_tags = my_text.tag_names("sel.first")

    # If state to see if a tag has been set
    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")

    else:
        my_text.tag_add("bold", "sel.first", "sel.last")

# italic text
def italic():
    # create a font
    italic_font = font.Font(my_text, my_text.cget("font"))
    italic_font.configure(slant="italic")

    # configure a tag
    my_text.tag_configure("italic", font=italic_font)
    current_tags = my_text.tag_names("sel.first")

    # If state to see if a tag has been set
    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")

    else:
        my_text.tag_add("italic", "sel.first", "sel.last")

# change text color
def text_color():
    # pick a color
    my_color = colorchooser.askcolor()[1]
    if my_color:
        status_bar.config(text=my_color)

        # color text
        color_font = font.Font(my_text, my_text.cget("font"))

        # configure a tag
        my_text.tag_configure("colored", font=color_font, foreground=my_color)
        current_tags = my_text.tag_names("sel.first")

        # If state to see if a tag has been set
        if "colored" in current_tags:
            my_text.tag_remove("colored", "sel.first", "sel.last")

        else:
            my_text.tag_add("colored", "sel.first", "sel.last")

# underline text
def underline():
    # create a font
    underline_font = font.Font(my_text, my_text.cget("font"))
    underline_font.configure(underline=True)

    # configure a tag
    my_text.tag_configure("underline", font=underline_font)
    current_tags = my_text.tag_names("sel.first")

    # If state to see if a tag has been set
    if "underline" in current_tags:
        my_text.tag_remove("underline", "sel.first", "sel.last")

    else:
        my_text.tag_add("underline", "sel.first", "sel.last")

# strike text
def strike():
    # create a font
    strike_font = font.Font(my_text, my_text.cget("font"))
    strike_font.configure(overstrike=True)

    # configure a tag
    my_text.tag_configure("overstrike", font=strike_font)
    current_tags = my_text.tag_names("sel.first")

    # If state to see if a tag has been set
    if "overstrike" in current_tags:
        my_text.tag_remove("overstrike", "sel.first", "sel.last")

    else:
        my_text.tag_add("overstrike", "sel.first", "sel.last")

def remove_align_tags():
    current_tags = my_text.tag_names("sel.first")
    if "left" in current_tags:
        my_text.tag_remove("left", "sel.first", "sel.last")
    if "right" in current_tags:
        my_text.tag_remove("right", "sel.first", "sel.last")
    if "center" in current_tags:
        my_text.tag_remove("center", "sel.first", "sel.last")

def align_left():
    remove_align_tags()
    my_text.tag_configure("left", justify='left')
    my_text.tag_add("left", "sel.first", "sel.last")

def align_right():
    remove_align_tags()
    my_text.tag_configure("right", justify='right')
    my_text.tag_add("right", "sel.first", "sel.last")

def align_middle():
    remove_align_tags()
    my_text.tag_configure("center", justify='center')
    my_text.tag_add("center", "sel.first", "sel.last")

def align_justify():
    remove_align_tags()

# **************** Create Toolbar buttons *********************

# undo & redo button
undo_icon = ImageTk.PhotoImage(Image.open("icons/undo.png").resize((15,15), Image.LANCZOS))
undo_button = Button(toolbar_frame, borderwidth=0., image=undo_icon, command=my_text.edit_undo)
undo_button.grid(row=0, column=0, sticky=W, padx=8, pady=2)

redo_icon = ImageTk.PhotoImage(Image.open("icons/redo.png").resize((15,15), Image.LANCZOS))
redo_button = Button(toolbar_frame, borderwidth=0., image=redo_icon, command=my_text.edit_redo)
redo_button.grid(row=0, column=1, sticky=W, padx=8, pady=2)

# bold button
bold_icon = ImageTk.PhotoImage(Image.open("icons/bold.png").resize((15,15), Image.LANCZOS))
bold_button = Button(toolbar_frame, borderwidth=0., image=bold_icon, command=bold)
bold_button.grid(row=0, column=3, sticky=W, padx=8, pady=2)

# italic button
italic_icon = ImageTk.PhotoImage(Image.open("icons/italics.png").resize((15,15), Image.LANCZOS))
italic_button = Button(toolbar_frame, borderwidth=0., image=italic_icon, command=italic)
italic_button.grid(row=0, column=4, sticky=W, padx=8, pady=2)

# underline button
underline_icon = ImageTk.PhotoImage(Image.open("icons/underline.png").resize((15,15), Image.LANCZOS))
underline_button = Button(toolbar_frame, borderwidth=0., image=underline_icon, command=underline)
underline_button.grid(row=0, column=5, sticky=W, padx=8, pady=2)

# overstrike button
strike_icon = ImageTk.PhotoImage(Image.open("icons/strike.png").resize((15,15), Image.LANCZOS))
strike_button = Button(toolbar_frame, borderwidth=0., image=strike_icon, command=strike)
strike_button.grid(row=0, column=6, sticky=W, padx=8, pady=2)

# text color
color_icon = ImageTk.PhotoImage(Image.open("icons/color.png").resize((18,18), Image.LANCZOS))
color_text_button = Button(toolbar_frame, borderwidth=0., image=color_icon, command=text_color)
color_text_button.grid(row=0, column=7, padx=8, pady=2)

# align left
left_icon = ImageTk.PhotoImage(Image.open("icons/align_left.png").resize((18,18), Image.LANCZOS))
left_button = Button(toolbar_frame, borderwidth=0., image=left_icon, command=align_left)
left_button.grid(row=0, column=8, padx=8, pady=2)

# align right
right_icon = ImageTk.PhotoImage(Image.open("icons/align_right.png").resize((18,18), Image.LANCZOS))
right_button = Button(toolbar_frame, borderwidth=0., image=right_icon, command=align_right)
right_button.grid(row=0, column=9, padx=8, pady=2)

# align center
center_icon = ImageTk.PhotoImage(Image.open("icons/align_middle.png").resize((18,18), Image.LANCZOS))
center_button = Button(toolbar_frame, borderwidth=0., image=center_icon, command=align_middle)
center_button.grid(row=0, column=10, padx=8, pady=2)

# align justify
justify_icon = ImageTk.PhotoImage(Image.open("icons/align_justify.png").resize((18,18), Image.LANCZOS))
justify_button = Button(toolbar_frame, borderwidth=0., image=justify_icon, command=align_justify)
justify_button.grid(row=0, column=11, padx=8, pady=2)


root.mainloop()