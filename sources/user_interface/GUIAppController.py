import sys
import tkinter as tk


class GUIAppController:
    def __init__(self, gui_app):
        self.gui_app = gui_app

    def start_recording(self, text_output):
        text_output.insert(tk.END, "Aufnahme gestartet...\n")

    def quit_app(self, text_output, master):
        # text_output.insert(tk.END, "Aufnahme beendet.\n")
        master.destroy()
        sys.exit()
