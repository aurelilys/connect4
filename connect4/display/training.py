from numpy.ma import array

from connect4 import Game, State, MoveResult
from connect4.display import Display
from connect4.player import UltimatePlayer
from connect4.player.ai import Agent


class TrainingDisplay(Display):

    def __init__(self, model):
        self._features = []
        self._targets = []
        self._model = model
        self._counter = 0

        super().__init__(Game([UltimatePlayer(0, '#f6b93b', Agent(0, model)), UltimatePlayer(1, '#e74c3c', Agent(1, model))], 7, 6, 4))

    def _on_ready(self):
        self._canvas.after(100, self._run)

    def _run(self):
        if self._game.state == State.PLAYING:
            (result, victory) = self._game.current.next_move(self._game, self)

            if result == MoveResult.VICTORY:
                for player in self._game._players:
                    if player.last_action().result == MoveResult.VICTORY:
                        win = player.last_action()
                        win_action = player.actions
                        win_action.remove(win)
                    else:
                        lose = player.last_action()

                self._features.append(win.board)
                self._features.append(lose.board)

                win_target = [0, 0, 0, 0, 0, 0, 0]
                win_target[win.played] = 1

                self._targets.append(win_target)

                for action in win_action:
                    self._features.append(action.board)

                    if action.prediction is not None:
                        target = action.prediction[0]
                    else:
                        target = [0, 0, 0, 0, 0, 0, 0]

                    target[action.played] = 0.8
                    self._targets.append(target)

                if lose.prediction is not None:
                    lose_target = lose.prediction[0]
                else:
                    lose_target = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

                if lose.played == win.played:
                    lose_target[lose.played] = 0
                else:
                    lose_target[win.played] = 1

                self._targets.append(lose_target)
        elif self._game.state == State.FINISHED:
            print("Ending Game #"+str(self._counter))

            self._reset(Game(self._game._players, 7, 6, 4))
            self._counter += 1

            if self._counter % 100 == 0:
                self._model.fit(array(self._features), array(self._targets), batch_size=1000, epochs=5)

                self._model.save("weights.h5")

                self._features = []
                self._targets = []

        self._window.after(2, self._run)

    def _move(self, event):
        pass

    def _click(self, event):
        pass
