"""
Author: Manuel Keck
"""
from src.user_interface.GUIApp import GUIApp
from src.train_model.TrainModelHelpers import split_dataset, get_amount_of_images


def main():
    """
    Main method to start guitar chord detector with tkinter GUI
    :return: None
    """
    # app = GUIApp()
    # app.protocol("WM_DELETE_WINDOW", GUIApp.on_closing)
    # app.mainloop()

    # split_dataset()
    get_amount_of_images()


if __name__ == '__main__':
    main()
