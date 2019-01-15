from elf_kingdom import *
from Elf import *
from Start import start
from Aggressive import Aggressive
from Normal import normal

elfDict = {}
alreadyNormal = False
nrmI = None
agrI = None
srtI = None


def do_turn(game):
        # vars
        my_elves = game.get_my_living_elves()
        my_portals = game.get_my_portals()
        enemy_castle = game.get_enemy_castle()
        my_castle = game.get_my_castle()
        if agrI is None:
            agrI = Aggressive(game, elfDict)


        # funcs
        def must_have_portals(elfDict):
            pass

        # main
        # update elfDict
        if my_elves:  # add new and delete old elves from the dictionary
            for elf in my_elves:  # add new
                if elf.unique_id not in elfDict.keys():
                    elfDict[elf.unique_id] = Elf(game, elf)

            for uid in elfDict.keys():  # delete old
                if uid not in [elf.unique_id for elf in my_elves]:
                    del elfDict[uid]
        else:  # if we have no elves just clear the dictionary
            elfDict.clear()

        for elf in elfDict.values():  # update game for all elf objects
            elf.game = game

        # fix None
        if my_portals is None:  # sets list to list if its null
            my_portals = []

        # choosing an attack mode:
        if not alreadyNormal and len(my_portals) < 7 and game.turn < (my_castle.location.distance(enemy_castle) / 50):
            start(game, elfDict)
        elif must_have_portals(my_portals) and ((game.get_enemy_mana() < 100 and my_castle.current_health > 75) or (enemy_castle.current_health and my_castle.current_health > 75)):
            agrI.do_aggressive(game, elfDict)
        else:
            normal(game, elfDict)
