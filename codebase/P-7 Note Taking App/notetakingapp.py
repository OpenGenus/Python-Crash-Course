import tkinter as tk
import sqlite3

# Create the main window
window = tk.Tk()
window.title("Note Taking App")
window.geometry("400x300")

# Create a text box
note_entry = tk.Text(window)
note_entry.pack()


# Create a save button and database integration
def save_note():
    note = note_entry.get("1.0", tk.END)
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)")
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (note,))
    conn.commit()
    conn.close()


save_button = tk.Button(window, text="Save Note", command=save_note)
save_button.pack()


# Adding a button to view saved notes
def view_notes():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()

    view_window = tk.Toplevel(window)
    view_window.title("View Notes")
    view_text = tk.Text(view_window)
    for note in notes:
        view_text.insert(tk.END, note[1] + "\n")
    view_text.pack()


view_button = tk.Button(window, text="View Notes", command=view_notes)
view_button.pack()

# Run the application
window.mainloop()
