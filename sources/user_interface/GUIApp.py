import tkinter as tk
import sys

from tkinter import scrolledtext
from tkinter import Text
from sources.user_interface.GUIAppController import GUIAppController


class GUIApp:
    def __init__(self, master):
        self.master = master
        master.title("Recording Tool")

        # Dynamic size based on screen size (50%)
        #screen_width = master.winfo.screenwidth()
        #screen_height = master.winfo.screenheight()
        #window_width = int(screen_width * 0.5)
        #window_height = int(screen_height * 0.5)

        master.configure(bg='#E0E0E0')

        # Output field
        self.text_output = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=40, height=10)
        self.text_output.pack(pady=10)

        # Terminal
        self.terminal_output = Text(master, wrap=tk.WORD, width=40, height=5)
        self.terminal_output.pack(pady=10)

        # Record Button
        self.record_button = tk.Button(master, text="Record", command=self.start_recording)
        self.record_button.pack(pady=5)

        # Finish Button
        self.finish_button = tk.Button(master, text="Finish", command=self.close_app)
        self.finish_button.pack(pady=5)

        # Reference controller class
        self.gui_app_controller = GUIAppController

        # Set window size
        #master.geometry(
        #    f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}"
        #    f"+{int((screen_height - window_height) / 2)}"
        #)

    def start_recording(self):
        self.gui_app_controller.start_recording(self.text_output)

    def close_app(self):
        self.gui_app_controller.quit_app(self.text_output, self.master)
