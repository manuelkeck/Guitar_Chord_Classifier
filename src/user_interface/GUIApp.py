import tkinter as tk
import cv2

from tkinter import ttk
from screeninfo import get_monitors
from src.user_interface.GUIAppController import GUIAppController
from src.device_handler.Camera import Camera
from PIL import Image, ImageTk


class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recording Tool")

        self.camera = Camera()

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
        self.left_frame = tk.Frame(self.content, width=400, height=300)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.camera_label = ttk.Label(self.left_frame, text="Camera Preview")
        self.camera_label.pack(padx=5, pady=10, anchor="n")
        self.video_label = tk.Label(self.left_frame, width=352, height=198)
        self.video_label.pack(pady=2)
        self.update_camera()

        # Right frame #######################################################
        self.right_frame = tk.Frame(self.content, width=480, height=500)
        self.right_frame.pack(side="left", fill="both", expand=True)

        self.camera_label = ttk.Label(self.right_frame, text="Output")
        self.camera_label.pack(padx=5, pady=10, anchor="nw")
        self.output_frame = ttk.Frame(self.right_frame)
        self.output_frame.pack(padx=5, fill="both", expand=True)
        text_widget_width = int(self.right_frame.winfo_width() * 0.9)
        text_widget_height = int(self.right_frame.winfo_height() * 0.5)
        self.textfield = tk.Text(self.output_frame, wrap="word", height=10, width=50)
        self.textfield.pack(fill="both", expand=True)

        self.specto_button = ttk.Button(self.right_frame, text="Spectogram", width=9, command=self.spectogram)
        self.specto_button.pack(padx=5, anchor="sw")
        self.discard_button = ttk.Button(self.right_frame, text="Discard", width=9, command=self.discard)
        self.discard_button.pack(padx=5, anchor="sw")

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

    def update_camera(self):
        frame = self.camera.get_frame()
        if frame is not None:
            frame = cv2.flip(frame, 1)
            img = Image.fromarray(frame)
            img = img.resize((self.video_label.winfo_width(), self.video_label.winfo_height()), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.video_label.configure(image=img)
            self.video_label.image = img
        self.root.after(10, self.update_camera)

    def on_closing(self):
        self.camera.release()
        self.root.destroy()
