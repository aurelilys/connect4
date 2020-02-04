from numpy import argmax, place, array
from tensorflow import keras
from tensorflow_core.python.keras import Model

from connect4 import Game


class Agent:

    def __init__(self, model: Model):
        self._model = model

    def predict(self, game: Game):
        board = []
        for i in range(game.board_height):
            internal = []

            for j in range(game.board_width):
                value = game._grid[j][i]

                if value is None:
                    internal.append([0, 0])
                else:
                    if value == 0:
                        internal.append([1, 0])
                    else:
                        internal.append([0, 1])

            board.append(internal)

        value = self._model.predict([board])

        print(value)

        ae = []

        for i in range(game.board_width):
            if game.can_put(i):
                print(i)
                ae.append(1)
            else:
                ae.append(0)

        valid_moves = array(ae)

        place(valid_moves, valid_moves == 0., [-999])
        place(valid_moves, valid_moves == 1., 0.)

        print(valid_moves)

        return argmax(value + valid_moves)


model = keras.Sequential()
model.add(keras.layers.SeparableConv2D(32, 4, activation='relu', input_shape=(6, 7, 2)))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(96))
model.add(keras.layers.Dense(7))
model.compile(optimizer="adam", loss="mean_squared_error")
model.summary()