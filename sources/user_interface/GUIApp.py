import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors
from sources.user_interface.GUIAppController import GUIAppController

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recording Tool")

        # Windows size and positioning (based on main screen)
        window_width = 960
        window_height = 540
        screen = get_monitors()[0]
        x = (screen.width - window_width) // 2
        y = (screen.height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        style = ttk.Style()

        style.configure("TFrame", background="yellow")
        style.configure("TButton", padding=6, relief="flat", background="#d9d9d9")

        self.content = tk.Frame(self.root)

        # Left frame #######################################################
        self.left_frame = tk.Frame(self.content, width=480, height=500, bg="blue")
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.camera_label = ttk.Label(self.left_frame, text="Camera Preview")
        self.camera_label.pack(padx=5, pady=5, anchor="n")
        self.camera_frame = tk.Frame(self.left_frame, width=460, height=270, bg="black")
        self.camera_frame.pack(padx=5, fill="both", expand=True)
        self.camera_placeholder = ttk.Label(self.camera_frame, text="Preview currently not implemented")
        self.camera_placeholder.pack()

        # Right frame #######################################################
        self.right_frame = tk.Frame(self.content, width=480, height=500, bg="green")
        self.right_frame.pack(side="left", fill="both", expand=True)

        self.textfield = tk.Text(self.right_frame, wrap="word", height=100, width=100)

        self.output_frame = ttk.Frame(self.right_frame, width=450, height=300, style="TFrame")
        self.output_frame.pack(padx=5, pady=5, fill="both", expand=True)
        self.output_label = ttk.Label(self.right_frame, text="Output Label")
        self.output_label.pack(padx=5, pady=5, anchor="n")
        self.specto_button = ttk.Button(self.right_frame, text="Spectogram", width=10, command=self.spectogram)
        self.specto_button.pack(padx=5, pady=5, anchor="sw")
        self.discard_button = ttk.Button(self.right_frame, text="Discard", width=10, command=self.discard)
        self.discard_button.pack(padx=5, pady=5, anchor="sw")

        # Bottom frame ######################################################
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side="bottom", fill="x")

        self.quit_frame = tk.Frame(self.bottom_frame)
        self.quit_frame.pack(padx=5, pady=5, side="left")
        self.quit_button = ttk.Button(self.quit_frame, text="Quit", command=root.destroy)
        self.quit_button.pack(padx=5, pady=5, anchor="w")

        self.record_frame = tk.Frame(self.bottom_frame)
        self.record_frame.pack(padx=5, pady=5, side="right")
        self.record_button = ttk.Button(self.record_frame, text="Record", command=self.start_recording)
        self.record_button.pack(padx=5, pady=5, anchor="e")

        self.bottom_frame.pack_propagate(False)
        self.bottom_frame.pack_propagate(True)

        self.content.pack(fill="both", expand=True)

        self.controller = GUIAppController(self)

    def start_recording(self):
        self.controller.start_chord_detection()

    def spectogram(self):
        self.controller.show_spectogram()

    def discard(self):
        self.controller.discard_record()
