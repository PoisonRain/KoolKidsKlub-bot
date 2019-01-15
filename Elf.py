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
        self.moving_to = [Location(0,0), Location(0,0)]  # (user input, elf target)
        self.was_building = None  # used to check if the elf was building the previous turn

    def move(self, dis):
        self.elf.move_to(dis)

    def move_normal(self, tgt, dist, dir=None, srt=None):
        """
        the elf (s) moves to a or b from :srt             a
        where e is designated point :tgt      -->   s-----e
        the distance from e to a|b is :dist               b

        :param tgt: The point where you make a normal line to you
        :param dist: The distance you want to go on the perpendicular line
        :param dir: The direction you prefer to go in (up, left) = 1, (down, right) = -1
        :param srt: Optional parameter, starting point; if not set is default to game.get_enemy_castle().location
        :return: The location the elf should go in

        """
        #if self.moving_to[0] == tgt:  # if the elf has the same target go to the previously calculated location
        #    return self.moving_to[1]
        #self.moving_to[0] = tgt

        if srt is None:
            srt = self.game.get_my_castle().location
        my_castle = self.game.get_my_castle()

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
        Yp1 = int(Mbp*Xp1 - Mbp*Xb + Yb)
        Xp2 = int(((-dist) * math.sqrt(A * A + B * B) - C + Mbp * Xb - Yb) / (A + Mbp))
        Yp2 = int(Mbp * Xp2 - Mbp * Xb + Yb)

        pointA = Location(Yp1, Xp1)
        pointB = Location(Yp2, Xp2)
        print str(self.elf) + "pointA: " + str(pointA) + " pointB: " + str(pointB)

        # check if you can build portal at pointA/B if not get a valid point:
        while not self.game.can_build_portal_at(pointA):
            pointA = pointA.towards(my_castle, 100)
        while not self.game.can_build_portal_at(pointB):
            pointB = pointB.towards(my_castle, 100)

        # choosing pointA or pointB:
        if dir is None:
            enemy_portals = self.game.get_enemy_castle()
            dest = pointA
            max = 0
            if enemy_portals:
                for point in [pointA, pointB]:
                    for portal in enemy_portals:
                        if point.distance(portal.location) > max:
                            max = point.distance(portal.location)
                            dest = point
                self.moving_to[1] = dest
                return dest

            else:
                self.moving_to[1] = pointA
                return pointA
        elif dir == 1:
            self.moving_to[1] = pointA
            return pointA
        elif dir == -1:
            self.moving_to[1] = pointB
            return pointB
        else:
            self.moving_to[1] = pointA
            return pointA
