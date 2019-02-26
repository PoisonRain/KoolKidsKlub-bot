from flanking import tuple_to_location, location_to_tuple
from elf_kingdom import Location
import math


def get_alpha_from_points(center_point, trgt_point):
    """
    get two points and returns the angle from the center
    :param center_point: the center of the circle
    :param trgt_point: a point on the circle
    :return: the angle of the target point
    """
    radius = center_point.distance(trgt_point)

    a = math.acos(trgt_point.col / (center_point.col + radius))

    if trgt_point.row > center_point.row:
        return math.degrees(a) % 360
    return (360 - math.degrees(a)) % 360


def get_point_by_alpha(alpha, center_point, trgt_point):
    """
    returns a point on the circle at a certain angle
    :param alpha: the angle
    :param center_point: the center of the circle
    :param trgt_point: a point on the circle
    :return: a new point on the circle at the provided angle
    """
    radius = center_point.distance(trgt_point)
    alpha = math.radians(alpha)
    x = center_point.col + radius * math.cos(alpha)
    y = center_point.row + radius * math.sin(alpha)

    return Location(int(y), int(x))


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
