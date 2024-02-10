import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model

# Laden des .keras-Modells
model_path = 'output/vgg/model/vgg16_model_v4.keras'
loaded_model = load_model(model_path)
loaded_model.summary()

