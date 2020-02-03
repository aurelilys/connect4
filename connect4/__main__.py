from connect4 import Game, Player
from connect4.display import Display


def main():
    Display(Game([Player(0, '#f6b93b'), Player(1, '#e74c3c')], 7, 6, 4))


if __name__ == "__main__":
    main()
