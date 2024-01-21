"""
Author: Manuel Keck
"""
import os.path

from tensorflow import keras as keras
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy
from src.train_model.CustomCallback import CustomCallback
from Settings import ROOT_DIR
from src.train_model.TFBaseModel import TFBaseModel


class ChordDetectionVGG16(TFBaseModel):
    def __init__(self):
        super().__init__("ChordDetectionVGG16")

    @staticmethod
    def get_vgg16_topless() -> keras.models.Model:
        model = VGG16(
            include_top=False,
            weights='imagenet',
            input_shape=(224, 224, 3),
            pooling=None,
            classes=1000,
            classifier_activation='softmax'
        )
        return model

    def define_model(self):
        model = keras.models.Sequential()
        vgg_model = self.get_vgg16_topless()
        model.add(vgg_model)

        # Add stages to VGG16
        # concatenate-layer
        # (32, 224, 224, landmarks+3)
        model.add(Flatten())
        model.add(Dense(units=1024, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(units=128, activation='relu'))
        model.add(Dense(units=16, activation='relu'))
        model.add(Dense(units=11, activation='softmax'))

        self.model = model

    def train(
            self,
            train_data: keras.utils.Sequence,
            val_data: keras.utils.Sequence,
            batch_size: int = 32,
            max_epochs: int = 100
    ):
        self.model.compile(
            optimizer=Adam(learning_rate=1e-3),
            loss=BinaryCrossentropy(),
            metrics=['acc']
        )

        log_path = os.path.join(ROOT_DIR, 'output/vgg/logs')
        model_path = os.path.join(ROOT_DIR, 'output/vgg/bestModel')

        callbacks = [
            keras.callbacks.TensorBoard(
                log_dir=log_path),
            keras.callbacks.ModelCheckpoint(
                filepath=model_path,
                save_best_only=True
            ),
            CustomCallback(
                epochMap={0: 18, 10: 14, 20: 10, 30: 6, 40: 3, 50: 0}
            )
        ]

        self.model.fit(
            x=train_data,
            validation_data=val_data,
            callbacks=callbacks,
            epochs=max_epochs
        )
