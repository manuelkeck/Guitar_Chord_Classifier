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

    def crop_captured_image(self, image: np.ndarray, image_path: str):
        """
        Crop captured image based on hand
        :param image: Image (frame) numpy array
        :param image_path: Where image will be saved
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_image)

        if results.multi_hand_landmarks:
            print("Landmarks found.")
            self.controller.add_text("[Image]: Landmarks found.")

            # Condition: only one hand visible in image
            hand_landmarks = results.multi_hand_landmarks[0]

            # Bounding Box
            h, w, _ = image.shape
            min_x, min_y = w, h
            max_x = max_y = 0

            for landmark in hand_landmarks.landmark:
                x, y = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(rgb_image, (x, y), 5, (0, 255, 0), -1)  # Grün, Radius 5
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

            # Increase boarding box
            min_x = max(0, min_x - 160)
            max_x = min(w - 1, max_x + 160)
            min_y = max(0, min_y - 90)
            max_y = min(h - 1, max_y + 90)

            # Draw boarding box
            cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)

            # Crop image
            hand_image = rgb_image[min_y:max_y, min_x:max_x]

            # Check target size and resize if needed
            if hand_image.shape[0] != Y_TARGET or hand_image.shape[1] != X_TARGET:
                hand_image = cv2.resize(hand_image, (X_TARGET, Y_TARGET), interpolation=cv2.INTER_AREA)

            rgb_image = hand_image

            # Draw landmarks on image
            # for landmark in hand_landmarks.landmark:
            #     lx, ly = int((landmark.x * w) - min_x), int((landmark.y * h) - min_y)
            #     if 0 <= lx < X_TARGET and 0 <= ly < Y_TARGET:
            #         cv2.circle(hand_image, (lx, ly), 5, (0, 255, 0), -1)

            # Save image to local file system
            self.controller.add_text(f"[Image]: Cropped image will be saved here: {image_path}")
            cv2.imwrite(image_path, rgb_image)
            print(f"Image stored here: {image_path}")
        else:
            print("No landmarks found.")
            self.controller.add_text("[Image]: No landmarks found!")

        self.controller.add_text("[Image]: Check captured image presented on left side.")

        # Show captured image on GUI (with landmarks, if found)
        print(type(rgb_image))
        image_pil = Image.fromarray(rgb_image)
        image_pil = image_pil.resize((
            self.gui_app.landmark_image.winfo_width(),
            self.gui_app.landmark_image.winfo_height()
        ), Image.LANCZOS)
        image_tk = ImageTk.PhotoImage(image=image_pil)
        self.gui_app.landmark_image.config(image=image_tk)
        self.gui_app.landmark_image.image = image_tk
