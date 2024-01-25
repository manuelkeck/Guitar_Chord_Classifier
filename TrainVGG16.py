"""
Author: Manuel Keck
"""
import os.path
import cv2

from src.train_model.Dataset import Dataset
from src.train_model.ChordDetectionVGG16 import ChordDetectionVGG16
from Settings import IMAGE_DIR
from src.train_model.LoadData import train_dataset, test_dataset


def main():
    # image_path = os.path.join(IMAGE_DIR, "training")
    # data = Dataset(image_path, image_path)

    # batch = train_dataset.__getitem__(0)

    chord_detector = ChordDetectionVGG16()
    chord_detector.train(train_dataset, test_dataset)

    pass


if __name__ == '__main__':
    main()
