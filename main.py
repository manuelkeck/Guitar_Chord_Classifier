import tkinter as tk

from sources.user_interface.GUIApp import GUIApp


def main():
    root = tk.Tk()
    GUIApp(root)
    root.protocol("WM_DELETE_WINDOW", GUIApp.on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()
