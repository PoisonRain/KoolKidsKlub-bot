from elf_kingdom import *
import Elf
import GridSystem

def build_portal_at(elf, portal_loc): #recives portal location, goes to build a portal there, returns
    if elf.can_build_portal():
        elf.build_portal()