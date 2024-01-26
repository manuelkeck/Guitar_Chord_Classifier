"""
Author: Manuel Keck
This file is for testing the trained model.
"""
import os.path

import matplotlib.pyplot as plt
import numpy as np
import cv2
import tensorflow as tf

from tensorflow.keras.models import load_model
from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from Settings import IMAGE_DIR, ROOT_DIR
from src.train_model.ChordDetectionVGG16 import ChordDetectionVGG16
from src.train_model.TrainModelHelpers import resize_image
from src.train_model.LoadData import val_dataset


# Define model
# Todo: create model.json to load as architecture
# model_vgg16 = ChordDetectionVGG16()

# Load model
path = os.path.join(ROOT_DIR, "output/vgg/model/vgg16_model_v3.keras")
# model_vgg16.load_model(path)
model = ChordDetectionVGG16()
model.load_model(path)
# model.summary()

# Load image (image is 16:9 and BGR)
image_path = os.path.join(IMAGE_DIR, 'validation/D/D-205.jpg')

# Resize image: result will be 224x224 with black borders (to keep 16:9 original format)
img = resize_image(np.asarray(Image.open(image_path)))
plt.imshow(img)
plt.show()
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.imshow(img)
plt.show()
pass
# Input: numpy array, output: resized numpy array
# img = resize_image(img)

# Input: Return numpy array from resize_image -> converted from BGR to RGB (because
# preprocess-input from keras converts from RGB to BGR
# Camera input stream is already numpy array BGR stream -> convert to RGB
# x = image.img_to_array(img)
x = np.expand_dims(img, axis=0)
# x = (x/255).astype(np.float32)

# Preprocess input: The images are converted from RGB to
# BGR, then each color channel is zero-centered with respect
# to the ImageNet dataset, without scaling.
# https://www.tensorflow.org/api_docs/python/tf/keras/applications/vgg16/preprocess_input
x = preprocess_input(x)

prediction = model.predict(x)[0]

value = 0
for i in prediction:
    value += i
print(f"Summed up softmax probabilities: {value}")

# decode_predictions = decode_predictions(prediction, top=11)
class_index = np.argmax(prediction)
print(f"Class index: {class_index}")

pass

