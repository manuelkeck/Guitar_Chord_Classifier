"""
Author: Manuel Keck
"""
import mediapipe as mp
import numpy as np
import cv2

from typing import Tuple

# Init mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


def detect_hand(image: np.ndarray) -> Tuple[list, int]:
    results = hands.process(image)
    check_var = 0

    if results.multi_hand_landmarks is not None:
        # Get and draw landmarks
        # image = draw_landmarks(image, results.multi_hand_landmarks)
        # cv2.imshow("Original image", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # Create heatmap with identified landmarks
        # return create_heatmap(results.multi_hand_landmarks), check_var
        return [], check_var

    else:
        # max_amount_landmarks = 21
        # iterator = 0
        # empty_heatmaps_list = []
        #
        # while iterator < max_amount_landmarks:
        #     empty_heatmaps_list.append(np.zeros((224, 224)))
        #     iterator += 1
        #
        check_var = 1
        # return empty_heatmaps_list, check_var
        return [], check_var


def draw_landmarks(image: np.ndarray, results: list) -> np.ndarray:
    for hand_landmarks in results:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return image


def create_heatmap(results: list) -> list:
    heatmap_list = []

    if results:
        counter = 0
        for hand_landmarks in results:
            for ids, lm in enumerate(hand_landmarks.landmark):
                heatmap_array = np.zeros((224, 224))
                counter += 1
                x_norm = int(lm.x * 224)
                y_norm = int(lm.y * 224)
                heatmap_array[y_norm][x_norm] = 1.0

                # Create heatmap with gaussian blur
                blurred_array = cv2.GaussianBlur(heatmap_array, (0, 0), sigmaX=5, sigmaY=5)
                normalized_blurred_array = blurred_array / np.max(blurred_array)
                heatmap_colored = cv2.applyColorMap((normalized_blurred_array * 255).astype(np.uint8), cv2.COLORMAP_JET)
                # cv2.imshow("Heatmap", heatmap_colored)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                heatmap_list.append(normalized_blurred_array)

        # Mediapipe hands provides up to 21 landmarks. If a lower amount was
        # found, the list should be filled up with empty arrays to reach the
        # correct dimension in CNN architecture concatenate layer/input layer
        if counter < 21:
            while counter < 21:
                heatmap_array = np.zeros((224, 224))
                heatmap_list.append(heatmap_array)
                counter += 1

    # Heatmap_list contains a list of 2D-arrays
    # Each 2D-array represents one landmark
    return heatmap_list
