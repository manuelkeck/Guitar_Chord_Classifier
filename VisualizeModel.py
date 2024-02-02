import tensorflow as tf
from src.train_model.ChordDetectionVGG16 import ChordDetectionVGG16

# Create an instance of your model class
your_model = ChordDetectionVGG16()

# Visualize the architecture and save the image
tf.keras.utils.plot_model(
    your_model.model,
    to_file='your_model_architecture.png',
    show_shapes=False,
    show_dtype=False,
    show_layer_names=True,
    rankdir='TB',
    expand_nested=False,
    dpi=96,
    layer_range=None,
    show_layer_activations=False,
    show_trainable=False
)
