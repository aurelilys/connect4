from enum import Enum
from random import randint
from tkinter import Canvas


class Particle:

    def __init__(self, direction, canvas: Canvas, color):
        # Initialize particle
        self._limit = randint(20, 300)
        self._direction = direction
        self._fall = False

        # Initialize position
        self._x = 600 if direction == Side.RIGHT else 0
        self._y = 450

        # Draw particle
        self.value = canvas.create_oval(0, 0, 0, 0, fill=color, width=0)

    def update(self, canvas: Canvas):
        # Check if it has reached limit
        if not self._fall and self._y < self._limit:
            self._fall = True
            self._direction = Side.random()

            return True

        if self._fall:
            # Fall particle
            if self._direction == Side.LEFT:
                self._x += randint(-1, 0) * 0.2
            else:
                self._x += randint(0, 1) * 0.2
            self._y += 1
        else:
            if self._direction == Side.LEFT:
                self._x += randint(1, 10)
            else:
                self._x += randint(-10, -1)
            self._y += randint(-10, -1)

        # Change coordinate
        canvas.coords(self.value, self._x, self._y, self._x + 6, self._y + 6)

        # Check if it is off window
        if self._y > 450 or self._y < 0 or self._x < 0 or self._x > 600:
            return False
        return True


class Side(Enum):
    RIGHT = 1,
    LEFT = 2,

    @staticmethod
    def random():
        if randint(0, 1) == 0:
            return Side.LEFT
        else:
            return Side.RIGHT
