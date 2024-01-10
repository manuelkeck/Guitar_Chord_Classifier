"""
Author: Manuel Keck
Some parts of this class are from MediaPipe:
Copyright 2023 The MediaPipe Authors. All Rights Reserved.
MediaPipe is licenced under the Apache Licence, Version 2.0
"""
import mediapipe as mp
import numpy as np
import cv2

from Settings import Y_TARGET, X_TARGET
from PIL import Image, ImageTk


class ImageProcessing:
    """
    This class will prepare the captured image to be compatible with Google's
    mediapipe. With mediapipe the hand will be detected and used to crop the
    captured image.
    """

    def __init__(self, gui_app, controller):
        self.gui_app = gui_app
        self.controller = controller
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.1
        )
        self.rgb_image = None

    def get_hand_landmarks(self, image: np.ndarray, image_path: str):
        """
        Resize and store image, if landmarks could be found
        :param image: Image (frame) numpy array
        :param image_path: Where image will be saved
        """
        self.rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(self.rgb_image)

        if results.multi_hand_landmarks:
            print("Landmarks found.")
            self.controller.add_text("[Image] Landmarks found.")
            self.save_image(image_path)
            self.draw_landmarks(results)
            self.show_image()
            check_var = True
        else:
            print("No landmarks found. Image will not be saved")
            self.controller.add_text("[Image] No landmarks found!")
            self.controller.add_text("[Image] Image will not be saved.")
            check_var = False

        self.controller.add_text("[Image] Check captured image presented on left side.")

        return check_var

    def draw_landmarks(self, results):
        # Condition: only one hand visible in image
        hand_landmarks = results.multi_hand_landmarks[0]

        h, w, _ = self.rgb_image.shape

        for landmark in hand_landmarks.landmark:
            x, y = int(landmark.x * w), int(landmark.y * h)
            cv2.circle(self.rgb_image, (x, y), 5, (0, 255, 0), -1)

    def show_image(self):
        # Show captured image on GUI (with landmarks, if found)
        image = cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image)

        # Get UI widget size and calculate ratio
        widget_height = self.gui_app.landmark_image.winfo_height()
        widget_width = self.gui_app.landmark_image.winfo_width()
        widget_aspect_ratio = widget_width / widget_height
        image_aspect_ratio = image_pil.width / image_pil.height

        # Resize
        if widget_aspect_ratio > image_aspect_ratio:
            tmp_width = widget_height * image_aspect_ratio
            image_pil = image_pil.resize((int(tmp_width), widget_height), Image.LANCZOS)
        else:
            tmp_height = widget_width / image_aspect_ratio
            image_pil = image_pil.resize((widget_width, int(tmp_height)), Image.LANCZOS)

        # Show
        image_tk = ImageTk.PhotoImage(image=image_pil)
        self.gui_app.landmark_image.config(image=image_tk)
        self.gui_app.landmark_image.image = image_tk

    def save_image(self, image_path: str):
        image = b''

        # Check target size and resize if needed
        if self.rgb_image.shape[0] != Y_TARGET or self.rgb_image.shape[1] != X_TARGET:
            image = cv2.resize(self.rgb_image, (X_TARGET, Y_TARGET), interpolation=cv2.INTER_AREA)

        # Save image to local file system
        self.controller.add_text(f"[Image] Cropped image will be saved here: {image_path}")
        self.controller.latest_image_path = image_path
        cv2.imwrite(image_path, image)
        print(f"Image stored here: {image_path}")
