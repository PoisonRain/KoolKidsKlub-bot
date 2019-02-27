from flanking import tuple_to_location, location_to_tuple
import math


def get_alpha_from_points(center_point, trgt_point):
    """
    get two points and returns the angle from the center
    :param center_point: the center of the circle
    :param trgt_point: a point on the circle
    :return: the angle of the target point
    """
    radius = center_point.distance(trgt_point)

    center_point = location_to_tuple(center_point)
    trgt_point = location_to_tuple(trgt_point)

    a = math.acos(trgt_point[0] / (center_point[0] + radius))

    if trgt_point[1] > center_point[1]:
        return math.degrees(a)
    return 360 - math.degrees(a)


def get_point_by_alpha(alpha, center_point, trgt_point):
    """
    returns a point on the circle at a certain angle
    :param alpha: the angle
    :param center_point: the center of the circle
    :param trgt_point: a point on the circle
    :return: a new point on the circle at the provided angle
    """
    radius = center_point.distance(trgt_point)
    center_point = location_to_tuple(center_point)
    alpha = math.radians(alpha)
    x = center_point[0] + radius * math.cos(alpha)
    y = center_point[1] + radius * math.sin(alpha)

    tup = (int(x), int(y))

    return tuple_to_location(tup)


def move_point_by_angle(axis, point, angle_delta):
    """
    moves a point by a certain angle on an axis
    :param axis: the axis (center)
    :param point: the point to move
    :param angle_delta: the amount of degrees
    :return: the new point
    """
    angle = get_alpha_from_points(axis, point)
    angle += angle_delta
    return get_point_by_alpha(math.radians(angle), axis, point)

#print move_point_by_angle(Location(0,0), Location(0,1), 90), (1, 0)
#print move_point_by_angle(Location(0,0), Location(1,0), 90), (0, -1)
#print move_point_by_angle(Location(0,0), Location(0,-1), 90), (-1, 0)
#print move_point_by_angle(Location(0,0), Location(-1,0), 90), (0, 1)