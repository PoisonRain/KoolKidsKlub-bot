from elf_kingdom import *
from handle_elves import *


def do_turn(game):
    try:
        handle_elves(game)
    except Exception, msg:
        print "Something withoud a try fucked up rip"
        print msg
