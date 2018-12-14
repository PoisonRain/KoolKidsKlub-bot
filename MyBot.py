from elf_kingdom import *
from AttackElf import *

def do_turn(game):
    attack_elf = AttackElf(game)
    attack_elf.handle()
