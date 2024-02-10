"""
Author: Manuel Keck
"""
import os.path

from tensorflow import keras as keras
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.layers import Flatten, Dense, Dropout, Input, Concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy
from src.train_model.CustomCallback import CustomCallback
from Settings import ROOT_DIR
from src.train_model.TFBaseModel import TFBaseModel
from src.train_model.VisualizeResults import plot_loss, plot_accuracy


class ChordDetectionVGG16hands(TFBaseModel):
    def __init__(self):
        super().__init__("ChordDetectionVGG16hands")

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
        # img -> vgg16
        # mask -> vgg16
        # concat
        # layers

        # image + mask = concat -> vgg16
        # layers

        model = keras.models.Sequential()
        vgg_model = self.get_vgg16_topless()

        input_rgb = Input(shape=(224, 224, 3), name='input_images')
        input_map = Input(shape=(224, 224, 21), name='input_heatmaps')

        # sample -> landmark heatmaps
        # __get_item__ -> heatmap creation
        # in get item ne liste an heatmap nummpy arrays und die dann später als numpy array umwandeln
        # erst beides zusammen sodass 224,224,24 entsteht und dann vlt flatten layer und dann vgg16
        #

        # model.add(vgg_model)

        concatenated_input1 = Concatenate(axis=-1)([vgg_model, input_rgb])
        concatenated_input2 = Concatenate(axis=-1)([vgg_model, input_map])
        concatenated_input_total = Concatenate(axis=-1)([concatenated_input1, concatenated_input2])

        model.add(Flatten()(concatenated_input_total))
        model.add(Dense(units=1024, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(units=128, activation='relu'))
        model.add(Dense(units=32, activation='relu'))
        model.add(Dense(units=11, activation='softmax'))

        self.model = model

    def train(
            self,
            train_data: keras.utils.Sequence,
            heatmaps: list,
            val_data: keras.utils.Sequence,
            batch_size: int = 64,
            max_epochs: int = 5
    ):
        self.model.compile(
            optimizer=Adam(learning_rate=1e-3),
            loss=BinaryCrossentropy(),
            metrics=['acc', 'categorical_accuracy']
        )

        log_path = os.path.join(ROOT_DIR, 'output/vgg/logs')
        model_path = os.path.join(ROOT_DIR, 'output/vgg/model')

        # Start tensorboard on localhost with command:
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
            x=[train_data, heatmaps],
            y=None,
            validation_data=val_data,
            callbacks=callbacks,
            epochs=max_epochs
        )

        # TFBaseModel class contains save function, refactor later
        self.model.save('output/vgg/model/vgg16_model_v4.h5')
        self.model.save('output/vgg/model/vgg16_model_v4.keras')

        plot_accuracy(history)
        plot_loss(history)
