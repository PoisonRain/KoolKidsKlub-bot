from elf_kingdom import *
from global_variebles import *


class BaseObject:
    # Grid system
    # 0  1  2  3  4
    # 5  6  7  8  9
    # 10 11 12 13 14
    # 14 15 17 18 19

    def get_grid(self, obj):
        col_jmp = max_cols / 5
        row_jmp = max_rows / 4
        grid_counter = 0

        for col in range(0, max_rows - row_jmp, row_jmp):
            for row in range(0, max_cols - col_jmp, col_jmp):
                if (col <= obj.location.col <= col + col_jmp) and (row <= obj.location.row <= row + row_jmp):
                    return grid_counter
                grid_counter += 1
