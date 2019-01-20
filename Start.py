from elf_kingdom import *


class Start:
    """
    does all the start things
    one elf goes in zigzags
    the other is flanking
    """
    def __init__(self, game, elfDict):
        self.game = game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]
        self.switch_sides = -1  # used to flip flop between direction the elves start to zigzag
        self.zigDict = {}
    
    def do_start(self, game, elfDict):
        # vars
        self.game = game  # update game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]  # update my_elves
        zig_elf_count = 1  # amount of elf to zigzag
        zig_dist = 1000  # distance to zig zag
        jmp = 1000




            
        
        
        