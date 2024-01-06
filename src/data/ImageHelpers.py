"""
Author: Manuel Keck
Functions to process captured images in fast-lane implementation
"""
import cv2
import numpy as np
import os
import json

from Settings import X_TARGET, Y_TARGET, OUT_DIR, IMAGE_DIR


def capture_image(image: np.ndarray, image_path: str):
    """
    This function implements a light-weighted option to capture images with the hand
    on fingerboard. There is no hand detection etc. implemented.
    """
    hand_image = cv2.resize(image, (X_TARGET, Y_TARGET), interpolation=cv2.INTER_AREA)
    cv2.imwrite(image_path, hand_image)


def get_folder(chord: str):
    return os.path.join(IMAGE_DIR + f"{chord}/")


def get_index(path: str):
    try:
        file = os.path.join(path + "info.json")
        print(f"File: {file}")
        with open(file, "r") as json_file:
            info_json = json.load(json_file)

        return info_json["index"]
    except FileNotFoundError:
        print("An error occurred in 'get_index'.")
        return


def update_index(path: str, index=0):
    try:
        file = os.path.join(path + "info.json")
        with open(file, "r") as json_file:
            info_json = json.load(json_file)

        info_json["index"] = index

        with open(file, "w") as json_file:
            json.dump(info_json, json_file)
    except FileNotFoundError:
        print("An error occurred in 'update_index'.")
        return
    except FileExistsError:
        print("An error occurred in 'update_index'.")
        return

    print(f"Updated index to {get_index(path)}.")
