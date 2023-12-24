import tkinter as tk
import cv2
import time
import threading

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
        self.recording_thread = None
        self.recording_thread_running = False
        self.recording_thread_stop = False
        self.camera = Camera()

        # Windows size and positioning (based on main screen)
        window_width = 960
        window_height = 540
        screen = get_monitors()[0]
        x = (screen.width - window_width) // 2
        y = (screen.height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

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
        self.video_label.pack(pady=2)
        self.update_camera()

        # Right frame #######################################################
        self.right_frame = tk.Frame(self.content, width=480, height=500)
        self.right_frame.pack(side="left", fill="both", expand=True)

        self.output_label = ttk.Label(self.right_frame, text="Output")
        self.output_label.pack(padx=5, pady=10, anchor="nw")
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
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(side="bottom", fill="x")

        self.quit_frame = tk.Frame(self.bottom_frame)
        self.quit_frame.pack(padx=5, pady=5, side="left")
        self.quit_button = ttk.Button(self.quit_frame, text="Quit", command=self.destroy)
        self.quit_button.pack(padx=5, pady=5, anchor="w")

        self.record_frame = tk.Frame(self.bottom_frame, bg="blue")
        self.record_frame.pack(padx=5, pady=5, side="right")

        self.progressbar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progressbar.pack(pady=20)

        self.record_button = ttk.Button(self.record_frame, text="Record", command=self.start_recording)
        self.record_button.pack(padx=5, pady=5, anchor="e")

        self.bottom_frame.pack_propagate(False)
        self.bottom_frame.pack_propagate(True)

        self.content.pack(fill="both", expand=True)

        self.controller = GUIAppController(self)

    def start_recording(self):
        def on_thread_complete():
            print("Callback from thread.")
            # self.stop_thread()
            # self.controller.perform_chord_detection()

        if self.recording_thread is not None and self.recording_thread.is_alive():
            print("Thread is already running.")
            return

        self.recording_thread_running = True
        self.recording_thread = threading.Thread(target=lambda: self.task(on_thread_complete))
        self.recording_thread.start()

    def task(self, callback):
        self.controller.record_audio()
        print("Callback will now be called")
        callback()
        while self.recording_thread.is_alive():
            print("Recording thread still alive...")
            time.sleep(1)
        self.controller.perform_chord_detection()

    def update_progressbar(self):
        for i in range(DURATION * 10):  # 10 Updates pro Sekunde
            time.sleep(0.1)
            self.progressbar["value"] = (i + 1) / (DURATION * 10) * 100
            self.update_idletasks()

        self.recording_thread.join()
        self.after_recording()

    def after_recording(self):
        print("After recording called")
        # self.controller.perform_chord_detection()

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
