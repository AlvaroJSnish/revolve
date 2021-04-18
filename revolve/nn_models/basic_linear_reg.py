# import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


def create_model(dataset_features):
    model = keras.Sequential([
        layers.Dense(32, activation='relu', input_shape=[
                     len(dataset_features.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(128, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)
    model.compile(loss="mse", optimizer=optimizer,
                  metrics=['mse'])

    return model


def fit_model(model, dataset_features, dataset_labels, path):
    model.fit(dataset_features, dataset_labels,
              epochs=400, validation_split=0.2)
    model.save(path + '/model')


def build_model(dataset_features, dataset_labels, path):
    dataframe = pd.DataFrame(data=dataset_features, index=None)

    model = create_model(dataframe)
    fit_model(model, dataframe, dataset_labels, path)
