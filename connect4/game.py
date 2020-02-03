from enum import Enum


class Game:

    def __init__(self, players, board_width, board_height, connect):
        self.state = State.PLAYING
        self._players = players
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

            player = self.current
            self._grid[row][i] = player.id

            if player.id == len(self._players) - 1:
                self.current = self._players[0]
            else:
                self.current = self._players[player.id + 1]

            (result, positions) = self.check_win(row, i)

            if result != MoveResult.NONE:
                self.state = State.FINISHED

                if result == MoveResult.VICTORY:
                    return i, result, Victory(player, positions)
            else:
                if self.check_draw():
                    self.state = State.FINISHED

                    return i, MoveResult.DRAW, None

            return i, result, None

    def check_draw(self):
        for i in range(self.board_width):
            if self._grid[i][self.board_height - 1] is None:
                return False
        return True

    def check_win(self, row, column):
        player = self._grid[row][column]

        if player is None:
            return None

        positions = []

        horizontal_left = max(row - self._connect + 1, 0)
        horizontal_right = min(row + self._connect, self.board_width) - 1

        for i in range(horizontal_left, horizontal_right + 1):
            if self._grid[i][column] == player:
                positions.append((i, column))

                if len(positions) == self._connect:
                    return MoveResult.VICTORY, positions
            else:
                positions.clear()

        positions.clear()

        vertical_up = max(column - self._connect + 1, 0)
        vertical_down = min(column + self._connect, self.board_height) - 1

        for i in range(vertical_up, vertical_down + 1):
            if self._grid[row][i] == player:
                positions.append((row, i))

                if len(positions) == self._connect:
                    return MoveResult.VICTORY, positions
            else:
                positions.clear()

        positions.clear()

        diagonal_up_left = min(row - horizontal_left, vertical_down - column)
        diagonal_down_right = min(horizontal_right - row, column - vertical_up)

        for i in range(0, diagonal_up_left + diagonal_down_right + 1):
            if self._grid[row - diagonal_up_left + i][column + diagonal_up_left - i] == player:
                positions.append((row - diagonal_up_left + i, column + diagonal_up_left - i))

                if len(positions) == self._connect:
                    return MoveResult.VICTORY, positions
            else:
                positions.clear()

        positions.clear()

        diagonal_up_right = min(horizontal_right - row, vertical_down - column)
        diagonal_down_left = min(row - horizontal_left, column - vertical_up)

        for i in range(0, diagonal_up_right + diagonal_down_left + 1):
            if self._grid[row + diagonal_up_right - i][column + diagonal_up_right - i] == player:
                positions.append((row + diagonal_up_right - i, column + diagonal_up_right - i))

                if len(positions) == self._connect:
                    return MoveResult.VICTORY, positions
            else:
                positions.clear()

        return MoveResult.NONE, None


class Player:

    def __init__(self, id: int, color):
        self.id = id
        self.color = color


class Victory:

    def __init__(self, player: Player, positions: []):
        self.player = player
        self.positions = positions


class State(Enum):
    PLAYING = 0,
    FINISHED = 1,
    DESTROYED = 2


class MoveResult(Enum):
    NONE = 1
    VICTORY = 1,
    DRAW = 2
