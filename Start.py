from elf_kingdom import *


class Zigzag:
    def __init__(self, game, elfDict):
        self.game = game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]
        self.zigDict = {}
        my_castle = game.get_my_castle().location
        enemy_castle = game.get_enemy_castle().location
        if game.cols > game.rows:
            self.x_is_bigger = True
            if my_castle.row > enemy_castle.row:
                self.middle_line = enemy_castle.row + (my_castle.row - enemy_castle.row)/2
                self.dist = (my_castle.row - enemy_castle.row)/2 - ((my_castle.row - enemy_castle.row)/2)/8
            else:
                self.middle_line = my_castle.row + (enemy_castle.row - my_castle.row)/2
                self.dist = (enemy_castle.row - my_castle.row)/2 - ((enemy_castle.row - my_castle.row)/2)/8
        else:
            self.x_is_bigger = False
            if my_castle.col > enemy_castle.col:
                self.middle_line = enemy_castle.col + (my_castle.col - enemy_castle.col)/2
                self.dist = (my_castle.col - enemy_castle.col)/2 - ((my_castle.col - enemy_castle.col)/2)/8
            else:
                self.middle_line = my_castle.col + (enemy_castle.col - my_castle.col)/2
                self.dist = (enemy_castle.col - my_castle.col)/2 - ((enemy_castle.col - my_castle.col)/2)/8

    def do_zigzag(self, game, elfDict):
        self.game = game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]
        amount_of_zigzag_elves = 1



class Start:
    """
    does all the start things
    one elf goes in zigzags
    the other is flanking
    """
    def __init__(self, game, elfDict):
        self.game = game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]
        self.zigzag = Zigzag(game, elfDict)

    def do_start(self, game, elfDict):
        # vars
        self.game = game  # update game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]  # update my_elves

        self.zigzag.do_zigzag(game, elfDict)
