from elf_kingdom import *


class BotObject(MapObject):
    # Grid system
    # 0  1  2  3  4
    # 5  6  7  8  9
    # 10 11 12 13 14
    # 14 15 17 18 19
    def __init__(self, game):
        self.game = game

    @staticmethod
    def get_grid(self, other):
        col_jmp = self.game.cols / 5
        row_jmp = self.game.rows / 4
        grid_counter = 0

        for col in range(0, self.game.rows - row_jmp, row_jmp):
            for row in range(0, self.game.cols - col_jmp, col_jmp):
                if (col <= other.location.col <= col + col_jmp) and (row <= other.location.row <= row + row_jmp):
                    return grid_counter
                grid_counter += 1
