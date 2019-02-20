from elf_kingdom import *


class Rect:
    def __init__(self, top_left, bottom_right):
        """
        makes a rectangle
        :param top_left: top left point
        :param bottom_right: bottom right point
        """
        self.t_l = top_left
        self.b_l = Location(bottom_right.row, top_left.col)
        self.b_r = bottom_right
        self.t_r = Location(top_left.col, bottom_right.row)
        self.s = (self.b_l.row - self.t_l.row) * (self.t_l.col - self.t_r.col)

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

    def is_inside(self, point):
        """
        checks if the point is inside te rectangle
        :param point: Location
        :return: if Location is inside the rectangle return True else False
        """
        return self.overlap(Rect(point, point+Location(1, 1)))


class BF:
    def __init__(self, game, evo_rad, obstacles):
        """
        initiates a new obstacles object that can initiate a maneuver algorithm
        :param game: the game object
        :param evo_rad: the distance to keep yourself from the obstacles (beware as this number gets
                                                                        smaller the runtime gets higher)
        :param obstacles: a list of obstacle objects
        """
        self.game = game
        self.map_grid = []
        self.step = evo_rad
        print self.step+game.rows % self.step, self.step+game.rows, self.step, type(game.rows), type(self.step)
        new_row = [Rect(Location(0, 0), Location(self.step+game.rows % self.step, self.step+game.cols % self.step))]
        for col in range(new_row[0].t_l.col, game.cols+1 - self.step, self.step):
            new_row.append(Rect(Location(0, col), Location(self.step, col+self.step)))
        self.map_grid.append(new_row)
        for row in range(new_row[0].b_l.row, game.rows+1 - self.step, self.step):
            new_row = [Rect(Location(row, 0), Location(row+self.step, self.step+game.cols % self.step))]
            for col in range(new_row[0].t_l.col, game.cols+1 - self.step, self.step):
                 new_row.append(Rect(Location(row, col), Location(row+self.step, col+self.step)))
            self.map_grid.append(new_row)

        if obstacles is not None:
            self.obstacles = [obstacle.location for obstacle in obstacles]
        else: self.obstacles = None

    def where_is_point(self, point):
        """
        returns the grid location of the point
        :param point: Location to check
        :return: tuple (row, col) of the grid location
        """
        # could possibly overshoot if so need additional checks
        col = (point.col+self.game.cols % self.step) // self.step
        row = (point.row+self.game.cols % self.step) // self.step
        tup = (row, col)
        return tup

    def is_valid(self, path, factor):
        """
        checks if the move is valid or not
        :param path: a list of moves (up: U, down: D, left: L, right: R)
        :param factor: the factor of "cover" needed for the rect to be considered unsafe (min 0 max 1)
        :return: True if is valid else False
        """
        # may need more edge cases
        path = self.path_to_tuple(path)
        return self.map_grid[path[0]][path[1]].is_safe(factor)

    def path_to_tuple(self, path):
        """
        converts a path to tuple
        :param path: a list of moves (up: U, down: D, left: L, right: R)
        :return: tuple location on the map_grid of the path
        """
        tup = ()
        for move in path:
            if move == "U":
                tup[0] += 1
            elif move == "D":
                tup[0] -= 1
            elif move == "L":
                tup[1] -= 1
            else:
                tup[1] += 1
        return tup

    def maneuver(self, elf, dest, factor, move=True):
        """
        initiates the maneuver algorithm
        :param Elf: the Elf object that is to be moved
        :param dest: the destination to be walked to
        :param move: if set to False returns the location if set to True moves the elf
        :return: if move set to False returns the location you would be moved to
        """
        dest_grid = self.where_is_point(dest)
        path_queue = []
        path = []

        def done():
            if self.path_to_tuple(path_queue[-1]) == dest_grid:
                return True
            else: return False

        def add_moves_if_valid():
            path = path_queue.pop(0)
            u_path = path[:].append(["U"])
            d_path = path[:].append(["D"])
            l_path = path[:].append(["L"])
            r_path = path[:].append(["R"])
            all_paths = [u_path, d_path, l_path, r_path]
            for path in all_paths:
                if not done() and self.is_valid(path):
                    path_queue.append(path)

        while not done():
            add_moves_if_valid()

        final_move = self.path_to_tuple(path_queue[0])
        final_rect = self.map_grid[final_move[0]][final_move[1]]

        t_r, t_l, b_l, b_r = final_rect.t_r, final_rect.t_l, final_rect.b_l, final_rect.b_r
        points = [t_l, b_r, b_l]
        min = (t_r, t_r.distance(dest))
        for location in points:
            distance = location.distance(dest)
            if distance < min[1]:
                min = (location, location.distance(dest))

        if move:
            elf.elf.move_towords(min[0])
        else:
            return min[0]