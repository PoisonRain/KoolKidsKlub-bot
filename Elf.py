from elf_kingdom import *
import math


class Elf:
    """
    elf class is used to remember previous elf state and have complex moving methods
    """
    def __init__(self, game, elf):
        self.game = game
        self.elf = elf
        # used to remember where the user designated the elf to go last turn and where he actually went:
        self.moving_to = [Location(0,0), Location(0,0)]  # (user input, elf target)
        self.was_building = None  # used to check if the elf was building the previous turn

    def move(self, dis):
        self.elf.move_to(dis)

    def attack(self, tgt):  # walk to and attacks a target
        if tgt is not None and not self.elf.already_acted:
            if self.elf.in_attack_range(tgt):
                self.elf.attack(tgt)
            else:
                self.elf.move_to(tgt)

    def build_portal(self, tgt):  # walks to and builds a portal at a location
        if tgt is not None and not self.elf.already_acted:
            if self.elf.in_attack_range(tgt):
                self.attack(tgt)
            else:
                self.elf.move_to(tgt)

    def move_normal(self, tgt, dist, dir=None, srt=None, fix=None):
        """
        the elf (s) moves to a or b from :srt             a
        where e is designated point :tgt      -->   s-----e
        the distance from e to a|b is :dist               b

        :param tgt: The point where you make a normal line to you
        :param dist: The distance you want to go on the perpendicular line
        :param dir: The direction you prefer to go in (up, left) = 1, (down, right) = -1
        :param srt: Optional parameter, starting point; if not set is default to game.get_enemy_castle().location
        :param fix: optional parameter if left None location will move to my_castle until portal is able to be build
        else if set to 1 location will be moved towards tgt else if set to -1 location will be moved towards enemy_castle
        :return: The location the elf should go in

        """
        #if self.moving_to[0] == tgt:  # if the elf has the same target go to the previously calculated location
        #    return self.moving_to[1]
        #self.moving_to[0] = tgt

        if srt is None:
            srt = self.game.get_my_castle().location

        my_castle = self.game.get_my_castle()
        enemy_castle = self.game.get_enemy_castle()

        Xa = float(srt.col)
        Ya = float(srt.row)
        Xb = float(tgt.col)
        Yb = float(tgt.row)

        if Ya == Yb:
            pointA = Location(Yb + dist, Xb)
            pointB = Location(Yb - dist, Xb)
        else:
            Mab = (Ya - Yb) / (Xa - Xb)
            A = -Mab
            B = 1
            C = Mab * Xb - Yb

            Mbp = -(1 / Mab)
            Xp1 = int((dist * math.sqrt(A * A + B * B) - C + Mbp * Xb - Yb) / (A + Mbp))
            Yp1 = int(Mbp * Xp1 - Mbp * Xb + Yb)
            Xp2 = int(((-dist) * math.sqrt(A * A + B * B) - C + Mbp * Xb - Yb) / (A + Mbp))
            Yp2 = int(Mbp * Xp2 - Mbp * Xb + Yb)

            pointA = Location(Yp1, Xp1)
            pointB = Location(Yp2, Xp2)

        # check if you can build portal at pointA/B if not get a valid point:
        if fix == -1:
            while not self.game.can_build_portal_at(pointA) and not pointA.equals(enemy_castle):
                pointA = pointA.towards(enemy_castle, 5)
            while not self.game.can_build_portal_at(pointB) and not pointB.equals(enemy_castle):
                pointB = pointB.towards(enemy_castle, 5)
            if pointA.equals(enemy_castle) or pointB.equals(enemy_castle):
                print "REEE"
        elif fix == 1:
            while not self.game.can_build_portal_at(pointA) and not pointA.equals(tgt):
                pointA = pointA.towards(tgt, 5)
            while not self.game.can_build_portal_at(pointB) and not pointB.equals(tgt):
                pointB = pointB.towards(tgt, 5)
            if pointA.equals(tgt) or pointB.equals(tgt):
                print "REEE"
        else:
            while not self.game.can_build_portal_at(pointA) and not pointA.equals(my_castle):
                pointA = pointA.towards(my_castle, 5)
            while not self.game.can_build_portal_at(pointB) and not pointB.equals(my_castle):
                pointB = pointB.towards(my_castle, 5)

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
