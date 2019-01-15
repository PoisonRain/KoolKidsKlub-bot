from elf_kingdom import *
from Elf import *
from Start import start
from Aggressive import aggressive
from Normal import normal

elfDict = {}
alreadyNormal = False


def do_turn(game):
    try:
        # vars
        my_elves = game.get_my_living_elves()
        my_portals = game.get_my_portals()
        enemy_castle = game.get_enemy_castle()
        my_castle = game.get_my_castle()

        # funcs
        def must_have_portals(game, elfDict):
            pass

        # main
        if my_elves:  # add new and delete old elves from the dictionary
            for elf in my_elves:  # add new
                if elf.unique_id not in elfDict:
                    elfDict[elf.unique_id] = Elf(game, elf)

            for uid in elfDict:  # delete old
                if uid not in my_elves:
                    del elfDict[uid]
        else:  # if we have no elves just clear the dictionary
            elfDict.clear()

        for key,val in elfDict:  # update game for all elf objects
            val.game = game

        if my_portals is None: # sets list to list if its null
            my_portals = []
        # choosing an attack mode:
        if not alreadyNormal and len(my_portals) < 7 and game.turn < (my_castle.location.distance(enemy_castle) / 50):
            start(game, elfDict)
        elif must_have_portals(my_portals) and ((game.get_enemy_mana() < 100 and my_castle.current_health > 75) or (enemy_castle.current_health and my_castle.current_health > 75)):
            aggressive(game, elfDict)
        else:
            normal(game, elfDict)

    except Exception, msg:
        print "Something without a try fucked up, rip"
        print msg
