"""
Author: Manuel Keck
"""
import tkinter as tk
import cv2
import time
import _thread

from tkinter import ttk
from screeninfo import get_monitors
from src.user_interface.GUIAppController import GUIAppController
from src.device_handler.Camera import Camera
from src.data.Image import ImageProcessing
from PIL import Image, ImageTk
from Settings import DURATION


class GUIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recording Tool")
        self.camera = Camera(self)
        self.controller = GUIAppController(self)

        # Windows size and positioning (based on main screen)
        window_height = 560
        window_width = 1000
        screen = get_monitors()[0]
        y = (screen.height - window_height) // 2
        x = (screen.width - window_width) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(750, 390)

        # style = ttk.Style()

        # style.configure("TFrame", background="yellow")
        # style.configure("TButton", padding=6, relief="flat", background="#d9d9d9")

        # Main frame #######################################################
        self.content = tk.Frame(self)
        self.content.pack(fill="both", expand=True)

        # Left frame #######################################################
        self.left_frame = tk.Frame(self.content, width=400, height=300)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.left_frame.pack_propagate(False)

        self.camera_label = ttk.Label(self.left_frame, text="Camera Preview")
        self.camera_label.pack(padx=5, pady=10, anchor="n")
        self.video_label = tk.Label(self.left_frame, width=352, height=198)
        self.video_label.pack(pady=3)
        self.update_camera()
        self.landmark_image = tk.Label(self.left_frame, width=352, height=198)
        self.landmark_image.pack(pady=10, anchor="s")

        # Right frame #######################################################
        self.right_frame = tk.Frame(self.content, width=480, height=500)
        self.right_frame.pack(side="left", fill="both", expand=True)

        self.output_label = ttk.Label(self.right_frame, text="Output")
        self.output_label.pack(padx=3, pady=10, anchor="nw")
        self.output_frame = ttk.Frame(self.right_frame)
        self.output_frame.pack(padx=5, fill="both", expand=True)
        self.textfield = tk.Text(self.output_frame, wrap="word", height=10, width=50)
        self.textfield.pack(fill="both", expand=True)
        self.textfield.config(state="disabled")

        self.specto_button = ttk.Button(self.right_frame, text="Spectogram", width=9, command=self.spectogram)
        self.specto_button.pack(padx=5, anchor="sw")
        # self.test_button = ttk.Button(self.right_frame, text="Bild", command=self.show_captured_image)
        # self.test_button.pack()

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

    def start_recording(self):
        self.record_button["state"] = "disable"
        _thread.start_new_thread(self.main_task, ())
        _thread.start_new_thread(self.record_audio, ())

    def main_task(self):
        """
        Contains progressbar and further processing of logic after recording is done
        """
        print(f"Task 1: GUI with progress bar. Thread-ID: {_thread.get_ident()}")
        for i in range(DURATION * 10):
            time.sleep(0.1)
            self.progressbar["value"] = (i + 1) / (DURATION * 10) * 100
            self.update_idletasks()
        print("Both tasks completed, chord detection will be called.")
        self.controller.perform_chord_detection()
        # print(f"Path: {self.controller.latest_image_path}")
        # self.show_captured_image(self.controller.latest_image_path)
        self.record_button["state"] = "normal"

    def record_audio(self):
        print(f"Task 2: Audio Recording. Thread-ID: {_thread.get_ident()}")
        self.controller.record_audio()

    def spectogram(self):
        self.controller.show_spectogram()

    def discard(self):
        self.controller.discard_record()

    def update_camera(self):
        frame = self.camera.get_frame()
        if frame is not None:
            # frame = cv2.flip(frame, 1)
            img = Image.fromarray(frame)
            img = img.resize((self.video_label.winfo_width(), self.video_label.winfo_height()), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.video_label.configure(image=img)
            self.video_label.image = img
        self.after(10, self.update_camera)

    # def show_captured_image(self):
    #     image = self.controller.show_landmark_image()
    #     cv2.imshow("Landmark Image", image)
    #     cv2.waitKey()
    #     cv2.destroyWindow("Landmark Image")
    #     # print(type(image))
    #     # image_pil = Image.fromarray(image)
    #     # image_pil = image_pil.resize((self.landmark_image.winfo_width(), self.landmark_image.winfo_height()), Image.LANCZOS)
    #     # image_tk = ImageTk.PhotoImage(image=image_pil)
    #     # self.landmark_image.config(image=image_tk)
    #     # self.landmark_image.image = image_tk

    def on_closing(self):
        self.camera.release()
        self.destroy()
