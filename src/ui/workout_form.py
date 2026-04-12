import tkinter as tk
from tkinter import ttk, constants
from services.workout_service import workout_service


class WorkoutForm:
    def __init__(self, root, refresh_list, clear_selection_on_new):
        self._refresh_list = refresh_list
        self._clear_selection_on_new = clear_selection_on_new
        self._root = root
        self._frame = ttk.Frame(master=root)
        self._selected_workout = None
        self._pending_sets = []
        self._movements = workout_service.get_all_movement_options()
        self._selected_set_index = None

        self._title_var = tk.StringVar()
        self._date_var = tk.StringVar()
        self._duration_var = tk.IntVar()

        self._movement_var = tk.StringVar()
        self._reps_var = tk.IntVar()
        self._weight_var = tk.DoubleVar()
        self._rir_var = tk.IntVar()

        self._sets_tree = None

        self._initialize()

    def _initialize(self):
        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(2, weight=1)
        self._build_metadata_section()
        self._build_sets_section()
        self._build_buttons()

    def grid(self):
        self._frame.grid(row=0, column=1, sticky=constants.NSEW)

    def _build_metadata_section(self):
        frame = ttk.Frame(master=self._frame)
        frame.columnconfigure(4, weight=1)

        ttk.Label(master=frame, text="Title:").grid(
            row=0, column=0, sticky=constants.W)
        self.title_entry = ttk.Entry(
            master=frame, textvariable=self._title_var)
        self.title_entry.grid(
            row=0, column=1, sticky=constants.EW, padx=(0, 10))

        ttk.Label(master=frame, text="Date (YYYY-MM-DD):").grid(row=1,
                                                                column=0, sticky=constants.W)
        self.date_entry = ttk.Entry(master=frame, textvariable=self._date_var)
        self.date_entry.grid(
            row=1, column=1, sticky=constants.EW, padx=(0, 10))

        ttk.Label(master=frame, text="Duration (min):").grid(
            row=2, column=0, sticky=constants.W)
        self.duration_entry = ttk.Entry(
            master=frame, textvariable=self._duration_var)
        self.duration_entry.grid(
            row=2, column=1, sticky=constants.EW, padx=(0, 10))

        ttk.Label(master=frame, text="Notes:").grid(
            row=0, column=3, rowspan=3, sticky=constants.W)

        notes_frame = ttk.Frame(master=frame)
        notes_frame.grid(row=0, column=4, rowspan=3,
                         sticky=constants.NSEW, pady=(5, 0))
        notes_frame.columnconfigure(0, weight=1)
        notes_frame.rowconfigure(0, weight=1)

        self.notes_text = tk.Text(master=notes_frame, height=5, wrap="word")
        self.notes_text.grid(row=0, column=0, sticky=constants.NSEW)

        scrollbar = ttk.Scrollbar(
            master=notes_frame, orient=constants.VERTICAL, command=self.notes_text.yview)
        scrollbar.grid(row=0, column=1, sticky=constants.NS)
        self.notes_text.configure(yscrollcommand=scrollbar.set)

        frame.grid(row=1, column=0, sticky=constants.NSEW)

    def _build_sets_section(self):
        sets_frame = ttk.Frame(master=self._frame)
        sets_frame.grid(row=2, column=0, sticky=constants.NSEW, pady=10)
        sets_frame.columnconfigure(0, weight=1)
        sets_frame.rowconfigure(0, weight=1)

        self._sets_tree = ttk.Treeview(
            master=sets_frame,
            columns=("weight", "reps", "rir"),
            show="tree headings",
            selectmode="browse"
        )
        self._sets_tree.heading("#0", text="Movement / Set")
        self._sets_tree.heading("weight", text="Weight (kg)")
        self._sets_tree.heading("reps", text="reps")
        self._sets_tree.heading("rir", text="RIR")
        self._sets_tree.grid(row=0, column=0, sticky=constants.NSEW)

        self._sets_tree.bind("<<TreeviewSelect>>", self._on_set_select)

        scrollbar = ttk.Scrollbar(
            sets_frame, orient=constants.VERTICAL, command=self._sets_tree.yview)
        self._sets_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=constants.NS)

        entry_frame = ttk.Frame(master=sets_frame)
        entry_frame.grid(row=2, column=0, columnspan=2,
                         sticky=constants.EW, padx=10)

        ttk.Label(entry_frame, text="Movement").grid(
            row=0, column=0, padx=(0, 5))
        self.movement_dropdown = ttk.Combobox(
            entry_frame,
            textvariable=self._movement_var,
            values=[m.name for m in self._movements],
            state="readonly"
        )
        self.movement_dropdown.grid(row=1, column=0, padx=(0, 5))

        ttk.Label(entry_frame, text="Weight").grid(
            row=0, column=1, padx=(0, 5))
        self.weight_entry = ttk.Entry(
            entry_frame, textvariable=self._weight_var, width=5)
        self.weight_entry.grid(row=1, column=1, padx=(0, 5))

        ttk.Label(entry_frame, text="Reps").grid(row=0, column=2, padx=(0, 5))
        self.reps_entry = ttk.Entry(
            entry_frame, textvariable=self._reps_var, width=5)
        self.reps_entry.grid(row=1, column=2, padx=(0, 5))

        ttk.Label(entry_frame, text="RIR").grid(row=0, column=3, padx=(0, 5))
        self.rir_entry = ttk.Entry(
            entry_frame, textvariable=self._rir_var, width=5)
        self.rir_entry.grid(row=1, column=3, padx=(0, 5))

        self.add_update_button = ttk.Button(
            entry_frame, text="Add/Update", state="disabled", command=self._handle_add_update_set)
        self.add_update_button.grid(row=1, column=4, padx=(0, 5))

        self._new_set_button = ttk.Button(
            entry_frame, text="New set", state="disabled", command=self._handle_new_set)
        self._new_set_button.grid(row=1, column=6, padx=(0, 5))

        self.delete_set_button = ttk.Button(
            entry_frame, text="Delete set", state="disabled", command=self._handle_delete_set)
        self.delete_set_button.grid(row=1, column=5, padx=(0, 5))

    def _build_buttons(self):
        buttons_frame = ttk.Frame(master=self._frame)
        buttons_frame.grid(
            row=3, column=0, sticky=constants.EW, padx=10, pady=10)

        self.new_button = ttk.Button(
            buttons_frame, text="New", command=self._handle_new)
        self.new_button.grid(row=0, column=0, padx=(0, 5))

        self.save_button = ttk.Button(
            buttons_frame, text="Save", state="disabled", command=self._handle_save)
        self.save_button.grid(row=0, column=1, padx=(0, 5))

        self.cancel_button = ttk.Button(
            buttons_frame, text="Cancel", state="disabled", command=self._handle_cancel)
        self.cancel_button.grid(row=0, column=2, padx=(0, 5))

        self.delete_workout_button = ttk.Button(
            buttons_frame, text="Delete workout", state="disabled", command=self._handle_delete_workout)
        self.delete_workout_button.grid(row=0, column=3, padx=(0, 5))

    def _clear_metadata_entries(self):
        self._title_var.set("")
        self._date_var.set("")
        self._duration_var.set(0)
        self.notes_text.delete("1.0", constants.END)

    def _clear_set_entries(self):
        self._movement_var.set("")
        self._weight_var.set(0.0)
        self._reps_var.set(0)
        self._rir_var.set(0)

    def _clear_set_tree(self):
        self._sets_tree.delete(*self._sets_tree.get_children())

    def _clear_form(self):
        self._pending_sets = []
        self._clear_metadata_entries()
        self._clear_set_entries()
        self._clear_set_tree()

    def _handle_new(self):
        self._clear_form()
        self._clear_selection_on_new()
        self._selected_workout = None
        self._selected_set_index = None
        self.delete_workout_button.configure(state="disabled")
        self.cancel_button.configure(state="disabled")
        self.save_button.configure(state="normal")
        self._new_set_button.configure(state="normal")
        self.add_update_button.configure(state="normal")

    def _handle_save(self):
        errors = workout_service.validate_workout()
        if errors:
            return

        if self._selected_workout is None:
            workout = workout_service.create_workout(
                title=self._title_var.get(),
                date=self._date_var.get(),
                duration=self._duration_var.get(),
                notes=self.notes_text.get("1.0", "end-1c"),
                sets=self._pending_sets
            )
            self._selected_workout = workout
        else:
            pending_metadata = {
                "title": self._title_var.get(),
                "date": self._date_var.get(),
                "duration": self._duration_var.get(),
                "notes": self.notes_text.get("1.0", "end-1c")
            }
            updated_workout = workout_service.update_workout(
                self._selected_workout, pending_metadata, self._pending_sets)
            self._selected_workout = updated_workout
        self._refresh_list(self._selected_workout.id)

    def _on_set_select(self, event):
        selected = self._sets_tree.selection()
        if not selected:
            self._selected_set_index = None
            return

        iid = selected[0]
        if self._sets_tree.get_children(iid):
            self._sets_tree.selection_remove(selected)
            self._selected_set_index = None
            return

        self._selected_set_index = int(iid)
        self.delete_set_button.configure(state="normal")
        self.add_update_button.configure(state="normal")
        s = self._pending_sets[self._selected_set_index]
        self._movement_var.set(s["movement_name"])
        self._weight_var.set(s["weight"])
        self._reps_var.set(s["reps"])
        self._rir_var.set(s["rir"])

    def _handle_add_update_set(self):
        movement = next((m for m in self._movements if m.name ==
                        self._movement_var.get()), None)
        if movement is None:
            return
        weight = self._weight_var.get()
        reps = self._reps_var.get()
        rir = self._rir_var.get()
        errors = workout_service.validate_set()
        if not errors:
            set_dict = {
                "movement": movement,
                "weight": weight,
                "reps": reps,
                "rir": rir,
            }
            if self._selected_set_index is None:
                self._pending_sets.append(set_dict)
            else:
                self._pending_sets[self._selected_set_index] = set_dict
                self._clear_set_selection()
            self._refresh_sets_tree()

    def _clear_set_selection(self):
        self._selected_set_index = None
        self._sets_tree.selection_remove(self._sets_tree.selection())
        self._clear_set_entries()

    def _handle_new_set(self):
        self._clear_set_selection()

    def _handle_delete_set(self):
        if self._selected_set_index is None:
            return
        self._pending_sets.pop(self._selected_set_index)
        self._selected_set_index = None
        self._clear_set_entries()
        self._refresh_sets_tree()

    def _refresh_sets_tree(self):
        self._clear_set_tree()
        current_movement = None
        parent_iid = None
        for i, s in enumerate(self._pending_sets):
            if s["movement_name"] != current_movement:
                parent_iid = self._sets_tree.insert("", constants.END,
                                                    text=s["movement_name"],
                                                    open=True
                                                    )
                current_movement = s["movement_name"]
            self._sets_tree.insert(parent_iid, constants.END,
                                   iid=str(i),
                                   values=(s["weight"], s["reps"], s["rir"])
                                   )

    def _handle_cancel(self):
        if self._selected_workout is None:
            self._clear_form()
        else:
            self.load_workout(self._selected_workout)

    def _handle_delete_workout(self):
        if self._selected_workout:
            workout_service.delete_workout(self._selected_workout)
            self._selected_workout = None
            self._clear_form()
            self._refresh_list()

    def load_workout(self, workout):
        self._selected_workout = workout
        self._title_var.set(workout.title)
        self._date_var.set(workout.date)
        self._duration_var.set(workout.duration)
        self.notes_text.delete("1.0", constants.END)
        self.notes_text.insert("1.0", workout.notes or "")

        self._selected_set_index = None

        self._pending_sets = [
            {
                "movement_id": s.movement_id,
                "movement_name": s.movement_name,
                "weight": s.weight,
                "reps": s.reps,
                "rir": s.rir,
            }
            for s in workout.sets
        ]
        self._refresh_sets_tree()
        self.save_button.configure(state="normal")
        self.cancel_button.configure(state="normal")
        self.delete_workout_button.configure(state="normal")
