import tkinter as tk
from tkinter import ttk, constants
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from services.analysis_service import analysis_service

class VolumeBarChart:
    def __init__(self, parent):
        fig = Figure(figsize=(5, 4), dpi=100)
        self._ax = fig.add_subplot()
        self._canvas = FigureCanvasTkAgg(fig, master=parent)
        self._canvas.get_tk_widget().grid(row=0, column=0, sticky=constants.NSEW)
        self.refresh()

    def refresh(self):
        self._ax.clear()
        volumes = analysis_service.get_current_week_volumes()
        self._ax.bar(volumes.keys(), volumes.values())
        self._ax.set_xlabel("Muscle group")
        self._ax.set_ylabel("Volume")
        self._ax.set_title("Current week completed volume per muscle group")
        self._canvas.draw()

class AnalysisView:
    def __init__(self, root):
        self._frame = ttk.Frame(master=root)
        self._initialize()

    def _initialize(self):
        self._frame.columnconfigure(0, weight=1)
        self._frame.rowconfigure(0, weight=1)
        self._volume_chart = VolumeBarChart(self._frame)

    def refresh(self):
        self._volume_chart.refresh()

    def grid(self):
        self._frame.grid(row=1, column=0, sticky=constants.NSEW)

    def tkraise(self):
        self._frame.tkraise()
        self.refresh()