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

        """
        every time we use an elf remove it from my_elves !!!!!!
        funcs:
        """
        def elf_flanking(game):  # well its the elf that flanks n shit
            if enemy_castle.location.row > my_castle.location.row:
                pass  # flank with the most bottom elf
            else:
                pass  # flank with the most upper elf (aka whitest elf)

        def elf_general(game):  # catch all for all the elves without a designated role
            for elf in my_elves:
                for troll in enemy_ice:
                    if elf.location.distance(troll) < 150:  # if you have an ice troll close run from them then break
                        break
                        pass
                    else:  # general attack thing here
                        pass

        # main
        if my_elves:  # general check if we have elves
            if my_portals:
                # basically check if you have a portal close to the enemy castle:
                if len(filter(lambda x: x.location.distance(enemy_castle.location) < 1500, my_portals)) != 0:
                    elf_flanking(game)
            if my_elves: # check if still has elves to make moves with
                elf_general(game) # catch all

    except Exception, msg:
        print "fuck, elf handling fucked up"
        print msg



