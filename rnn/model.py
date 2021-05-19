import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import datetime

# tensorboard --logdir logs/fit
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

# model = keras.Sequential()
# # Add an Embedding layer expecting input vocab of size 1000, and
# # output embedding dimension of size 64.
# model.add(layers.Embedding(input_dim=1000, output_dim=64))

# # Add a LSTM layer with 128 internal units.
# model.add(layers.LSTM(128))

# # Add a Dense layer with 10 units.
# model.add(layers.Dense(10))

# model.fit(x=x_train, 
#           y=y_train, 
#           epochs=5, 
#           validation_data=(x_test, y_test), 
#           callbacks=[tensorboard_callback])


# model.summary()
