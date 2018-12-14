from elf_kingdom import *


class GridSystem:
    @staticmethod
    def check_build_in_grid(game, grid):
        jmp_x = game.cols / 5
        jmp_y = game.rows / 4
        start_x = grid[0] * jmp_x
        start_y = grid[1] * jmp_y

        for row in range(start_y, start_y + jmp_y, 300):
            for col in range(start_x, start_x + jmp_x, 300):
                if game.can_build_portal_at(Location(col, row)):
                    return Location(col, row)
        return False

    @staticmethod
    def is_portal_at_grid(game, portal, grid):
        jmp_x = game.cols / 5
        jmp_y = game.rows / 4
        start_x = grid[0] * jmp_x
        start_y = grid[1] * jmp_y

        for row in range(start_y, start_y + jmp_y, 300):
            for col in range(start_x, start_x + jmp_x, 300):
                if portal.location == (Location(col, row)):
                    return True
        return False
