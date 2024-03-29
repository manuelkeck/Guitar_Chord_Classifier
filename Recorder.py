"""
Author: Manuel Keck
"""
from src.user_interface.GUIApp import GUIApp


def main():
    """
    Main method to start guitar chord detector with tkinter GUI
    :return: None
    """
    app = GUIApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == '__main__':
    main()
