from tkinter import ttk, constants
from services.workout_service import workout_service


class WorkoutsList:
    def __init__(self, root, handle_select_workout):
        self._root = root
        self._frame = None
        self._tree = None
        self._scrollbar = None
        self._handle_select_workout = handle_select_workout

        self._initialize()

    def grid(self):
        self._frame.grid(row=0, column=0, sticky=constants.NSEW)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._frame.rowconfigure(0, weight=1)
        self._frame.columnconfigure(0, weight=1)
        self._frame.columnconfigure(1, weight=0)

        self._tree = ttk.Treeview(
            master=self._frame,
            columns=("title", "date", "duration"),
            show="headings",
            selectmode="browse"
        )
        self._tree.heading("title", text="Title")
        self._tree.heading("date", text="Date")
        self._tree.heading("duration", text="Duration")

        self._scrollbar = ttk.Scrollbar(
            master=self._frame,
            orient=constants.VERTICAL,
            command=self._tree.yview
        )
        self._tree.configure(yscrollcommand=self._scrollbar.set)

        self._scrollbar.grid(row=0, column=1, sticky=constants.NS)
        self._tree.grid(row=0, column=0, sticky=constants.NSEW)

        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        self._refresh_tree()

    def _on_select(self, event):
        workout_id = self._get_selected_id()
        if workout_id is None:
            return
        self._handle_select_workout(workout_id)

    def _clear_selection(self):
        selection = self._tree.selection()
        if selection is None:
            return
        self._tree.selection_remove(selection)

    def _refresh_tree(self, select_id=None):
        self._tree.delete(*self._tree.get_children())

        summaries = workout_service.get_all_workout_summaries()
        for s in summaries:
            self._tree.insert(
                "",
                constants.END,
                iid=s.workout_id,
                values=(
                    s.title,
                    s.date,
                    s.duration
                )
            )
        if select_id is not None:
            self._tree.selection_set(select_id)

    def _update_workout_summary(self, summary):
        self._tree.item(
            summary.workout_id,
            values=(
                summary.title,
                summary.date,
                summary.duration
            )
        )

    def _delete_workout_summary(self, workout_id):
        self._tree.delete(workout_id)

    def _get_selected_id(self):
        selected = self._tree.selection()
        return int(selected[0]) if selected else None
