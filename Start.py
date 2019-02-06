from elf_kingdom import *


class Zigzag:
    """
    handles zigzags for all elves
    """
    def __init__(self, game, elfDict):
        self.game = game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]
        self.zigDict = {}
        self.switch_sides = -1
        my_castle = game.get_my_castle().location
        enemy_castle = game.get_enemy_castle().location
        if game.cols > game.rows:  # get the mid on the y axis
            self.x_is_bigger = True
            self.middle_line = (my_castle.row + enemy_castle.row) / 2
            if my_castle.row > enemy_castle.row:  # get the distance to make normal line on
                self.dist = ((my_castle.row - enemy_castle.row)/2)
            else:
                self.dist = ((enemy_castle.row - my_castle.row)/2)
            if my_castle.col > enemy_castle.col:  # get mix and max
                self.min = enemy_castle.col
                self.max = my_castle.col
            else:
                self.min = my_castle.col
                self.max = enemy_castle.col
        else:  # get the mid on the x axis
            self.x_is_bigger = False
            self.middle_line = (my_castle.col + enemy_castle.col)/2
            if my_castle.col > enemy_castle.col:  # get the distance to make normal line on
                self.dist = ((my_castle.col - enemy_castle.col)/2)
            else:
                self.dist = ((enemy_castle.col - my_castle.col)/2)
            if my_castle.row > enemy_castle.row:  # get mix and max
                self.min = enemy_castle.row
                self.max = my_castle.row
            else:
                self.min = my_castle.row
                self.max = enemy_castle.row
        self.min += 1000  # normalize min max
        self.max -= 1000
        self.dist *= 0.8  # normalize dist

    def update_zigDict(self, elfDict):
        """
        gets updated zigDict checks for new entries gives them in an altering manner a direction to go
        and deletes dead elves from the dictionary
        """
        for uid in elfDict.keys():
            if uid not in self.zigDict:
                self.zigDict[uid] = self.switch_sides
                if self.switch_sides == 1:
                    self.switch_sides = -1
                else:
                    self.switch_sides = 1

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
