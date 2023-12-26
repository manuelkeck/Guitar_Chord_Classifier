import tkinter as tk
import cv2
import time
import _thread

from tkinter import ttk
from screeninfo import get_monitors
from src.user_interface.GUIAppController import GUIAppController
from src.device_handler.Camera import Camera
from PIL import Image, ImageTk
from Settings import DURATION


class GUIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recording Tool")
        self.camera = Camera()

        # Windows size and positioning (based on main screen)
        window_height = 540
        window_width = 960
        screen = get_monitors()[0]
        y = (screen.height - window_height) // 2
        x = (screen.width - window_width) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(750, 390)

        style = ttk.Style()

        style.configure("TFrame", background="yellow")
        style.configure("TButton", padding=6, relief="flat", background="#d9d9d9")

        self.content = tk.Frame(self)

        # Left frame #######################################################
        self.left_frame = tk.Frame(self.content, width=400, height=300)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.camera_label = ttk.Label(self.left_frame, text="Camera Preview")
        self.camera_label.pack(padx=5, pady=10, anchor="n")
        self.video_label = tk.Label(self.left_frame, width=352, height=198)
        self.video_label.pack()
        self.update_camera()

        # Right frame #######################################################
        self.right_frame = tk.Frame(self.content, width=480, height=500)
        self.right_frame.pack(side="left", fill="both", expand=True)

        self.output_label = ttk.Label(self.right_frame, text="Output")
        self.output_label.pack(padx=3, pady=10, anchor="nw")
        self.output_frame = ttk.Frame(self.right_frame)
        self.output_frame.pack(padx=5, fill="both", expand=True)
        self.textfield = tk.Text(self.output_frame, wrap="word", height=10, width=50)
        self.textfield.pack(fill="both", expand=True)

        self.specto_button = ttk.Button(self.right_frame, text="Spectogram", width=9, command=self.spectogram)
        self.specto_button.pack(padx=5, anchor="sw")

        self.progress_frame = tk.Frame(self.right_frame)
        self.progress_frame.pack(anchor="e", side="right")
        self.discard_button = ttk.Button(self.right_frame, text="Discard", width=9, command=self.discard)
        self.discard_button.pack(padx=5, anchor="sw")
        self.progress_label = ttk.Label(self.progress_frame, text="Recording progress")
        self.progress_label.pack(padx=6, anchor="w")
        self.progressbar = ttk.Progressbar(self.progress_frame, orient="horizontal", length=200, mode="determinate")
        self.progressbar.pack(padx=6, anchor="w", side="left")

        # Bottom frame ######################################################
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(side="bottom", fill="x")

        self.quit_frame = tk.Frame(self.bottom_frame)
        self.quit_frame.pack(padx=5, pady=5, side="left", fill="both")
        self.quit_button = ttk.Button(self.quit_frame, text="Quit", command=self.destroy)
        self.quit_button.pack(padx=5, pady=5, anchor="w")

        self.recording_frame = tk.Frame(self.bottom_frame)
        self.recording_frame.pack(padx=5, side="right", fill="both")
        self.record_button = ttk.Button(self.recording_frame, text="Record", command=self.start_recording)
        self.record_button.pack(padx=5, anchor="e", side="right")

        self.bottom_frame.pack_propagate(False)
        self.bottom_frame.pack_propagate(True)

        self.content.pack(fill="both", expand=True)

        self.controller = GUIAppController(self)

    def start_recording(self):
        _thread.start_new_thread(self.progress_bar, ())
        _thread.start_new_thread(self.record_audio, ())

    def progress_bar(self):
        print("Task 1: Progress bar")
        for i in range(DURATION * 10):
            time.sleep(0.1)
            self.progressbar["value"] = (i + 1) / (DURATION * 10) * 100
            self.update_idletasks()
        print("Both tasks completed, chord detection will be called.")
        self.controller.perform_chord_detection()

    def record_audio(self):
        print("Task 2: Audio Recording")
        self.controller.record_audio()

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
        self.after(10, self.update_camera)

    def on_closing(self):
        self.camera.release()
        self.destroy()
