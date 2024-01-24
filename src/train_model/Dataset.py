"""
Author: Manuel Keck
https://www.tensorflow.org/api_docs/python/tf/keras/utils/Sequence
"""
import os
import numpy as np

from matplotlib import pyplot as plt
from tensorflow import keras as keras
from typing import Optional, Callable, List, Tuple
from Settings import CLASSES_MAP

from src.train_model.TrainModelHelpers import get_sub_folders
from src.train_model.Sample import Sample


class Dataset(keras.utils.Sequence):
    def __init__(self, image_path: str, batch_size: int = 64, shuffle=True, input_shape=(224, 224, 3),
                 augmentation: bool = False, preprocessing: Optional[Callable] = None):

        self.image_path = image_path  # ROOT_DIR/data/images/training/
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.input_shape = input_shape
        self.image_files = []

        self.data_samples: List[Sample] = []
        self.load_data()

        self.indexes = np.arange(len(self.data_samples))
        self.on_epoch_end()

    def load_data(self):
        print("Loading data...")

        # Loop through all dirs to append training image paths to image_files
        sub_folders = get_sub_folders(self.image_path)
        for sub_folder in sub_folders:
            tmp_dir = os.path.join(self.image_path, sub_folder)
            self.image_files = [os.path.join(tmp_dir, img) for img in os.listdir(tmp_dir) if img != 'info.json']

            # Loop through all image paths and add Sample object to data_sample list
            # Sample object contains:
            # image: np.array (resized, black boarders)
            # label: np.array (mapped with CLASSES_MAP from Settings.py
            for image in self.image_files:
                extracted_dir = os.path.dirname(image)
                chord_label = os.path.basename(extracted_dir)
                tmp_label = self.generate_label(chord_label)
                self.data_samples.append(Sample(image, tmp_label))
                pass

        print("Data loaded.")

        # Test output to check image from data_samples
        # img = self.data_samples[0].image
        # plt.imshow(img)
        # plt.show()

    pass

    def __len__(self):
        return int(np.floor(len(self.data_samples) / self.batch_size))

    # def __getitem__(self, index):
    #     """
    #     Create 'mini batches' from image data for training
    #     """
    #     batch_x = self.img_samples[index * self.batch_size:(index + 1) * self.batch_size]
    #     batch_y = self.labels[index * self.batch_size:(index + 1) * self.batch_size]
    #
    #     # x = images for mini batch
    #     # y = corresponding label
    #     x = np.zeros((len(batch_x), *self.input_shape))
    #     y = [None] * len(batch_x)
    #
    #     for i, image_path in enumerate(batch_x):
    #         image = cv2.imread(image_path)
    #         image = self.resize_image(image)    # redundant, refactoring needed
    #         x[i] = image / 255.0
    #         y[i] = self.generate_label(batch_y[i])  # redundant, refactoring needed
    #
    #     return x, np.array(y)

    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        input_images = []
        labels = []

        for index in indexes:
            # Todo: call method for augmentation and preprocessing if needed
            tmp_img = self.data_samples[index].image
            tmp_img = (tmp_img/255).astype(np.float32)
            input_images.append(tmp_img)
            labels.append(self.data_samples[index].label)

        return np.array(input_images), np.array(labels)

    @staticmethod
    def generate_label(label: str) -> np.array:
        labels = [0] * 11

        for chord, index in CLASSES_MAP.items():
            if chord == label:
                labels[index] = 1
                break

        if label == 'None':
            labels[10] = 1

        return np.array(labels)

    def generate_sample(self, index : int) -> Tuple[np.ndarray, np.ndarray]:
        # input_img, label =
        pass

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.data_samples))
        if self.shuffle:
            np.random.shuffle(self.indexes)

