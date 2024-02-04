"""
Author: Manuel Keck
"""
import os.path

from tensorflow import keras as keras
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy, CategoricalCrossentropy
from src.train_model.CustomCallback import CustomCallback
from Settings import ROOT_DIR
from src.train_model.TFBaseModel import TFBaseModel
from src.train_model.VisualizeResults import plot_loss, plot_accuracy


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
            test_data: keras.utils.Sequence,
            batch_size: int = 4,
            max_epochs: int = 200
    ):
        self.model.compile(
            optimizer=Adam(learning_rate=1e-4),
            loss=BinaryCrossentropy(),
            metrics=['acc', 'categorical_accuracy']
        )

        log_path = os.path.join(ROOT_DIR, 'output/vgg/logs')
        model_path = os.path.join(ROOT_DIR, 'output/vgg/model')

        # Start tensorboard on localhost with
        # tensorboard --logdir=./output/vgg/logs

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

        history = self.model.fit(
            x=train_data,
            validation_data=test_data,
            callbacks=callbacks,
            epochs=max_epochs
        )

        # TFBaseModel class contains save function, refactor later
        self.model.save('output/vgg/model/vgg16_model_v9.keras')

        plot_accuracy(history)
        plot_loss(history)

