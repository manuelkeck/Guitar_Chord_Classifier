import tkinter as tk

from src.user_interface.GUIApp import GUIApp


def main():
    """
    Main method to start guitar chord detector with tkinter GUI
    :return: None
    """
    root = tk.Tk()
    GUIApp(root)
    root.protocol("WM_DELETE_WINDOW", GUIApp.on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()
