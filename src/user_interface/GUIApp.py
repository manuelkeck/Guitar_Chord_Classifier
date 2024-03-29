"""
Author: Manuel Keck
"""
import tkinter as tk
import time
import _thread
import cv2
import mediapipe as mp
import os.path

from tkinter import ttk

import numpy as np
from screeninfo import get_monitors
from src.user_interface.GUIAppController import GUIAppController
from src.device_handler.Camera import Camera
from src.train_model.ChordDetectionVGG16 import ChordDetectionVGG16
from src.train_model.TrainModelHelpers import resize_image
from PIL import Image, ImageTk, ImageOps
from Settings import DURATION, CLASSES, AMOUNT, ROOT_DIR, CLASSES_MAP
from tensorflow.keras.applications.vgg16 import preprocess_input

# Init mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Load model
path = os.path.join(ROOT_DIR, "output/vgg/model/vgg16_model_v4.keras")
model = ChordDetectionVGG16()
model.load_model(path)


class GUIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.chord_text = None
        self.title("Recording Tool")
        self.controller = GUIAppController(self)
        self.camera = Camera(self, self.controller)
        self.recalculated_width, self.recalculated_height = None, None
        self.predicted_chord: str = ''

        # Windows size and positioning (based on user's main screen)
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
        self.video_label = tk.Label(self.left_frame, width=348, height=194)
        self.video_label.pack(pady=3)
        self.canvas = tk.Canvas(self.video_label, width=50, height=50, borderwidth=0, highlightthickness=0)
        self.after(100, self.delayed_aspect_ratio)
        self.after(100, self.update_camera)
        self.landmark_image = tk.Label(self.left_frame, width=348, height=194)
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

        self.spectro_button = ttk.Button(self.right_frame, text="Spectrogram", width=10, command=self.spectrogram)
        self.spectro_button.pack(padx=5, pady=5, anchor="sw")

        self.progress_frame = tk.Frame(self.right_frame)
        self.progress_frame.pack(anchor="e", side="right")
        self.discard_button = ttk.Button(self.right_frame, text="Discard", width=10, command=self.discard)
        self.discard_button.pack(padx=5, pady=5, anchor="sw")
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
        self.create_button = ttk.Button(self.recording_frame, text="Create", command=self.open_popup)
        self.create_button.pack(padx=5, anchor="e", side="right")
        self.chord_classifier_button = ttk.Button(self.recording_frame, text="Chord Classifier",
                                                  command=self.toggle_view)
        self.chord_classifier_button.pack(padx=5, anchor="e", side="left")

        self.bottom_frame.pack_propagate(False)
        self.bottom_frame.pack_propagate(True)

    def open_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Chord")

        main_window_x = self.winfo_x()
        main_window_y = self.winfo_y()
        main_window_width = self.winfo_width()
        main_window_height = self.winfo_height()

        popup_width = 250
        popup_height = 150
        popup_x = main_window_x + (main_window_width - popup_width) // 2
        popup_y = main_window_y + (main_window_height - popup_height) // 2

        popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        container = tk.Frame(popup)
        container.pack()
        label = tk.Label(container, text="Enter the chord for which you want\n to capture images for the dataset:")
        label.pack()
        entry = tk.Entry(container)
        entry.pack()
        confirm_button = tk.Button(popup, text="Confirm", command=lambda: self.on_confirm(entry.get(), popup))
        confirm_button.pack(side=tk.RIGHT, padx=(10, 20), pady=10)

        cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy)
        cancel_button.pack(side=tk.LEFT, padx=(20, 10), pady=10)

    def on_confirm(self, user_input, popup):
        self.record_button["state"] = "disable"
        self.create_button["state"] = "disable"
        print("User input:", user_input)
        popup.destroy()

        if user_input in CLASSES or user_input == "None":
            self.controller.add_text(f"Capturing images for chord {user_input} "
                                     f"will be started.")
            _thread.start_new_thread(self.main_task, (AMOUNT, "fast-lane"))
            _thread.start_new_thread(self.controller.chord_fastlane_dataset, (user_input,))
        else:
            self.controller.add_text("Please enter one of the following chords: "
                                     "A, Am, Bm, C, D, Dm, E, Em, F, G or 'None'.")

    def start_recording(self):
        self.record_button["state"] = "disable"
        self.create_button["state"] = "disable"
        _thread.start_new_thread(self.main_task, (DURATION, ""))
        _thread.start_new_thread(self.record_audio, ())

    def main_task(self, duration: int, flag: str):
        """
        Contains progressbar and further processing of logic after recording is done
        """
        print(f"Task 1: GUI with progress bar. Thread-ID: {_thread.get_ident()}")

        time.sleep(0.5)

        if flag != "fast-lane":
            for i in range(duration * 10):
                time.sleep(0.1)
                self.progressbar["value"] = (i + 1) / (duration * 10) * 100
                self.update_idletasks()

            # Will be started after x=DURATION time, with a one-second delay
            self.controller.perform_chord_detection()
        else:
            print("Fast-lane dataset creation selected. Progressbar will not be updated. Check logs in terminal.")

        self.record_button["state"] = "normal"
        self.create_button["state"] = "normal"

    def record_audio(self):
        print(f"Task 2: Audio Recording. Thread-ID: {_thread.get_ident()}")
        self.controller.record_audio()

    def spectrogram(self):
        self.controller.show_spectrogram()

    def discard(self):
        self.controller.discard_record()

    def aspect_ratio(self):
        frame = self.camera.get_frame()

        # Calculate webcam aspect ratio
        video_aspect = frame.shape[1] / frame.shape[0]
        print(f"Identified webcam resolution: {frame.shape[1]} x {frame.shape[0]}. Aspect ratio: {video_aspect}")
        label_aspect = self.video_label.winfo_width() / self.video_label.winfo_height()
        print(
            f"Label: {self.video_label.winfo_width()} x {self.video_label.winfo_height()}. Aspect ratio: {label_aspect}")

        # Scale width or height based on calculated formats
        if label_aspect > video_aspect:
            new_height = self.video_label.winfo_height()
            new_width = int(video_aspect * new_height)
        else:
            new_width = self.video_label.winfo_width()
            new_height = int(new_width / video_aspect)

        return new_width, new_height

    def delayed_aspect_ratio(self):
        """
        This is needed because GUI needs some time to built up
        """
        self.recalculated_width, self.recalculated_height = self.aspect_ratio()

    def update_camera(self):
        frame = self.camera.get_frame()

        if frame is not None:
            # frame = cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 0)

            if self.chord_classifier_button.cget("text") == "Recording Tool":
                # Chord detection:
                image = resize_image(frame)
                x = np.expand_dims(image, axis=0)
                x = preprocess_input(x)
                prediction = model.predict(x)[0]
                class_index = np.argmax(prediction)
                if prediction[class_index] > 0.9:
                    if class_index == 10:
                        self.predicted_chord = 'None'
                        print(f"Chord: {self.predicted_chord}")
                    for chord, i in CLASSES_MAP.items():
                        if i == class_index:
                            if chord != self.predicted_chord or self.predicted_chord == '':
                                self.predicted_chord = chord
                                print(f"Chord: {self.predicted_chord}")
                                self.canvas.itemconfig(self.chord_text, text=chord)

                # Hand detection:
                # frame.flags.writeable = False
                # results = hands.process(frame)
                #
                # # Draw the hand annotations on the image
                # frame.flags.writeable = True
                # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                # if results.multi_hand_landmarks:
                #     for hand_landmarks in results.multi_hand_landmarks:
                #         mp_drawing.draw_landmarks(
                #             frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            img = Image.fromarray(frame)
            img = img.resize((self.recalculated_width, self.recalculated_height), Image.LANCZOS)
            img = ImageOps.pad(img, (
                self.video_label.winfo_width(),
                self.video_label.winfo_height()
            ), color='black')
            img = ImageTk.PhotoImage(img)
            self.video_label.configure(image=img)
            self.video_label.image = img
            self.after(50, self.update_camera)

    def on_closing(self):
        self.camera.release()
        self.destroy()

    def toggle_view(self):
        if self.chord_classifier_button.cget("text") == "Chord Classifier":
            # Hide elements
            self.right_frame.pack_forget()
            self.landmark_image.pack_forget()

            # Disable buttons
            self.record_button["state"] = "disable"
            self.create_button["state"] = "disable"

            # Resize camera preview
            self.left_frame.pack_propagate(True)
            self.video_label.config(width=self.video_label.winfo_width() * 2,
                                    height=self.video_label.winfo_height() * 2)

            self.chord_classifier_button.config(text="Recording Tool")

            # Create chord prediction display
            # self.canvas.pack(anchor='ne')
            self.canvas.place(in_=self.video_label, relx=1.0, rely=0.0, anchor='ne')
            self.canvas.create_rectangle(0, 0, 50, 50, fill='black')
            self.chord_text = self.canvas.create_text(25, 25, text='-', fill='white', font=('Helvetica', 16))

        else:
            # Show elements
            self.right_frame.pack(side="left", fill="both", expand=True)
            self.landmark_image.pack(pady=10, anchor="s")

            # Enable buttons
            self.record_button["state"] = "normal"
            self.create_button["state"] = "normal"

            self.left_frame.pack_propagate(False)
            self.video_label.config(width=348, height=194)

            self.chord_classifier_button.config(text="Chord Classifier")

            # Repack left frame
            self.left_frame.config(width=400, height=300)
            self.left_frame.pack(side="left", fill="both", expand=True)

            # Destroy chord display
            self.canvas.pack_forget()
