"""
elf class n shit
"""

from elf_kingdom import *
import math


class Elf:
    def __init__(self, game, elf):
        self.game = game
        self.elf = elf
        # used to remember where the user designated the elf to go last turn and where he actually went:
        self.moving_to = (Location(0,0), Location(0,0))  # (user input, elf target)

    def move(self, dis):
        pass

    def move_normal(self, tgt, dist, dir=1, srt=None):
        """
        the elf (s) moves to a or b from :srt             a
        where e is designated point :tgt      -->   s-----e
        the distance from e to a|b is :dist               b

        :param tgt: The point where you make a normal line to you
        :param dist: The distance you want to go on the perpendicular line
        :param dir: The direction you prefer to go in (up, left) = 1, (down, right) = -1; default is 1
        :param srt: Optional parameter, starting point; if not set is default to game.get_enemy_castle().location
        :return: true if was able to move the elf false other wise

        """
        if self.moving_to[0] == tgt:  # if the elf has the same target go to the previously calculated location
            self.move(self.moving_to[1])
            return
        if srt is None:
            srt = self.game.get_my_castle().location

        Xa = srt.col
        Ya = srt.row
        Xb = tgt.col
        Yb = tgt.row

        Mab = (Ya - Yb) // (Xa - Xb)
        A = -Mab
        B = 1
        C = Mab * Xb - Yb

        Mbp = -(1 // Mab)
        Xp1 = int((dist * math.sqrt(A * A + B * B) - C + Mbp * Xb - Yb) / (A + Mbp))
        Yp1 = int(Mbp*Xp1 - Mbp*Xb +Yb)
        Xp2 = int(((-dist) * math.sqrt(A * A + B * B) - C + Mbp * Xb - Yb) / (A + Mbp))
        Yp2 = int(Mbp * Xp2 - Mbp * Xb + Yb)

        pointA = Location(Yp1, Xp1)
        pointB = Location(Yp2, Xp2)
        print "pointA: " + str(pointA) + " pointB: " + str(pointB)
        self.elf.move_to(pointA)
