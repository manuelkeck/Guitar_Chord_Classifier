import tkinter as tk

from sources.user_interface.GUIApp import GUIApp


def main():
    root = tk.Tk()
    GUIApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
