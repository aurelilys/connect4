from ann_visualizer.visualize import ann_viz
from tensorflow import keras
from tensorflow_core.python.keras import Model

model = keras.Sequential()
model.add(keras.layers.Dense(7))

ann_viz(model, title="My first neural network")
Agent(model)


class Agent:

    def __init__(self, model: Model):
        self._model = model

    def train(self, epoch=10000):
        model = self._model

        for epoch in range(epoch):
            print(model)

    def predict(self, valid_moves):
        print(valid_moves)
