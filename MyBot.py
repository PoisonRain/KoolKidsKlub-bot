from elf_kingdom import *
from Elf import *
from Start import Start
from Aggressive import Aggressive
from Normal import Normal
from Defense import Defense
from Infrastructure import Infrastructure
import flanking

# old state:
old_my_castle_health_3_turns = []
old_my_portals = []
elfDict = {}  # key: elf unique id; value: Elf instance
nrmI = None
agrI = None
srtI = None
defI = None
infI = None
start_done = True
max_dist_from_castle = 12000
defence_portal_dist = 2000  # portals we consider as our defence portals


def do_turn(game):
    # vars
    global elfDict, attackDict, agrI, nrmI, srtI, defI, infI, old_my_portals, old_my_castle_health_3_turns, start_done
    my_elves = game.get_my_living_elves()
    my_portals = game.get_my_portals()
    enemy_castle = game.get_enemy_castle()
    my_castle = game.get_my_castle()
    flank_elves = []  # list of all elves that try to flank and build a portal
    if agrI is None:
        agrI = Aggressive(game, elfDict)
    if srtI is None:
        portal_amount = 3
        fountain_amount = game.get_my_mana() / game.mana_fountain_cost
        if fountain_amount < 1:
            fountain_amount = 1
        srtI = Start(game, elfDict, portal_amount, 1600, fountain_amount)
    if nrmI is None:
        nrmI = Normal(game, elfDict, agrI, srtI)
    if defI is None:
        defI = Defense(game, elfDict)
    if infI is None:
        infI = Infrastructure(game, elfDict)

    if game.turn == 1:
        flanking.initialize(my_elves)

    update_elfDict(game, my_elves)  # update elfDict

    # fix None
    if my_portals is None:  # sets list to list if its null
        my_portals = []

    infI.update(game, elfDict)
    infI.add_infrastructure()
    infI.build_and_maintain()
    ##choosing an attack mode:#
    #if agrI.get_aggresive_score(game) > 0 or enemy_castle.current_health < 16:
    #    print "aggressive mode"
    #    agrI.do_aggressive(game, elfDict, nrmI)
    #elif not start_done and game.turn < (my_castle.location.distance(enemy_castle) / 100):
    #    print "start mode"
    #    start_done = srtI.do_start(game, elfDict)
    #else:
    #    print "normal mode"
    #    nrmI.do_normal(game, elfDict)

    # update old state:
    old_my_portals = my_portals
    old_my_castle_health_3_turns.append(my_castle.current_health)
    old_my_castle_health_3_turns = old_my_castle_health_3_turns[:3]
    for elf in elfDict.values():
        elf.old_health_2_turns.append(elf.elf.current_health)
        elf.old_health_2_turns = elf.old_health_2_turns[:2]


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

