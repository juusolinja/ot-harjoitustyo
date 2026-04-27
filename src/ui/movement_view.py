from tkinter import ttk, constants
import tkinter as tk
from services.movement_service import movement_service
from services.muscle_group_service import muscle_group_service

class MovementManagementView:
    def __init__(self, root, on_add_movement):
        self._frame = ttk.Frame(master=root)
        self._muscle_group_name_var = tk.StringVar()
        self._movement_name_var = tk.StringVar()
        self._muscle_group_var = tk.StringVar()
        self._muscle_group_error_var = tk.StringVar()
        self._movement_error_var = tk.StringVar()
        self._muscle_groups = []
        self._movements = []
        self._selected_muscle_group = None
        self._selected_movement = None
        self._on_add_movement = on_add_movement
        self._initialize()

    def _initialize(self):
        self._frame.columnconfigure(0, weight=1)
        self._frame.columnconfigure(1, weight=1)
        self._frame.rowconfigure(0, weight=1)
        self._build_muscle_group_panel()
        self._build_movement_panel()

    def tkraise(self):
        self._frame.tkraise()

    def grid(self):
        self._frame.grid(row=1, column=0, sticky=constants.NSEW)

    def refresh(self):
        self._selected_muscle_group = None
        self._selected_movement = None
        self._delete_mg_button.configure(state="disabled")
        self._delete_mv_button.configure(state="disabled")
        self._muscle_groups = muscle_group_service.get_all()
        self._movements = movement_service.get_all()
        self._refresh_muscle_group_tree()
        self._refresh_movement_tree()
        self._refresh_muscle_group_dropdown()

    def _build_muscle_group_panel(self):
        frame = ttk.Frame(master=self._frame)
        frame.grid(row=0, column=0, sticky=constants.NSEW, padx=10, pady=10)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        entry_frame = ttk.Frame(master=frame)
        entry_frame.grid(row=0, column=0, sticky=constants.EW, pady=(5, 0))
        entry_frame.columnconfigure(0, weight=1)

        self._mg_entry = ttk.Entry(entry_frame, textvariable=self._muscle_group_name_var)
        self._mg_entry.grid(row=0, column=0, sticky=constants.EW, padx=(5, 5))
        ttk.Button(entry_frame, text="Add", command=self._handle_add_muscle_group).grid(row=0, column=1, padx=(0, 5))

        self._mg_tree = ttk.Treeview(
            master=frame,
            columns=("name",),
            show="headings",
            selectmode="browse"
        )
        self._mg_tree.heading("name", text="Muscle group")
        self._mg_tree.grid(row=1, column=0, sticky=constants.NSEW)
        self._mg_tree.bind("<<TreeviewSelect>>", self._on_muscle_group_select)

        self._mg_error = ttk.Label(frame, textvariable=self._muscle_group_error_var, style="Error.TLabel")
        self._mg_error.grid(row=2, column=0)

        self._delete_mg_button = ttk.Button(frame, text="Delete", state="disabled", command=self._handle_delete_muscle_group)
        self._delete_mg_button.grid(row=3, column=0, pady=(0, 5))

    def _build_movement_panel(self):
        frame = ttk.Frame(master=self._frame)
        frame.grid(row=0, column=1, sticky=constants.NSEW, padx=10, pady=10)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        entry_frame = ttk.Frame(master=frame)
        entry_frame.grid(row=0, column=0, sticky=constants.EW, pady=(5, 0))
        entry_frame.columnconfigure(0, weight=1)

        self._mv_entry = ttk.Entry(entry_frame, textvariable=self._movement_name_var)
        self._mv_entry.grid(row=0, column=0, sticky=constants.EW, padx=(5, 5))

        self._mg_dropdown = ttk.Combobox(entry_frame, textvariable=self._muscle_group_var, state="readonly")
        self._mg_dropdown.grid(row=1, column=0, sticky=constants.EW, padx=(5, 5), pady=(5, 0))

        ttk.Button(entry_frame, text="Add", command=self._handle_add_movement).grid(row=1, column=1, padx=(0, 5), pady=(5, 0))

        self._mv_tree = ttk.Treeview(
            master=frame,
            show="tree",
            selectmode="browse"
        )
        self._mv_tree.grid(row=1, column=0, sticky=constants.NSEW)
        self._mv_tree.bind("<<TreeviewSelect>>", self._on_movement_select)

        self._mv_error = ttk.Label(frame, textvariable=self._movement_error_var, style="Error.TLabel")
        self._mv_error.grid(row=2, column=0)

        self._delete_mv_button = ttk.Button(frame, text="Delete", state="disabled", command=self._handle_delete_movement)
        self._delete_mv_button.grid(row=3, column=0, pady=(0, 5))

    def _refresh_muscle_group_tree(self):
        self._mg_tree.delete(*self._mg_tree.get_children())
        for mg in self._muscle_groups:
            self._mg_tree.insert("", "end", iid=str(mg.id), values=(mg.name,))

    def _refresh_movement_tree(self):
        self._mv_tree.delete(*self._mv_tree.get_children())
        
        groups = {}
        for m in self._movements:
            mg_name = m.primary_muscle_group.name
            groups.setdefault(mg_name, []).append(m)

        for mg_name in sorted(groups.keys()):
            parent_iid = self._mv_tree.insert("", "end", text=mg_name, open=True)
            for m in groups[mg_name]:
                self._mv_tree.insert(parent_iid, "end", iid=str(m.id), text=m.name)

    def _refresh_muscle_group_dropdown(self):
        self._mg_dropdown.configure(values=[mg.name for mg in self._muscle_groups])

    def _on_muscle_group_select(self, event):
        selected = self._mg_tree.selection()
        if not selected:
            self._selected_muscle_group = None
            self._delete_mg_button.configure(state="disabled")
            return
        mg_id = selected[0]
        self._selected_muscle_group = next((mg for mg in self._muscle_groups if str(mg.id) == mg_id), None)
        if self._selected_muscle_group:
            self._delete_mg_button.configure(state="normal")

    def _on_movement_select(self, event):
        selected = self._mv_tree.selection()
        if not selected:
            self._selected_movement = None
            self._delete_mv_button.configure(state="disabled")
            return
        mv_id = selected[0]
        if self._mv_tree.get_children(mv_id):
            self._mv_tree.selection_remove(selected)
            self._selected_movement = None
            self._delete_mv_button.configure(state="disabled")
            return
        self._selected_movement = next((m for m in self._movements if str(m.id) == mv_id), None)
        if self._selected_movement:
            self._delete_mv_button.configure(state="normal")

    def _handle_add_muscle_group(self):
        name = self._muscle_group_name_var.get().strip()
        if not name:
            return
        muscle_group_service.create(name)
        self._muscle_group_name_var.set("")
        self.clear_errors()
        self.refresh()

    def _handle_delete_muscle_group(self):
        if self._selected_muscle_group is None:
            return

        if muscle_group_service.is_referred_to(self._selected_muscle_group):
            self._muscle_group_error_var.set("Cannot delete muscle group that a movement refers to!")
            return
        muscle_group_service.delete(self._selected_muscle_group)
        self._selected_muscle_group = None
        self._delete_mg_button.configure(state="disabled")
        self.clear_errors()
        self.refresh()

    def _handle_add_movement(self):
        name = self._movement_name_var.get().strip()
        muscle_group = next((mg for mg in self._muscle_groups if mg.name == self._muscle_group_var.get()), None)
        if not name or muscle_group is None:
            return
        movement_service.create(name, muscle_group)
        self._movement_name_var.set("")
        self.clear_errors()
        self.refresh()
        self._on_add_movement()

    def _handle_delete_movement(self):
        if self._selected_movement is None:
            return
        if movement_service.is_referred_to(self._selected_movement):
            self._movement_error_var.set("Cannot delete movement that a set refers to!")
            return
        movement_service.delete(self._selected_movement)
        self._selected_movement = None
        self._delete_mv_button.configure(state="disabled")
        self.clear_errors()
        self.refresh()

    def clear_errors(self):
        self._muscle_group_error_var.set("")
        self._movement_error_var.set("")
