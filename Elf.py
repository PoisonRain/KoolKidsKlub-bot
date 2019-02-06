from elf_kingdom import *
from math import sqrt


class Elf:
    """
    elf class is used to remember previous elf state and have complex moving methods
    """
    def __init__(self, game, elf, rows, cols):
        self.game = game
        self.elf = elf
        self.rows = rows
        self.cols = cols
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
        global pointA, pointB
        if srt is None:
            srt = self.game.get_my_castle().location

        my_castle = self.game.get_my_castle()
        enemy_castle = self.game.get_enemy_castle()

        x_a, y_a = float(tgt.col), float(tgt.row)
        x_b, y_b = float(srt.col), float(srt.row)

        x_d, y_d = x_a - x_b, y_a - y_b
        d = sqrt(x_d ** 2 + y_d ** 2)

        x_d /= d
        y_d /= d

        x_1, y_1 = x_a + dist * y_d, y_a - dist * x_d
        x_2, y_2 = x_a - dist * y_d, y_a + dist * x_d

        pointA = Location(int(y_1), int(x_1))
        pointB = Location(int(y_2), int(x_2))

        def out_of_boundaries(game, loc, dist):
            if loc.row > self.rows - dist or loc.row < dist:
                return False
            elif loc.col > self.cols - dist or loc.col < dist:
                return False
            else:
                return True

        def check_if_able_to_build(loc):  # check if able to build a portal if not move the point over
            global pointA, pointB
            while not self.game.can_build_portal_at(pointA) and not pointA.equals(loc) and out_of_boundaries(self.game, pointA, 50):
                pointA = pointA.towards(loc, 5)
            while not self.game.can_build_portal_at(pointB) and not pointB.equals(loc) and out_of_boundaries(self.game, pointB, 50):
                pointB = pointB.towards(loc, 5)
            if pointA.equals(loc) or pointB.equals(loc):
                print "REEE"

        if fix == -1:
            check_if_able_to_build(enemy_castle)
        elif fix == 1:
            check_if_able_to_build(tgt)
        else:
            check_if_able_to_build(my_castle)

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
