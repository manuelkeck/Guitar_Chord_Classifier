from tensorflow.keras.callbacks import Callback
from typing import Dict


class CustomCallback(Callback):

    def __init__(self, epochMap: Dict):
        self.epochMap = epochMap

    def on_train_begin(self, logs=None):
        pass

    def on_train_end(self, logs=None):
        pass

    def UnfreezeAll(self):
        for i in range(1, len(self.model.layers[0].layers)):
            self.model.layers[0].layers[i].trainable = True

    def on_epoch_begin(self, epoch, logs=None):
        if epoch in self.epochMap.keys():
            self.UnfreezeAll()
            freezeUpToLayer = self.epochMap[epoch]

            for i in range(1, freezeUpToLayer):
                self.model.layers[0].layers[i].trainable = False


    def on_epoch_end(self, epoch, logs=None):
        pass

    def on_test_begin(self, logs=None):
        pass

    def on_test_end(self, logs=None):
        pass

    def on_predict_begin(self, logs=None):
        pass

    def on_predict_end(self, logs=None):
        pass

    def on_train_batch_begin(self, batch, logs=None):
        pass

    def on_train_batch_end(self, batch, logs=None):
        pass

    def on_test_batch_begin(self, batch, logs=None):
        pass

    def on_test_batch_end(self, batch, logs=None):
        pass

    def on_predict_batch_begin(self, batch, logs=None):
        pass
    def on_predict_batch_end(self, batch, logs=None):
        pass