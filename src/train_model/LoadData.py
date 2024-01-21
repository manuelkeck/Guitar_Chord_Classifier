"""
Author: Manuel Keck
"""
import os.path

from Settings import IMAGE_DIR
from src.train_model.Dataset import Dataset

train_images_path = os.path.join(IMAGE_DIR, "training/")

train_dataset = Dataset(train_images_path)

test_images_path = os.path.join(IMAGE_DIR, "testing/")

test_dataset = Dataset(test_images_path)
