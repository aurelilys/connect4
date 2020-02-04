from connect4 import Game, HumanPlayer
from connect4.display import Display


def main():
    Display(Game([HumanPlayer(0, '#f6b93b'), HumanPlayer(1, '#e74c3c')], 7, 6, 4))


if __name__ == "__main__":
    main()
