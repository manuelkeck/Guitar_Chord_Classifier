import tkinter as tk

from tkinter import ttk
from screeninfo import get_monitors
from sources.user_interface.GUIAppController import GUIAppController


class GUIApp:
    def __init__(self, root):


        self.root = root
        self.root.title("Recording Tool")
        # root.resizable(False, False)
        # self.controller = controller

        # Windows size and positioning (based on main screen)
        window_width = 960
        window_height = 540
        screen = get_monitors()[0]
        x = (screen.width - window_width) // 2
        y = (screen.height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        style = ttk.Style()

        style.configure("TFrame", background="black")
        style.configure("TButton", padding=6, relief="flat", background="#d9d9d9")

        # Left frame
        self.left_frame = tk.Frame(root, width=480, height=500, bg="red")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.camera_frame = tk.Frame(self.left_frame, width=450, height=100, bg="black")
        self.camera_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.camera_label = ttk.Label(self.left_frame, text="Camera Label")
        self.camera_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Right frame
        self.right_frame = tk.Frame(root, width=480, height=500, bg="green")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.output_frame = ttk.Frame(self.right_frame, width=450, height=300, style="TFrame")
        self.output_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.output_label = ttk.Label(self.right_frame, text="Output Label")
        self.output_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.specto_button = ttk.Button(self.right_frame, text="Spectogram", width=10, command=self.spectogram)
        self.specto_button.grid(row=1, column=0, padx=5, pady=5, sticky="sw")

        self.discard_button = ttk.Button(self.right_frame, text="Discard", width=10)
        self.discard_button.grid(row=2, column=0, padx=5, pady=5, sticky="sw")

        # Quit
        self.quit_button = ttk.Button(self.root, text="Quit", command=root.destroy)
        self.quit_button.grid(row=2, column=0, padx=5, pady=5, sticky="sw")

        # Record
        self.record_button = ttk.Button(self.root, text="Record", command=self.start_recording)
        self.record_button.grid(row=2, column=1, padx=5, pady=5, sticky="se")

        # self.root.grid_rowconfigure(0, weight=1)
        # self.left_frame.grid_rowconfigure(0, weight=1)
        # self.right_frame.grid_rowconfigure(0, weight=1)

        self.controller = GUIAppController(self)

    def start_recording(self):
        self.controller.start_chord_detection()

    def spectogram(self):
        self.controller.show_spectogram()
