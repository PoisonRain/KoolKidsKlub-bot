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

    return a


def get_point_by_alpha(alpha, center_point, trgt_point):
    """
    returns a point on the circle at a certain angle
    :param alpha: the angle
    :param center_point: the center of the circle
    :param trgt_point: a point on the circle
    :return: a new point on the circle at the provided angleit
    """
    radius = center_point.distance(trgt_point)
    center_point = location_to_tuple(center_point)

    x = center_point[0] + radius * math.cos(alpha)
    y = center_point[1] + radius * math.sin(alpha)

    tup = (int(x), int(y))

    return tuple_to_location(tup)

