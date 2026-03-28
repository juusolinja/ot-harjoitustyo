from tkinter import ttk, constants
from services.workout_service import workout_service

class UI:
    def __init__(self, root):
        self._root = root
        self._tree = None

    def start(self):
        header = ttk.Label(self._root, text="Workouts")
        header.grid(row=0, column=0, pady=10, sticky=constants.W)

        self._tree = ttk.Treeview(self._root, columns=("Date", "Notes"), show="headings")
        self._tree.heading("Date", text="Date")
        self._tree.heading("Notes", text="Notes")
        self._tree.grid(row=1, column=0, sticky=constants.NSEW)

        self._root.grid_rowconfigure(1, weight=1)
        self._root.grid_columnconfigure(0, weight=1)

        self._refresh_workouts()

    def _refresh_workouts(self):
        for row in self._tree.get_children():
            self._tree.delete(row)

        for workout in workout_service.get_all_workouts():
            self._tree.insert("", constants.END, values=(workout.date, workout.notes))



    

