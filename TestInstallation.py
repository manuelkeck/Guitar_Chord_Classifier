import tensorflow as tf

print(tf.__version__)
print(tf.config.list_physical_devices('CPU'))
print(tf.config.list_physical_devices('GPU'))
