from elf_kingdom import *
from handle_elves import handle_elves


def do_turn(game):
    try:
        handle_elves(game)
    except Exception, msg:
        print "Something without a try fucked up, rip"
        print msg
