import sys

from numpy.ma import array

from connect4.game import Game, State, MoveResult
from connect4.player import UltimatePlayer
from connect4.player.ai import Agent, create_model


def main(argv):
    model = create_model()

    training(model, 30000)


def training(model, iteration=1000):
    features = []
    targets = []

    for i in range(iteration):
        print("Starting Game #" + str(i))
        game = Game([UltimatePlayer(0, '#f6b93b', Agent(0, model)), UltimatePlayer(1, '#e74c3c', Agent(1, model))], 7,
                    6, 4)
        game.state = State.PLAYING

        while game.state == State.PLAYING:
            game.current.next_move(game)

        for player in game._players:
            if player.last_action().result == MoveResult.VICTORY:
                win = player.last_action()
                win_action = player.actions
                win_action.remove(win)
            else:
                lose = player.last_action()

        features.append(win.board)
        features.append(lose.board)

        win_target = [0, 0, 0, 0, 0, 0, 0]
        win_target[win.played] = 1

        targets.append(win_target)

        for action in win_action:
            features.append(action.board)

            if action.prediction is not None:
                target = action.prediction[0]
            else:
                target = [0, 0, 0, 0, 0, 0, 0]

            target[action.played] = 0.8
            targets.append(target)

        if lose.prediction is not None:
            lose_target = lose.prediction[0]
        else:
            lose_target = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

        if lose.played == win.played:
            lose_target[lose.played] = 0
        else:
            lose_target[win.played] = 1

        targets.append(lose_target)

    model.fit(array(features), array(targets), batch_size=1000, epochs=10)

    model.save("weights.h5")


if __name__ == "__main__":
    main(sys.argv[1:])
