# Copyright(c) by Thomas Gulde - 2020 All Rights Reserved
import tensorflow.keras as keras
import os
import numpy as np

from abc import ABC, abstractmethod
from Settings import MODEL_PATH
from typing import Optional


class TFBaseModel(ABC):
    def __init__(self, name: str):
        self.model: Optional[keras.Model] = None
        self.name = name
        self.modelPath = os.path.join(MODEL_PATH, name + ".h5")
        self.define_model()
        self.analyze_model()

    def analyze_model(self):
        self.model.summary()
        plot_model_path = os.path.join(MODEL_PATH, self.name + ".png")
        # problem with pydot - wtf?
        # plot_model(self.model, plot_model_path)

    def load_model(self, path: Optional[str] = None):
        if path is None:
            self.model = keras.models.load_model(self.modelPath)
        else:
            self.model = keras.models.load_model(path)

    def save_model(self, path: str):
        if path is None:
            self.model.save(self.modelPath)
        else:
            self.model.save(path)

    def predict(self, x: np.ndarray):
        return self.model.predict(x)

    @abstractmethod
    def define_model(self):
        raise Exception("Not Implemented!")

    @abstractmethod
    def train(
            self,
            train_dataset: keras.utils.Sequence,
            test_dataset: keras.utils.Sequence,
            max_epochs: int = 100
    ):
        raise Exception("Not Implemented!")

    # @abstractmethod
    # def PreprocessInput(self, x: np.ndarray) -> np.ndarray:
    #    return x
