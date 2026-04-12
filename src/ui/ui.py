from ui.workout_view import WorkoutView


class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        self._show_workout_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_workout_view(self):
        self._hide_current_view()

        self._current_view = WorkoutView(
            self._root
        )

        self._current_view.pack()
