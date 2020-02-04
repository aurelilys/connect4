from math import floor
from tkinter import Canvas, Tk, PhotoImage

from connect4 import Game, State, MoveResult
from connect4.display.win import WinEffect


class Display:

    def __init__(self, game: Game):
        self._game = game
        self._cursor = None

        self._window = Tk()

        self._window.title("Connect4")
        self._window.resizable(width=False, height=False)
        self._window.geometry("600x450+{}+{}".format(int((self._window.winfo_screenwidth() / 2) - (600 / 2)),
                                                     int((self._window.winfo_screenheight() / 2) - (450 / 2))))
        self._window.iconphoto(False, PhotoImage(file="assets/logo.png"))

        self._canvas = Canvas(self._window, width=600, height=450, background='#ecf0f1')
        self._canvas.place(x=0, y=0)
        self._canvas.create_polygon(90, 50, 510, 50, 510, 420, 525, 420, 525, 430, 485, 430, 485, 420, 500, 420, 500,
                                    410, 100, 410, 100, 420, 115, 420, 115, 430, 75, 430, 75, 420, 90, 420, width=3,
                                    fill='#1e3799', outline="black")

        for x in range(self._game.board_width):
            for y in range(self._game.board_height):
                self._draw_token(x, y, '#ecf0f1')

        self._canvas.bind("<Motion>", self._move)
        self._canvas.bind("<ButtonPress-1>", self._click)
        self._window.protocol("WM_DELETE_WINDOW", lambda: self._destroy())

        self._game.state = State.PLAYING
        self._window.mainloop()

    def _draw_token(self, x, y, color):
        self._canvas.create_oval(100 + ((x + 0.2) * (400 / self._game.board_width)),
                                 60 + ((y + 0.2) * (340 / self._game.board_height)),
                                 100 + ((x + 0.8) * (400 / self._game.board_width)),
                                 60 + ((y + 0.8) * (340 / self._game.board_height)), fill=color, width=3,
                                 outline="black")

    def _draw_cursor(self, x):
        minimum = 100 + ((x + 0.2) * (400 / self._game.board_width))
        maximum = 100 + ((x + 0.8) * (400 / self._game.board_width))

        self._cursor = self._canvas.create_oval(minimum, 40 - (maximum - minimum),
                                                maximum, 40, fill=self._game.current.color)

    def _destroy(self):
        self._game.state = State.DESTROYED
        self._window.destroy()

    def _move(self, event):
        if self._game.state != State.PLAYING:
            return
        if event.x <= 100 or event.x >= 500:
            return

        if self._cursor is not None:
            event.widget.delete(self._cursor)

        x = floor((event.x - 100) / (400 / self._game.board_width))
        self._draw_cursor(x)

    def _click(self, event):
        if self._game.state != State.PLAYING:
            return
        if event.x < 100 or event.x > 500:
            return

        x = floor((event.x - 100) / (400 / self._game.board_width))
        if not self._game.can_put(x):
            return

        color = self._game.current.color
        (y, result, victory) = self._game.put(x)

        self._draw_token(x, self._game.board_height - y - 1, color)

        if self._cursor is not None:
            self._canvas.delete(self._cursor)

        if result == MoveResult.VICTORY:
            self._window.after(0, WinEffect(self._game, self._canvas, victory).run)
            return

        if result == MoveResult.NONE:
            self._draw_cursor(x)

        self._game.current.next_move(self._game)
