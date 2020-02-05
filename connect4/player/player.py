from connect4 import Game
from connect4.display import Display
from connect4.player.ai import Agent


class Player:

    def __init__(self, id: int, color):
        self.id = id
        self.color = color
        self.actions = []

    def movement(self, board, played, result):
        self.actions.append(Action(board, played, result))

    def next_move(self, game: Game, display=None):
        pass

    def last_action(self):
        return self.actions[len(self.actions) - 1]


class HumanPlayer(Player):
    pass


class UltimatePlayer(Player):

    def __init__(self, id: int, color, agent: Agent):
        super().__init__(id, color)

        self._agent = agent

    def next_move(self, game, display=None):
        (x, board, prediction) = self._agent.predict(game, False if display is Display else True)
        (y, result, victory) = game.put(x)

        self.actions.append(Action(board, x, result, prediction))

        if display is not None:
            display._draw_token(x, game.board_height - y - 1, self.color)

        return result, victory


class Action:

    def __init__(self, board, played, result, prediction=None):
        self.board = board
        self.played = played
        self.result = result
        self.prediction = prediction
