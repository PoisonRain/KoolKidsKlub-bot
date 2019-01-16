from elf_kingdom import *

class Zigzag:
    """
    elf does ZigZags thats it
    """
    def __init__(self,game, elf, dist, jmp, dir):
        """
        :param dist: the distance from the straight line
        :param jmp: the jumps of distance on the straight line
        :param dir: the initial side they go (up/down)
        """
        self.dist = dist
        self.dir = dir
        self.enemy_castle = game.get_enemy_castle()
        self.tgt = elf.elf.location.towards(self.enemy_castle , jmp)
        self.jmp = jmp
        self.stp = 2*jmp
        self.to_go = elf.move_noraml(self.tgt, dist, -self.dir)


    def do_zig(self, elf):
        if elf.elf.location.equals(self.to_go):
            self.tgt = elf.elf.location.towards(self.get_enemy_castle(), self.jmp)
            self.stp += self.jmp
            self.to_go = elf.move_noraml(self.tgt, self.dist, self.dir)
            if self.dist == 1:
                self.dir = -1
            else:
                self.dir = 1
            elf.elf.move_to(self.to_go)
        else:
            elf.elf.move_to(self.to_go)

class Start:
    """
    does all the start things
    one elf goes in zigzags
    the other is flanking
    """
    def __init__(self, game, elfDict):
        self.game = game
        self.my_elves = list(elfDict.values())
        self.switch_sides = 1  # used to flip flop between direction the elves start to zigzag
        self.zigDict = {}
    
    def do_start(self, game, elfDict):
        # vars
        self.game = game  # update game
        self.my_elves = list(elfDict.values())  # update my_elves
        zigzag_amount = 1  # amount of elf to zigzag
        dist_zig = 1000  # distance to zig zag
        
        # main
        # move in zigzags
        while len(self.zigDict) < zigzag_amount:  # add new elves to zigDict
            for uid in elfDict.keys():
                if uid not in self.zigDict.keys():
                    self.zigDict[uid] = Zigzag(game, elfDict[uid], dist_zig, self.switch_sides)
                    if self.switch_sides == 1:
                        self.switch_sides = 0
                    else:
                        self.switch_sides = 1
                    break

        for uid in elfDict.keys():
            if uid in self.zigDict:
                self.zigDict[uid].do_zig(elfDict[uid])
            
            
        
        
        