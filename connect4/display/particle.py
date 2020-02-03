from enum import Enum
from random import randint
from tkinter import Canvas


class Particle:

    def __init__(self, direction, canvas: Canvas, color):
        self.limit = randint(20, 300)
        self.direction = direction
        self.fall = False

        self.x = 600 if direction == Side.RIGHT else 0
        self.y = 450

        self.value = canvas.create_oval(0, 0, 0, 0, fill=color, width=0)

    def update(self, canvas: Canvas):
        if not self.fall and self.y < self.limit:
            self.fall = True
            self.direction = Side.random()

            return True

        if self.fall:
            if self.direction == Side.LEFT:
                self.x = randint(-1, 0) + self.x
            else:
                self.x = randint(0, 1) + self.x
            self.y = 1 + self.y

            canvas.coords(self.value, self.x, self.y, self.x + 6, self.y + 6)

            if self.y > 450 or self.y < 0 or self.x < 0 or self.x > 600:
                return False
            return True

        if self.direction == Side.LEFT:
            self.x = randint(1, 10) + self.x
        else:
            self.x = randint(-10, -1) + self.x
        self.y = randint(-10, -1) + self.y

        canvas.coords(self.value, self.x, self.y, self.x + 6, self.y + 6)
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
