import tkinter as tk
from tkinter import constants
from ui.workout_list import WorkoutsList
from ui.workout_form import WorkoutForm
from services.workout_service import workout_service


class WorkoutView:
    def __init__(self, root):
        self._root = root
        self._frame = tk.Frame(master=root)
        self._workout_list = WorkoutsList(
            self._frame, self._handle_select_workout)
        self._workout_form = WorkoutForm(
            self._frame, self._refresh_list, self._clear_selection_on_new)

        self._initialize()

    def _initialize(self):
        self._frame.rowconfigure(0, weight=1)
        self._frame.columnconfigure(0, weight=0)
        self._frame.columnconfigure(1, weight=1)

        self._workout_list.grid()
        self._workout_form.grid()

    def grid(self):
        self._frame.grid(row=1, column=0, sticky=constants.NSEW)

    def tkraise(self):
        self._frame.tkraise()

    def _handle_select_workout(self, workout_id):
        workout = workout_service.get_workout_by_id(workout_id)
        self._workout_form.load_workout(workout)

    def _refresh_list(self, workout_id=None):
        self._workout_list._refresh_tree(select_id=workout_id)

    def _clear_selection_on_new(self):
        self._workout_list._clear_selection()

    def refresh_movement_options(self):
        self._workout_form.refresh_movement_options()
