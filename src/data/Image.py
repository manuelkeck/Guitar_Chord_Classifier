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

    def __init__(self, gui_app):
        self.gui_app = gui_app

    def crop_captured_image(self, image: np.ndarray, image_path: str):
        """
        Crop captured image based on hand
        :param image: Image (frame) numpy array
        :param image_path: Where image will be saved
        """
        # Test: Show captured image on GUI
        image_pil = Image.fromarray(image)
        image_pil = image_pil.resize((self.gui_app.landmark_image.winfo_width(), self.gui_app.landmark_image.winfo_height()), Image.LANCZOS)
        image_tk = ImageTk.PhotoImage(image=image_pil)
        self.gui_app.landmark_image.config(image=image_tk)
        self.gui_app.landmark_image.image = image_tk

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.1
        )
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_image)

        if results.multi_hand_landmarks:
            # Condition: only one hand visible in image
            hand_landmarks = results.multi_hand_landmarks[0]
            print("3")

            # Bounding Box
            h, w, _ = image.shape
            min_x, min_y = w, h
            max_x = max_y = 0

            for landmark in hand_landmarks.landmark:
                x, y = int(landmark.x * w), int(landmark.y * h)
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

            # Calculate center of hand
            center_x, center_y = (max_x + min_x) // 2, (max_y + min_y) // 2
            print("4")

            # Calculate center to crop image
            start_x = max(0, center_x - X_TARGET // 2)
            end_x = min(w, center_x + X_TARGET // 2)
            start_y = max(0, center_y - Y_TARGET // 2)
            end_y = min(h, center_y + Y_TARGET // 2)

            # Crop image
            hand_image = image[start_y:end_y, start_x:end_x]
            print("5")
            # Check target size
            if hand_image.shape[0] != Y_TARGET or hand_image.shape[1] != X_TARGET:
                hand_image = cv2.resize(hand_image, (X_TARGET, Y_TARGET), interpolation=cv2.INTER_AREA)

            # Save image to local file system
            cv2.imwrite(image_path, hand_image)
            print(f"Image stored here: {image_path}")
        else:
            print("No landmarks found")
