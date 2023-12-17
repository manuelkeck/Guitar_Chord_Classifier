"""
This code is based on https://github.com/ayushkumarshah/Guitar-Chords-recognition
with some modifications to get it worked.
"""

import librosa
import numpy as np

from keras.layers import Activation, Dense, Dropout, Conv2D, \
    Flatten, MaxPooling2D
from keras.models import Sequential
from keras.models import model_from_json
from sources.chord_detection.settings import CLASSES_MAP, MODEL_JSON, MODEL_H5, CLASSES, \
    MODEL_DIR
from sources.chord_detection.metrics import *


class CNN(object):
    def __init__(self, most_shape):
        # logger.info("Initializing CNN")
        print("Initializing CNN")
        self.model = Sequential()
        self.input_shape = most_shape + (1,)
        # logger.info(f"Input shape = {self.input_shape}")
        print(f"Input shape = {self.input_shape}")
        self.model.add(Conv2D(24, (5, 5), strides=(1, 1), input_shape=self.input_shape))
        self.model.add(MaxPooling2D((4, 2), strides=(4, 2)))
        self.model.add(Activation('relu'))

        self.model.add(Conv2D(48, (5, 5), padding="valid"))
        self.model.add(MaxPooling2D((4, 2), strides=(4, 2)))
        self.model.add(Activation('relu'))

        self.model.add(Conv2D(48, (5, 5), padding="valid"))
        self.model.add(Activation('relu'))

        self.model.add(Flatten())
        self.model.add(Dropout(rate=0.5))

        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(rate=0.5))

        self.model.add(Dense(10))
        self.model.add(Activation('softmax'))
        # logger.info("CNN Initialized")
        print("CNN Initialized")

    def load_model(self):
        # logger.info('Loading saved model')
        print('Loading saved model')
        # load json and create model
        try:
            with open(MODEL_JSON, "r") as json_file:
                loaded_model_json = json_file.read()
            loaded_model = model_from_json(loaded_model_json)
            # load weights into new model
            loaded_model.load_weights(MODEL_H5)
            loaded_model.compile(
                optimizer="Adam",
                loss="categorical_crossentropy",
                metrics=['accuracy', precision, recall, fmeasure])
            self.model = loaded_model
            # logger.info('Model loaded from ' + MODEL_DIR)
            print('Model loaded from ' + MODEL_DIR)
        except:
            # logger.info("Model not found")
            print("Model not found")

    def predict(self, filepath, loadmodel=True):
        # logger.info('Prediction')
        print('Prediction')
        if loadmodel:
            # self.load_model()
            pass
        else:
            # try:
            y, sr = librosa.load(filepath, duration=2)
            ps = librosa.feature.melspectrogram(y=y, sr=sr, )
            px = ps
            px
            shape = (1,) + self.input_shape
            ps = np.array(ps.reshape(shape))
            # predictions = self.model.predict_classes(ps)
            predictions_tmp = self.model.predict(ps)
            predictions = predictions_tmp.argmax(axis=-1)
            class_id = predictions[0]
            chord = str(CLASSES[class_id])
            # logger.info("The recorded chord is " + chord)
            print("The recorded chord is " + chord)
        # except:
        # logger.info("File note found")
        # chord = "N/A"
        return chord

    @staticmethod
    def get_class(class_ID):
        return list(CLASSES_MAP.keys())[list(CLASSES_MAP.values()).index(class_ID)]
