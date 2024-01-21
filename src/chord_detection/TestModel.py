"""
Author: Manuel Keck
This file is for testing the trained model.
"""
import os.path

import numpy as np
import tensorflow.keras.models

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from Settings import IMAGE_DIR


# Load model
model: tensorflow.keras.models.Model

image_path = os.path.join(IMAGE_DIR, 'validation/A/A-1.jpg')


