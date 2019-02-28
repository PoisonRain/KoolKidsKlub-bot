from elf_kingdom import *
from Start import Start
from Portals import Portals
from newMath import *

__metaclass__ = type


class Infrastructure(Start):
    def __init__(self, game, elfDict, start_distance=800, radius=1000, ziging_angle=30):
        """
        the class builds portals systematicly along the game board
        :param game: game instence
        :param elfDict: elfDict
        :param start_distance: the distance the first portal will be built from our castle
        :param radius: the starting point and the just it will make each time it will place a portal
        :param ziging_angle: the angle of the oofset for the zigzag (+-)
        """
        self.game = game
        self.elfDict = elfDict
        self.radius = start_distance
        self.radius_delta = radius
        self.ziging_angle = ziging_angle
        self.portal_locations = []
        self.built_portals = []
        self.not_built = []
        enemy_castle_loc = game.get_enemy_castle().location
        my_castle_loc = game.get_my_castle().location

    def update(self, game, elfDict):
        """
        updates the instence
        :param game: game instence
        :param elfDict: elfDict
        """
        self.game = game
        self.elfDict = elfDict
        self.update_portals(self.not_built)

    def remove_duplicates(self):
        for location in self.portal_locations:
            for location_other in self.portal_locations:
                if location is not location and location.equals(location_other):
                    self.portal_locations.remove(location_other)
        print self.portal_locations

    def update_portals(self, not_built):
        """
        updates self.built_portals
        :param not_built: a list of bortals that are yet builded
        """
        # try:
        built_loccations = list(self.portal_locations)
        for location in not_built:
            built_loccations.remove(location)
        built_portals = []
        for location in built_loccations:
            portal = Portals.portal_on_location(self.game, location)
            if portal:
                built_portals.append(portal)
        self.built_portals = built_portals  # except Exception as msg:  #    print msg, "update_portals"

    def get_next_location(self):
        """
        returns the next location to build a portals on
        (using self.radius, self.zigzag_delta MUST BE CHANGED changed outside)
        :return: next Location
        """
        ##try:
        game = self.game
        my_castle = game.get_my_castle()
        enemy_castle = game.get_enemy_castle()
        target_location = enemy_castle.location
        start_location = my_castle.location.towards(target_location, self.radius)

        # start_location = get_point_by_alpha(2, my_castle.location, start_location)
        alpha = get_alpha_from_points(my_castle.location, enemy_castle.location)
        print alpha
        if my_castle.location.row > game.rows / 2 and my_castle.location.col < game.cols / 2:
            alpha = 110
        else:
            alpha = 20
        print alpha
        location = self.get_object_ring_locations(game, my_castle.location, start_location, 1, 0, alpha)
        if len(location) > 0:
            return location[0]
        return location  # except Exception as msg:  #    print msg, "get_next_location"

    def add_infrastructure(self):
        """
        adds the next portal location to the self.portal_locations
        """
        ##try:
        if len(self.portal_locations) == len(self.built_portals):
            game = self.game
            next_location = self.get_next_location()
            portals_sorted = Portals.closest_portals_sorted(game, next_location)
            if len(portals_sorted) > 0:
                if next_location.distance(portals_sorted[0]) <= self.radius:
                    for location in self.portal_locations:
                        if location.equals(portals_sorted[0].location):
                            break
                    else:
                        self.portal_locations.append(portals_sorted[0].location)
                    self.radius = game.get_my_castle().distance(portals_sorted[0]) + self.radius_delta + 50
                    next_location = next_location = self.get_next_location()
            if self.radius < game.get_my_castle().distance(game.get_enemy_castle()) - self.radius_delta:
                self.radius += self.radius_delta
            self.ziging_angle *= -1
            self.portal_locations.append(next_location)
        self.remove_duplicates()  # except Exception as msg:  #    print msg, "add_infrastructure"

    def build_and_maintain(self):
        # try:
        locations = list(self.portal_locations)
        locations.reverse()
        self.not_built = self.build_structure_ring(self.game, locations, self.elfDict,
                                                   0)  # except Exception as msg:  #    print msg, "build_and_maintain"

    def get_object_ring_locations(self, game, axis, start_location, amount, object_type=0, alpha=20):
        """
        returns a list of where to place a semi ring of objects around a location
        :param game: the game instance
        :param axis: the axis (center) around where the object would be built
        :param start_location: the first location (will be moving to the left and right from this location)
        :param amount: the amount of location it will return
        :param object_type: 0 for portals, 1 for fountains
        :return: a list of objects around the start_location facing end location
        """
        target_points = []
        strt_alpha = get_alpha_from_points(axis, start_location)
        pos_alpha = strt_alpha + alpha
        neg_alpha = strt_alpha - alpha
        while len(
                target_points) < amount and pos_alpha < strt_alpha + 360 and neg_alpha > strt_alpha - 360:  # while the amount is not reached and the points didnt go a full circle

            pos_point = get_point_by_alpha(pos_alpha % 360, axis, start_location)
            if object_type == 0 and Portals.portal_on_location(game,
                                                               pos_point) or object_type == 1 and Normal.Normal.fountain_on_location(
                game, pos_point):
                target_points.append(pos_point)
                print 'pos_point: ' + str(pos_point)
                if len(target_points) >= amount:
                    break
            elif self.can_build_objects_by_list(game, pos_point, target_points, object_type):
                target_points.append(pos_point)
                print 'pos_point: ' + str(pos_point)
                if len(target_points) >= amount:
                    break

            pos_alpha += 5
            neg_point = get_point_by_alpha(neg_alpha % 360, axis, start_location)
            if object_type == 0 and Portals.portal_on_location(game,
                                                               neg_point) or object_type == 1 and Normal.Normal.fountain_on_location(
                game, neg_point):
                target_points.append(neg_point)
                print 'neg_point: ' + str(neg_point)
                if len(target_points) >= amount:
                    break
            elif self.can_build_objects_by_list(game, neg_point, target_points, object_type):
                target_points.append(neg_point)
                print 'neg_point: ' + str(neg_point)
                if len(target_points) >= amount:
                    break

            neg_alpha -= 5
        return target_points