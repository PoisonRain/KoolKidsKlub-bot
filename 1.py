from elf_kingdom import *
from math import sqrt


class Elf:
    """
    elf class is used to remember previous elf state and have complex moving methods
    """
    def __init__(self, game, elf):
        self.game = game
        self.elf = elf
        self.elf_rad = game.elf_max_speed
        # used to remember where the user designated the elf to go last turn and where he actually went:
        self.moving_to = [Location(0,0), Location(0,0)]  # (user input, elf target)
        self.was_building = None  # used to check if the elf was building the previous turn
#
    #def d_to_nearest_portal(point):
    #    pass
#
    #def nearest_portal(point):
    #    #portal = portal
    #    pass
    #
    #def get_enemy_portal(self):
    #    pass
#
    #def move_to(point):
    #    pass
#
    #def move_normal(tgt, dist, dir=None, srt=None):
    #    pass
#
    #def check_for_wall(u_id):
    #    pass
#
    ## search up "Paul Bourke circles sphere" if u wanna know whats going on here, should be
    ## under circles intersections iirc
    ## @paulbourke.net/geometry/circlesphere/


    def find_circle_center(self, p1, p2, p3):
        m_a = (p2.row - p1.row) / (p2.col - p1.col)
        m_b = (p3.row - p2.row) / (p3.col - p2.col)

        x_o = (m_a * m_b * (p1.row - p3.row) + m_b * (p1.col + p2.col) - m_a * (p2.col + p3.col)) / (2 * (m_b - m_a))
        y_o = (-1 / m_a) * (x_o - (p1.col + p2.col) / 2) + ((p1.row + p2.row) / 2)

        return Location(y_o, x_o)

    # outputs 1 out of the 2 intersection points between a circle and the elf's range(100 rad)
    def circles_intersection(self, stp, obp, rad, dir=None):
        # param stp = the elf's current position
        # param obp = the given circle's center point
        # param rad = the given circle's radios
        # param dir = dictates which of the 2 point will be outputted, will default if not entered
        p1 = (stp.col, stp.row)
        p0 = (obp.col, obp.row)
        d = sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)

        a = (rad ** 2 - self.elf_rad ** 2 + d ** 2) / (2 * d)
        h = sqrt(rad ** 2 - a ** 2)
        p2 = (p0[0] + a * (p1[0] - p0[0]) / d, p0[1] + a * (p1[1] - p0[1]) / d)

        p3_1 = (p2[0] + h * (p1[1] - p0[1]) / d, p2[1] - h * (p1[0] - p0[0]) / d)
        p3_2 = (p2[0] - h * (p1[1] - p0[1]) / d, p2[1] + h * (p1[0] - p0[0]) / d)

        if dir is None or dir == 1:
            return Location(p3_1[1], p3_1[0])
        else:
            return Location(p3_2[1], p3_2[0])

    def pathing(self, stp, trp, rad, dir=None):
        # TODO make a check for a wall
     #   ## TODO make a check if the outpetted point is within a portal's range for which the point will then move along said range
        p1 = (stp.col, stp.row)
        p4 = (trp.col, trp.row)
        d = sqrt((p1[0] - p4[0]) ** 2 + (p1[1] - p4[1]) ** 2)
        third_point_dist = d / 16
        p5 = ((p1[0] + p4[0]) / 2, (p1[1] + p4[1]) / 2)
#
        p3rd = self.move_normal(Location(p5[1], p5[0]), third_point_dist, dir, Location(p1[1], p1[0]))
        #0p3rd = (p3rd_0.col, p3rd_0.row)
#
        print(stp, trp, p3rd)

        p0 = self.find_circle_center(stp, p3rd, trp)
        rad_0 = sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)
        p3 = self.circles_intersection(stp, p0, rad_0, dir)

        self.elf.move_to(p3)
        #if d_to_nearest_portal(p3) < rad:
        #    obp = nearest_portal(p3)
        #    circle_point = move_along_circle(stp, obp, rad, dir)
        #    move_to(circle_point)
        #else:
        #    move_to(p3)
        pass

    def move(self, dis):
        stp = self.elf.location
        trp = dis
        rad = 100
        self.pathing(stp, trp, rad)

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
        Xp1 = int((dist * sqrt(A * A + B * B) - C + Mbp * Xb - Yb) / (A + Mbp))
        Yp1 = int(Mbp*Xp1 - Mbp*Xb + Yb)
        Xp2 = int(((-dist) * sqrt(A * A + B * B) - C + Mbp * Xb - Yb) / (A + Mbp))
        Yp2 = int(Mbp * Xp2 - Mbp * Xb + Yb)

        pointA = Location(Yp1, Xp1)
        pointB = Location(Yp2, Xp2)

        # check if you can build portal at pointA/B if not get a valid point:
        while not self.game.can_build_portal_at(pointA):
            pointA = pointA.towards(my_castle, 5)
        while not self.game.can_build_portal_at(pointB):
            pointB = pointB.towards(my_castle, 5)

        # choosing pointA or pointB:
        if dir is None:
            enemy_portals = self.game.get_enemy_portals()
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
