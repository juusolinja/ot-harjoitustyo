from tkinter import ttk, constants
from ui.workout_view import WorkoutView
from ui.movement_view import MovementManagementView


class UI:
    def __init__(self, root):
        self._root = root
        self._frame = ttk.Frame(master=root)
        self._frame.pack(fill=constants.BOTH, expand=True)
        self._frame.rowconfigure(1, weight=1)
        self._frame.columnconfigure(0, weight=1)
        self._build_navbar()
        self._build_views()

    def _build_navbar(self):
        navbar = ttk.Frame(master=self._frame)
        navbar.grid(row=0, column=0, sticky=constants.EW)
        ttk.Button(navbar, text="Workouts", command=self._show_workout_view).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(navbar, text="Movements", command=self._show_movement_view).grid(row=0, column=1, padx=(0, 5))

    def _build_views(self):
        self._workout_view = WorkoutView(self._frame)
        self._movement_view = MovementManagementView(self._frame, self._refresh_movement_options)
        self._workout_view.grid()
        self._movement_view.grid()
        self._show_workout_view()

    def _show_workout_view(self):
        self._workout_view.tkraise()

    def _show_movement_view(self):
        self._movement_view.refresh()
        self._movement_view.tkraise()

    def start(self):
        self._show_workout_view()

    def _refresh_movement_options(self):
        self._workout_view.refresh_movement_options()
    