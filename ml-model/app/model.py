from pathlib import Path

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

MODEL_PATH = Path(__file__).resolve().parent / 'mnist_cnn.keras'


def build_model() -> keras.Model:
    model = keras.Sequential([
        layers.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax'),
    ])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def train_and_save() -> keras.Model:
    (x_train, y_train), _ = keras.datasets.mnist.load_data()
    x_train = x_train.astype('float32') / 255.0
    x_train = np.expand_dims(x_train, -1)
    model = build_model()
    model.fit(x_train, y_train, batch_size=128, epochs=2, validation_split=0.1, verbose=2)
    model.save(MODEL_PATH)
    return model


def load_or_train_model() -> keras.Model:
    if MODEL_PATH.exists():
        return keras.models.load_model(MODEL_PATH)
    return train_and_save()
