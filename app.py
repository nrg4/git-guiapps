import tkinter as tk


"""
nw    n    ne
w   center   e
sw    s    se"""

root = tk.Tk()
root.title("gui_git_app")
root.geometry("800x600")

title_label = tk.Label(root,
                       text="The GUI Git App",
                       font=("Helvetica", 16, *("bold", "italic")))
title_label.pack(
    anchor="w",
    padx=20,
    pady=20
    )


root.mainloop()