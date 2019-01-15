from elf_kingdom import *

global distance_from_line
distance_from_line = 500


def start(game, elfDict):
    my_castle_loc = game.get_my_castle().location
    enemy_castle_loc = game.get_enemy_castle().location
    m = -1 / (float(my_castle_loc.row - enemy_castle_loc.row) / (
                enemy_castle_loc.col - my_castle_loc.col))  # the y axis is inverted, while the x is normal, and so is the slope formula
    b = my_castle_loc.row + m * my_castle_loc.col
    print(b)
    print(str(-m) + '*x + ' + str(b))  # normal line equation
    print(-m * (my_castle_loc.col + distance_from_line) + b)
