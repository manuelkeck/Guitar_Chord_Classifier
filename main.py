"""
Author: Manuel Keck
"""
from src.user_interface.GUIApp import GUIApp
from src.data.Image import Image


def main():
    """
    Main method to start guitar chord detector with tkinter GUI
    :return: None
    """
    app = GUIApp()
    app.protocol("WM_DELETE_WINDOW", GUIApp.on_closing)
    app.mainloop()


if __name__ == '__main__':
    main()
