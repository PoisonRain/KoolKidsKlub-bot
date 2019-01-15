"""
elf class n shit
"""

from elf_kingdom import *


class Elf:
    def __init__(self, game, elf):
        self.game = game
        self.elf = elf
        # used to remember where the user designated the elf to go last turn and where he actually went:
        self.moving_to = (Location(0,0), Location(0,0))  # (user input, elf target)

    def move(self, dis):
        pass

    def move_normal(self, tgt, dist, dir=1, srt=None):
        """
        the elf (s) moves to a or b from :srt             a
        where e is designated point :tgt      -->   s-----e
        the distance from e to a|b is :dist               b

        :param tgt: The point where you make a normal line to you
        :param dist: The distance you want to go on the perpendicular line
        :param dir: The direction you prefer to go in (up, left) = 1, (down, right) = -1; default is 1
        :param srt: Optional parameter, starting point; if not set is default to game.get_enemy_castle().location
        :return: true if was able to move the elf false other wise

        """
        if self.moving_to[0] == tgt:  # if the elf has the same target go to the previously calculated location
            self.move(self.moving_to[1])
            return
        if srt is None:
            srt = self.game.get_enemy_castle().location

        def second_degree(a, b, c):
            # :return: 2 solution of a second degree equation
            solve1 = (-b-((b*b)-(4*a*c)))/(2*a)
            solve2 = (-b+((b*b)-(4*a*c)))/(2*a)
            return solve1, solve2

        # tgt x and b:
        xt = tgt.row
        yt = tgt.col

        # y-y1 = m(x-x1)=
        m = ((tgt.row - srt.row) // (tgt.col - srt.col)) // -1
        b = (m*xt)+yt

        # -b+-sqrt(b^2-4ac)/2a:
        ax = 2*(m*m)
        bx = (2*xt*m)-(2*m*(yt-b))
        c = ((xt*xt) + ((yt-b)**2)) - (dist*dist)

        # final solve for the 2 points:
        x1, x2 = second_degree(ax, bx, c)
        y1 = (m*x1) + b
        y2 = (m*x2) + b

        pointA = Location(x1, y1)
        pointB = Location(x2, y2)
        print "pointA: "+pointA, " pointA: "+pointB
        return
