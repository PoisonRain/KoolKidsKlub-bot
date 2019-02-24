from flanking import tuple_to_location, location_to_tuple
import math


def get_alpha_from_points(center_point, trgt_point):
    radius = center_point.distance(trgt_point)

    center_point = location_to_tuple(center_point)
    trgt_point = location_to_tuple(trgt_point)

    a = math.acos(trgt_point[0] / (center_point[0] + radius))

    return a


def get_point_by_alpha(alpha, center_point, trgt_point):
    radius = center_point.distance(trgt_point)
    center_point = location_to_tuple(center_point)
    trgt_point = location_to_tuple(trgt_point)

    x = center_point[0] + radius * math.cos(alpha)
    y = center_point[1] + radius * math.sin(alpha)

    tup = (int(x), int(y))

    return tuple_to_location(tup)

