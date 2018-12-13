from elf_kingdom import *
import AttackElf

def do_turn(game):
    attack_elf = AttackElf(game)
    attack_elf.handle()
