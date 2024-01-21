"""
Author: Manuel Keck
Functions to create datasets for VGG16
"""
import keras.utils
import os
import tensorflow as tf
from tensorflow import keras
import keras as keras

from Settings import IMAGE_DIR
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def get_data_generator():
    # datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    pass


def get_datasets():
    train_data_dir = os.path.join(IMAGE_DIR, 'training')
    validation_data_dir = os.path.join(IMAGE_DIR, 'validation')
    test_data_dir = os.path.join(IMAGE_DIR, 'test')

    train_generator = datagen
