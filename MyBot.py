from elf_kingdom import *
from Challenges import is_challenge
from Elf import *

# old state:
old_my_castle_health_3_turns = []
old_my_portals = []
elfDict = {}  # key: elf unique id; value: Elf instance
nrmI = None
agrI = None
srtI = None
defI = None
start_done = False
max_dist_from_castle = 12000
defence_portal_dist = 2000  # portals we consider as our defence portals


def do_turn(game):
    # vars
    global elfDict, old_my_portals, old_my_castle_health_3_turns
    my_elves = game.get_my_living_elves()
    my_portals = game.get_my_portals()
    enemy_castle = game.get_enemy_castle()
    my_castle = game.get_my_castle()

    if game.turn == 1:
        pass
    update_elfDict(game, my_elves)  # update elfDict

    # fix None
    if my_portals is None:  # sets list to list if its null
        my_portals = []

    print is_challenge(game)

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

