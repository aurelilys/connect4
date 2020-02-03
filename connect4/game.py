from enum import Enum


class Game:

    def __init__(self, players, board_width, board_height, connect):
        self.players = players
        self.board_width = board_width
        self.board_height = board_height
        self._connect = connect

        self._grid = [[None for i in range(0, board_height)] for j in range(0, board_width)]

        self.current = players[0]

    def can_put(self, row):
        return self._grid[row][self.board_height - 1] is None

    def put(self, row):
        for i in range(self.board_height):
            if self._grid[row][i] is not None:
                continue

            self._grid[row][i] = self.current.id

            if self.current.id == len(self.players) - 1:
                self.current = self.players[0]
            else:
                self.current = self.players[self.current.id + 1]

            result = self.check_win(row, i)

            return i, result

    def check_draw(self):
        for i in self._grid[self.board_width - 1]:
            if i is not None:
                return True
        return False

    def check_win(self, row, column):
        player = self._grid[row][column]

        if player is None:
            return None

        connect = 0

        horizontal_left = max(row - self._connect + 1, 0)
        horizontal_right = min(row + self._connect, self.board_width) - 1

        for i in range(horizontal_left, horizontal_right + 1):
            if self._grid[i][column] == player:
                connect = connect + 1

                if connect == self._connect:
                    return MoveResult.VICTORY
            else:
                connect = 0

        connect = 0

        vertical_up = max(column - self._connect + 1, 0)
        vertical_down = min(column + self._connect, self.board_height) - 1

        for i in range(vertical_up, vertical_down + 1):
            if self._grid[row][i] == player:
                connect = connect + 1

                if connect == self._connect:
                    return MoveResult.VICTORY
            else:
                connect = 0

        connect = 0

        diagonal_up_left = min(row - horizontal_left, vertical_down - column)
        diagonal_down_right = min(horizontal_right - row, column - vertical_up)

        for i in range(0, diagonal_up_left + diagonal_down_right + 1):
            if self._grid[row - diagonal_up_left + i][column + diagonal_up_left - i] == player:
                connect = connect + 1

                if connect == self._connect:
                    return MoveResult.VICTORY
            else:
                connect = 0

        connect = 0

        diagonal_up_right = min(horizontal_right - row, vertical_down - column)
        diagonal_down_left = min(row - horizontal_left, column - vertical_up)

        for i in range(0, diagonal_up_right + diagonal_down_left + 1):
            if self._grid[row + diagonal_up_right - i][column + diagonal_up_right - i] == player:
                connect = connect + 1

                if connect == self._connect:
                    return MoveResult.VICTORY
            else:
                connect = 0

        return MoveResult.NONE


class Player:

    def __init__(self, id: int, color):
        self.id = id
        self.color = color


class State(Enum):
    PLAYING = 0,
    FINISHED = 1


class MoveResult(Enum):
    NONE = 1
    VICTORY = 1,
    DRAW = 2
