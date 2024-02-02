"""
Author: Manuel Keck
This file is for testing the trained model.
"""
import os.path

import matplotlib.pyplot as plt
import numpy as np
import cv2

from PIL import Image
from tensorflow.keras.applications.vgg16 import preprocess_input
from Settings import IMAGE_DIR, ROOT_DIR
from src.train_model.ChordDetectionVGG16 import ChordDetectionVGG16
from src.train_model.TrainModelHelpers import resize_image
from Settings import CLASSES_MAP

# Load model
path = os.path.join(ROOT_DIR, "output/vgg/model/vgg16_model_v8.keras")
model = ChordDetectionVGG16()
model.load_model(path)
# model.summary()

# Load image (image is 16:9 and BGR)
image_path = os.path.join(IMAGE_DIR, 'validation/G/G-47.jpg')

# Resize image: result will be 224x224 with black borders (to keep 16:9 original format)
img = resize_image(np.asarray(Image.open(image_path)))
# plt.imshow(img)
# plt.show()
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Input: Return numpy array from resize_image -> converted from BGR to RGB (because
# preprocess-input from keras converts from RGB to BGR
# Camera input stream is already numpy array BGR stream -> convert to RGB
# x = image.img_to_array(img)
x = np.expand_dims(img, axis=0)
x = (x/255).astype(np.float32)

# https://www.tensorflow.org/api_docs/python/tf/keras/applications/vgg16/preprocess_input
x = preprocess_input(x)

prediction = model.predict(x)[0]

class_index = np.argmax(prediction)
if class_index == 10:
    print(f"Chord: None")

for chord, index in CLASSES_MAP.items():
    if index == class_index:
        print(f"Chord: {chord}")
