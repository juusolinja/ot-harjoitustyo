from tkinter import ttk

def apply_styles():
    style = ttk.Style()
    style.configure("Treeview", rowheight=20)
    style.configure("Error.TLabel", foreground="#ff1744")
