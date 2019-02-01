from elf_kingdom import *
from Elf import *
from Start import start
from Aggressive import Aggressive
from Normal import normal
import flanking

elfDict = {}  # key: elf unique id; value: Elf instance
attackDict = {}  # key: portal unique id; value: portal instance
alreadyNormal = False
old_my_portals = []
nrmI = None
agrI = None
srtI = None


def update_attackDict(my_elves, my_portals):
    global attackDict, old_my_portals
    attack_portal = None
    if my_portals:
        for uid in attackDict.keys():  # delete destroyed portals
            if uid not in [portal.unique_id for portal in my_portals]:
                del attackDict[uid]

        for elf in my_elves:  # add new attack portals
            if elf.elf.is_building is False and elf.was_building is True:
                for portal in my_portals:
                    if portal not in old_my_portals:
                        attack_portal = portal
                        break
                if attack_portal is not None:
                    attackDict[attack_portal.unique_id] = attack_portal
                elf.was_building = False
    else:
        attackDict.clear()


def update_elfDict(game, my_elves):
    global elfDict
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


def must_have_portals(elfDict):
    pass


def do_turn(game):
        # vars
        global elfDict, attackDict, agrI, old_my_portals
        my_elves = game.get_my_living_elves()
        my_portals = game.get_my_portals()
        enemy_castle = game.get_enemy_castle()
        my_castle = game.get_my_castle()
        flank_elves = []  # list of all elves that try to flank and build a portal
        if agrI is None:
            agrI = Aggressive(game, elfDict, attackDict)
        

        if game.turn == 1:
            flanking.initialize(elves)

        update_elfDict(game, my_elves)  # update elfDict

        # fix None
        if my_portals is None:  # sets list to list if its null
            my_portals = []
        
        flank_elves = agrI.do_aggressive(game, elfDict, attackDict)
        # choosing an attack mode:
        #if not alreadyNormal and len(my_portals) < 7 and game.turn < (my_castle.location.distance(enemy_castle) / 50):
        #    start(game, elfDict)
        #elif must_have_portals(my_portals) and ((game.get_enemy_mana() < 100 and my_castle.current_health > 75) or (enemy_castle.current_health and my_castle.current_health > 75)):
        #    flank_elves = agrI.do_aggressive(game, elfDict, attackDict)
        #else:
        #    flank_elves = normal(game, elfDict)

        update_attackDict(flank_elves, my_portals)  # updating attackDict

        old_my_portals = my_portals  # update old_my_portals

