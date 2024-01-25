"""
Author: Manuel Keck
"""
import os.path
import cv2
import numpy as np

from src.train_model.Dataset import Dataset
from src.train_model.ChordDetectionVGG16hands import ChordDetectionVGG16hands
from Settings import IMAGE_DIR
from src.train_model.LoadData import train_dataset, test_dataset
from src.train_model.HandDetection import detect_hand
from src.train_model.TrainModelHelpers import resize_image
from PIL import Image


def main():
    image_path = os.path.join(IMAGE_DIR, "training/A/A-293.jpg")
    # image_path = os.path.join(IMAGE_DIR, "training/None/None-1.jpg")
    image = resize_image(np.asarray(Image.open(image_path)))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    detect_hand(image)

    # chord_detector = ChordDetectionVGG16hands()
    # chord_detector.train(train_dataset, test_dataset)

    pass


if __name__ == '__main__':
    main()
