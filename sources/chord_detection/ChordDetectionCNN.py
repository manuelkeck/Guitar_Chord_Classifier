"""
This code is based on https://github.com/ayushkumarshah/Guitar-Chords-recognition
with some modifications to get it worked and PEP8 conform.
"""

import librosa
import numpy as np

from keras.models import Sequential
from keras.models import model_from_json
from sources.chord_detection.settings import CLASSES_MAP, CLASSES, MODEL_DIR
from sources.chord_detection.metrics import *


class CNN(object):
    def __init__(self, most_shape):
        print("Initializing CNN")

        self.model = Sequential()
        self.input_shape = most_shape + (1,)

        print(f"Input shape = {self.input_shape}")

    def load_model(self):
        print('Loading saved model')

        # Load json and h5 and create model with weights
        try:
            with open("models/chord_audio_detector/model.json", "r") as json_file:
                loaded_model_json = json_file.read()
            loaded_model = model_from_json(loaded_model_json)
            loaded_model.load_weights("models/chord_audio_detector/model.h5")
            loaded_model.compile(
                optimizer="Adam",
                loss="categorical_crossentropy",
                metrics=['accuracy', precision, recall, fmeasure])
            self.model = loaded_model
            print('Model loaded successfully from ' + MODEL_DIR)
        except FileNotFoundError:
            print("Model file not found")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def predict(self, filepath, load_model=True):
        chord = ""
        if load_model:
            self.load_model()
            pass
        else:
            try:
                y, sr = librosa.load(filepath, duration=2)
                ps = librosa.feature.melspectrogram(y=y, sr=sr, )
                shape = (1,) + self.input_shape
                ps = np.array(ps.reshape(shape))
                predictions_tmp = self.model.predict(ps)
                predictions = predictions_tmp.argmax(axis=-1)
                class_id = predictions[0]
                chord = str(CLASSES[class_id])
            except FileNotFoundError:
                print("File not found.")
                chord = "N/A"
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                chord = "N/A"

        return chord

    @staticmethod
    def get_class(class_id):
        return list(CLASSES_MAP.keys())[list(CLASSES_MAP.values()).index(class_id)]
