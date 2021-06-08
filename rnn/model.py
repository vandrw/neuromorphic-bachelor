import numpy as np
import muspy
import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras


class DrumRNN:
    def __init__(self) -> None:
        self.model = None

    def idyom_loss(self):
        pass

    def create_model(self):
        model = keras.Sequential()

        model.add(
            layers.Bidirectional(layers.LSTM(512, return_sequences=True), input_shape=(5, 10))
        )
        model.add(layers.Bidirectional(layers.LSTM(128)))
        model.add(layers.Dense(10))

        self.model = model


    def generate(self):
        raise NotImplementedError

    def generate_music(self, path, filename) -> None:
        music = self.generate()

        muspy.write_audio(path + os.sep + filename, music, audio_format="wav")

        muspy.show_pianoroll(music)
        plt.show()
