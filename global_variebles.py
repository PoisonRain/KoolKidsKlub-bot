from elf_kingdom import *

# Grid system
# 0  1  2  3  4
# 5  6  7  8  9
# 10 11 12 13 14
# 14 15 17 18 19

max_cols = game.cols
max_rows = game.rows
my_portals = game.get_my_portals()
my_castle = game.get_my_castle()
enemy_portals = game.get_enemy_portals()
enemy_castle = game.get_enemy_castle()
attack_elf = game.get_all_my_elves()[1]
defense_elf = game.get_all_my_elves()[0]
enemy_elves = game.get_enemy_living_elves()
enemy_lava = game.get_enemy_lava_giants()
enemy_ice = game.get_enemy_ice_trolls()

if my_portals:
    enemy_has_portals = True
else:
    enemy_has_portals = False

if my_portals:
    have_portals = True
else:
    have_portals = False
