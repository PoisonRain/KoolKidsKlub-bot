from elf_kingdom import *


def aggressive(game, elfDict):
    try:
        # vars
        my_elves = [elf for key, elf in elfDict]
        switch_sides = False  # switching side on the perpendicular line

        # funcs
        def get_attack_location():
            pass

        # main
        for elf in my_elves:  # attack with each elf
            elf.move(get_attack_location())

    except Exception, msg:
        print "Something in the aggressive mode fucked up"
        print msg
