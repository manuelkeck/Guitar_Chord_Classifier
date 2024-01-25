"""
Author: Manuel Keck
"""
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Init mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


def detect_hand(image: np.ndarray):
    results = hands.process(image)

    if results.multi_hand_landmarks is not None:
        # multi_hand_landmarks = list with coordinates
        # [landmark {
        #     x: 0.43212813
        #     y: 0.5860103
        #     z: -1.256982e-06
        # }
        #  landmark {
        #      x: 0.4734379
        #      y: 0.51644135
        #      z: -0.07483422
        #  }
        # ...
        # ]

        image = draw_landmarks(image, results.multi_hand_landmarks)
        plt.imshow(image)
        plt.show()

        pass


def draw_landmarks(image: np.ndarray, results: list) -> np.ndarray:
    for hand_landmarks in results:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return image
