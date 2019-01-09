"""
this file contains all of the elf handles
probs later will be divided for ease of use mid comp
or not ? really depends if they add more elves
"""

from elib import *
from elf_kingdom import *



def handle_elves(game):
    try:
        # vars
        my_elves = game.get_my_living_elves()
        enemy_elves = game.get_enemy_living_elves()
        enemy_portals = game.get_enemy_portals()
        my_portals = game.get_my_portals()
        enemy_castle = game.get_enemy_castle()
        enemy_ice = game.get_enemy_ice_trolls()
        my_castle = game.get_my_castle()

        # funcs
        def elf_flanking(game, elf):  # well its the elf that flanks n shit
            if enemy_castle.location.row > my_castle.location.row:
                pass  # flank with the most bottom elf
            else:
                pass  # flank with the most upper elf (aka whitest elf)

        # main
        if my_elves:  # general check if we have elves
            if my_portals:
                if (len(filter(lambda x: x.location.distance(my_castle.location) > x.location.distance(enemy_castle.location), my_portals)) < 1):  # basically check if you have an attack portal
                    elf_flanking()

    except Exception, msg:
        print "fuck elf handling fucked up"
        print msg



