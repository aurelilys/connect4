from math import floor
from random import randint
from tkinter import Canvas

from connect4 import Victory, State, Game
from connect4.display.particle import Particle, Side


class WinEffect:

    def __init__(self, game: Game, canvas: Canvas, victory: Victory):
        self._game = game
        self._canvas = canvas
        self._victory = victory
        self._particles = []
        self._color = ['#e74c3c', '#e67e22', '#8e44ad', '#1abc9c', '#2ecc71', '#f1c40f', '#f39c12']

        self._x = 0
        self._y = 0

        self._counter = 0
        self._shake = len(self._victory.positions) * 100

    def run(self):
        if self._game.state == State.DESTROYED:
            return

        if self._counter <= self._shake:
            if self._counter == self._shake:
                self._canvas.after(10, self.run)
            else:
                if self._counter % 100 == 0:
                    oval_x, oval_y = self._victory.positions[floor(self._counter / 100)]

                    self._canvas.create_oval(100 + ((oval_x + 0.2) * (400 / self._game.board_width)),
                                             400 - ((oval_y + 0.2) * (340 / self._game.board_height)),
                                             100 + ((oval_x + 0.8) * (400 / self._game.board_width)),
                                             400 - ((oval_y + 0.8) * (340 / self._game.board_height)),
                                             fill=self._victory.player.color, width=5, outline="#ecf0f1")

                self._x += randint(-self._x - 3, -self._x + 3)
                self._y += randint(-self._y - 3, -self._y + 3)

                self._canvas.place(x=self._x, y=self._y)
        else:
            if self._counter % 2 == 0:
                self._particles.append(Particle(Side.RIGHT, self._canvas, self._color[randint(0, 6)]))
                self._particles.append(Particle(Side.LEFT, self._canvas, self._color[randint(0, 6)]))

            for particle in self._particles:
                if not particle.update(self._canvas):
                    self._canvas.delete(particle.value)
                    self._particles.remove(particle)

        self._counter += 1
        self._canvas.after(10, self.run)
