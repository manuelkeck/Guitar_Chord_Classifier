"""
Author: Manuel Keck
"""
import numpy as np
import cv2

from src.train_model.TrainModelHelpers import resize_image


class Sample(object):
    """
    This object class contains two numpy arrays and maps image with label
    """
    def __init__(self, image_path: str, label: np.array):
        self.image = resize_image(cv2.imread(image_path))
        self.hm = []
        self.label = label

