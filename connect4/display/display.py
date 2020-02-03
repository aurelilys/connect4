from math import floor
from tkinter import Canvas, Tk, PhotoImage

from connect4 import Game, MoveResult, State
from connect4.display.win import WinEffect


class Display:

    def __init__(self, game: Game):
        self.game = game
        self.cursor = None

        window = Tk()

        window.title("Connect4")

        window.resizable(width=False, height=False)
        window.geometry("600x450+{}+{}".format(int((window.winfo_screenwidth() / 2) - (600 / 2)),
                                               int((window.winfo_screenheight() / 2) - (450 / 2))))
        window.iconphoto(False, PhotoImage(file="../assets/logo.png"))

        self.window = window
        self.canvas = Canvas(self.window, width=600, height=450, background='#ecf0f1')
        self.canvas.place(x=0, y=0)
        self.canvas.create_polygon(90, 50, 510, 50, 510, 420, 525, 420, 525, 430, 485, 430, 485, 420, 500, 420, 500,
                                   410, 100, 410, 100, 420, 115, 420, 115, 430, 75, 430, 75, 420, 90, 420, width=3,
                                   fill='#1e3799', outline="black")

        for x in range(self.game.board_width):
            for y in range(self.game.board_height):
                self.canvas.create_oval(100 + ((x + 0.2) * (400 / self.game.board_width)),
                                        60 + ((y + 0.2) * (340 / self.game.board_height)),
                                        100 + ((x + 0.8) * (400 / self.game.board_width)),
                                        60 + ((y + 0.8) * (340 / self.game.board_height)), fill='#ecf0f1', width=3,
                                        outline="black")

        self.canvas.bind("<Motion>", self.move)
        self.canvas.bind("<ButtonPress-1>", self.click)
        self.window.protocol("WM_DELETE_WINDOW", lambda: self._destroy())

        self.window.mainloop()

    def _destroy(self):
        self.game.state = State.DESTROYED
        self.window.destroy()

    def move(self, event):
        if self.game.state != State.PLAYING:
            return
        if event.x <= 100 or event.x >= 500:
            return

        if self.cursor is not None:
            event.widget.delete(self.cursor)

        x = floor((event.x - 100) / (400 / self.game.board_width))
        minimum = 100 + ((x + 0.2) * (400 / self.game.board_width))
        maximum = 100 + ((x + 0.8) * (400 / self.game.board_width))

        self.cursor = event.widget.create_oval(minimum, 40 - (maximum - minimum),
                                               maximum, 40,
                                               fill=self.game.current.color)

    def click(self, event):
        if self.game.state != State.PLAYING:
            return
        if event.x < 100 or event.x > 500:
            return

        x = floor((event.x - 100) / (400 / self.game.board_width))
        if not self.game.can_put(x):
            return

        color = self.game.current.color
        (y, result, victory) = self.game.put(x)

        event.widget.create_oval(100 + ((x + 0.2) * (400 / self.game.board_width)),
                                 400 - ((y + 0.2) * (340 / self.game.board_height)),
                                 100 + ((x + 0.8) * (400 / self.game.board_width)),
                                 400 - ((y + 0.8) * (340 / self.game.board_height)), fill=color, width=3,
                                 outline="black")

        if self.cursor is not None:
            self.canvas.delete(self.cursor)

        if result == MoveResult.VICTORY:
            self.window.after(0, WinEffect(self.game, self.canvas, victory).run)
            return

        minimum = 100 + ((x + 0.2) * (400 / self.game.board_width))
        maximum = 100 + ((x + 0.8) * (400 / self.game.board_width))
        self.cursor = event.widget.create_oval(minimum, 40 - (maximum - minimum),
                                               maximum, 40,
                                               fill=self.game.current.color)
