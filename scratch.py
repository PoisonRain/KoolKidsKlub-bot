from elf_kingdom import *
from math import sqrt

def find_circle_center(p1, p2, p3):
    x_p1, y_p1 = float(p1.col), float(p1.row)
    x_p2, y_p2 = float(p2.col), float(p2.row)
    x_p3, y_p3 = float(p3.col), float(p3.row)

    m_a = (y_p2 - y_p1) / (x_p2 - x_p1)
    m_b = (y_p3 - y_p2) / (x_p3 - x_p2)

    print (m_a, m_b)

    x_o = (m_a * m_b * (y_p1 - y_p3) + m_b * (x_p1 + x_p2) - m_a * (x_p2 + x_p3)) / (2 * (m_b - m_a))
    y_o = (-1 / m_a) * (x_o - (x_p1 + x_p2) / 2) + ((y_p1 + y_p2) / 2)

    return Location(y_o, x_o)


def circles_intersection(stp, obp, rad, dir=None):
    # param stp = the elf's current position
    # param obp = the given circle's center point
    # param rad = the given circle's radios
    # param dir = dictates which of the 2 point will be outputted, will default if not entered
    x_p1, y_p1 = float(stp.col), float(stp.row)
    x_p0, y_p0 = float(obp.col), float(obp.row)
    d = sqrt((x_p1 - x_p0) ** 2 + (y_p1 - y_p0) ** 2)

    a = (rad ** 2 - self.elf_rad ** 2 + d ** 2) / (2 * d)
    h = sqrt(rad ** 2 - a ** 2)
    x_p2, y_p2 = float(x_p0 + a * (x_p1 - x_p0) / d), float(y_p0 + a * (y_p1 - y_p0))

    x_p3_1, y_p3_1 = float(x_p2 + h * (y_p1 - y_p0) / d), float(y_p2 - h * (y_p1 - y_p0) / d)
    x_p3_2, y_p3_2 = float(x_p2 - h * (y_p1 - y_p0) / d), float(y_p2 + h * (y_p1 - y_p0) / d)

    if dir is None or dir == 1:
        return Location(y_p3_1, x_p3_1)
    else:
        return Location(y_p3_2, x_p3_2)



def pathing(self, stp, trp, rad, dir=None):
    # TODO make a check for a wall
    #   ## TODO make a check if the outpetted point is within a portal's range for which the point will then move along said range
    x_p1, y_p1 = float(stp.col), float(stp.row)
    x_p4, y_p4 = float(stp.col), float(stp.row)

    d = sqrt((x_p1 - x_p4) ** 2 + (y_p1 - y_p4) ** 2)
    third_point_dist = d / 16
    x_p5, y_p5 = (x_p1 + x_p4) / 2, (y_p1 + y_p4) / 2
    #
    p3rd = self.move_normal(Location(y_p5, x_p5), third_point_dist, dir, Location(y_p1, x_p1))

    p0 = self.find_circle_center(stp, p3rd, trp)
    x_p0, y_p0 = float(p0.col), float(p0.row)
    rad_0 = sqrt((x_p1 - x_p0) ** 2 + (y_p1 - y_p0) ** 2)
    p3 = self.circles_intersection(stp, p0, rad_0, dir)

    self.elf.move_to(p3)
    # if d_to_nearest_portal(p3) < rad:
    #    obp = nearest_portal(p3)
    #    circle_point = move_along_circle(stp, obp, rad, dir)
    #    move_to(circle_point)
    # else:
    #    move_to(p3)
    pass


    def move_normal(self, tgt, dist, dir=None, srt=None):
        x_a, y_a = float(srt.col), float(srt.row)
        x_b, y_b = float(tgt.col), float(tgt.row)

        x_d, y_d = x_a - x_b, y_a - y_b
        d = sqrt(x_d ** 2 + y_d ** 2)
        x_d /= d
        y_d /= d

        x_1, y_1 = x_a + dist * y_d, y_a - dist * x_d
        x_2, y_2 = x_a - dist * y_d, y_a + dist * x_d

        pointA = Location(y_1, x_1)
        pointB = Location(y_2, x_2)

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

print circles_intersection(Location(0,0), Location(0,2), 1)