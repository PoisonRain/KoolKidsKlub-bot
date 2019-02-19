from elf_kingdom import *


class Rect:
    def __init__(self, top_left, bottom_right):
        """
        makes a rectangle
        :param top_left: top left point
        :param bottom_right: bottom right point
        """
        self.t_l = top_left
        self.b_l = Location(top_left.col, bottom_right.row)
        self.b_r = bottom_right
        self.t_r = Location(bottom_right.col, top_left.row)
        self.s = (self.b_l.row - self.t_l.row) * (self.t_r.col - self.t_l)

    def overlap(self, other):
        """
        check if two rectangles overlap
        :param other: other rectangle
        :return: True if they overlap else False
        """
        if other.t_r.col < self.t_l.col or self.t_r.col < other.t_l.col:  # if rectangle to the side
            return False
        if other.b_r.row > self.t_r.row or self.b_r.row > other.t_r.row:  # if rect above
            return False
        return True

    def is_safe(self, other, factor):
        """
        checks if a rectangle is safe to move trough
        :param other: other overlapping rectangle, the obstacle
        :param factor: the factor of "cover" needed for the rect to be considered unsafe (min 0 max 1)
        :return: True if safe else False
        """
        if self.t_l.col < other.t_l.col: is_to_left = True
        else: is_to_left = False
        if self.t_l.row < other.t_l.row: is_above = True
        else: is_above = False
        if is_above:  # create the overlapping part
            if is_to_left:
                top_left, bot_right = other.t_l, self.b_r
                area = Rect(top_left, bot_right)
            else:
                top_left, bot_right = Location(self.t_l.col, other.t_l.row), Location(other.t_l.col, self.b_l.row)
                area = Rect(top_left, bot_right)
        else:
            if is_to_left:
                top_left, bot_right = Location(other.t_l.col, self.t_l.row), Location(self.t_l.col, other.b_l.row)
                area = Rect(top_left, bot_right)
            else:
                top_left, bot_right = self.t_l, other.b_r
                area = Rect(top_left, bot_right)

        if self.s * factor > area.s:  # check if its safe
            return True
        return False

class BF:
    def __init__(self):
        pass