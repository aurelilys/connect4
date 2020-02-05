from os import path
import random as random

import tensorflow.keras as keras

from numpy import place
from numpy.ma import array, argmax

from connect4 import Game


class Agent:

    def __init__(self, id, model):
        self.id = id
        self._model = model

    def predict(self, game: Game, training=True):
        board = []
        for i in range(game.board_height):
            internal = []

            for j in range(game.board_width):
                value = game._grid[j][i]

                if value is None:
                    internal.append([0, 0])
                else:
                    internal.append([1, 0]) if value == self.id else internal.append([0, 1])

            board.append(internal)

        if training:
            if random.random() > 0.95:
                valid_moves = []

                for i in range(game.board_width):
                    valid_moves.append(1) if game.can_put(i) else valid_moves.append(0)

                i = random.randint(0, 6)

                while valid_moves[i] == 0:
                    if i >= 6:
                        i = 0
                    else:
                        i = i + 1

                return i, board, None

        prediction = self._model.predict(array([board]))
        valid_moves = []

        for i in range(game.board_width):
            valid_moves.append(1) if game.can_put(i) else valid_moves.append(0)

        valid_moves = array(valid_moves)

        place(valid_moves, valid_moves == 0., [-999])
        place(valid_moves, valid_moves == 1., 0.)

        return argmax(prediction + valid_moves), board, prediction


def create_model():
    if path.exists("weights.h5"):
        model = keras.models.load_model("weights.h5")
    else:
        model = keras.models.Sequential()
        model.add(keras.layers.Conv2D(42, (4, 4), input_shape=(6, 7, 2), activation='tanh', padding="same"))
        model.add(keras.layers.MaxPooling2D(strides=(2, 2)))
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(1024, activation='relu'))
        model.add(keras.layers.Dense(512, activation='relu'))
        model.add(keras.layers.Dense(256, activation='relu'))
        model.add(keras.layers.Dense(7, activation='softmax'))
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

    model.summary()
    return model
