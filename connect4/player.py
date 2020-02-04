from connect4.ai import Agent


class Player:

    def __init__(self, id: int, color):
        self.id = id
        self.color = color

    def next_move(self, game):
        pass


class HumanPlayer(Player):
    pass


class UltimatePlayer(Player):

    def __init__(self, id: int, color, agent: Agent):
        super().__init__(id, color)

        self._agent = agent

    def next_move(self, game):
        game.put(self._agent.predict(game))
        pass
