from tkinter import Tk, PhotoImage, Canvas, Button, Scale, HORIZONTAL, Label, StringVar
from tkinter.colorchooser import askcolor
from tkinter.ttk import Entry

from connect4 import Game, Player
from connect4.display import Display


class PlayerSelector:

    def __init__(self, id, name, color, window):
        self.id = id
        self.color = color
        self.entry = StringVar(window, name)


class Configure:

    def __init__(self):
        self._window = Tk()

        self._players = [PlayerSelector(0, "Player 1", '#f6b93b', self._window),
                         PlayerSelector(1, "Player 2", '#e74c3c', self._window)]

        self._window.title("Connect4 Deluxe")
        self._window.resizable(width=False, height=False)
        self._window.geometry("300x350+{}+{}".format(int((self._window.winfo_screenwidth() / 2) - (300 / 2)),
                                                     int((self._window.winfo_screenheight() / 2) - (350 / 2))))

        self._window.iconphoto(False, PhotoImage(file="assets/logo.png"))

        self._canvas = Canvas(self._window, width=300, height=450, background='#ecf0f1')

        Label(self._window, text="Connect4", foreground='#2c3e50', font=("The Bold Font", 15)).place(x=160, y=30,
                                                                                                     anchor="e")
        Label(self._window, text="Deluxe", foreground='#6c5ce7', font=("The Bold Font", 15)).place(x=160, y=30,
                                                                                                   anchor="w")

        self._connect = Scale(self._window, from_=4, to=10, label="Connect", font=("The Bold Font", 7), length=200,
                              orient=HORIZONTAL)
        self._width = Scale(self._window, from_=7, to=15, label="Width", font=("The Bold Font", 7), length=200,
                            orient=HORIZONTAL)
        self._height = Scale(self._window, from_=6, to=15, label="Height", font=("The Bold Font", 7), length=200,
                             orient=HORIZONTAL)
        self._connect.place(x=150, y=80, anchor="center")
        self._width.place(x=150, y=140, anchor="center")
        self._height.place(x=150, y=200, anchor="center")

        Button(self._window, text="Play", foreground='#2c3e50', font=("The Bold Font", 10), command=self.launch).place(
            x=120, y=315, width=60, height=25)

        for player in self._players:
            self.create_button(player)

        self._window.mainloop()

    def create_button(self, player):
        Entry(self._window, textvariable=player.entry, font=("The Bold Font", 10), width=10).place(x=50,
                                                                                                   y=250 + player.id * (
                                                                                                           20 + 10))
        player.button = Button(self._window, width=5, background=player.color, borderwidth=0,
                               command=lambda: self.on_change_color(player))
        player.button.place(x=180, y=250 + (player.id * (20 + 10)))

    def on_change_color(self, player):
        _, color = askcolor(parent=self._window, initialcolor=player.color)
        player.button.configure(background=color)
        player.color = color

    def launch(self):
        connect = self._connect.get()
        width = self._width.get()
        height = self._height.get()

        self._window.destroy()

        players = []
        for player in self._players:
            players.append(Player(player.id, player.entry.get(), player.color))

        Display(Game(players, width, height, connect))
