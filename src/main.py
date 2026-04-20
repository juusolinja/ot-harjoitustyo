from tkinter import Tk
from ui.ui import UI
from ui.styles import apply_styles


def main():
    window = Tk()
    apply_styles()
    window.title("Workout tracker")
    window.geometry("1400x800")

    ui = UI(window)
    ui.start()

    window.mainloop()


if __name__ == "__main__":
    main()
