from elf_kingdom import *
from Start import Start
from Portals import Portals

__metaclass__ = type


class Infrastructure(Start):
    def __init__(self, game, elfDict, start_distance=800, radius=1000, ziging_distance=500):
        """
        the class builds portals systematicly along the game board
        :param game: game instence
        :param elfDict: elfDict
        :param start_distance: the distance the first portal will be built from our castle
        :param radius: the starting point and the just it will make each time it will place a portal
        :param ziging_distance: de delta of the ofset for the zigzag (+-)
        """
        self.game = game
        self.elfDict = elfDict
        self.radius = start_distance
        self.radius_delta = radius
        self.portal_locations = []
        self.built_portals = []
        self.not_built = []
        enemy_castle_loc = game.get_enemy_castle().location
        my_castle_loc = game.get_my_castle().location
        # if y delta is bigger the x delta:
        if (Location(enemy_castle_loc.row, 0).distance(Location(my_castle_loc.row, 0)) >
            Location(0, enemy_castle_loc.col).distance(Location(0, my_castle_loc.col))):
            self.zigzag_delta = [Location(0, ziging_distance), 1]
        else:
            self.zigzag_delta = [Location(ziging_distance, 0), 1]

    def update(self, game, elfDict):
        """
        updates the instence
        :param game: game instence
        :param elfDict: elfDict
        """
        self.game = game
        self.elfDict = elfDict
        self.update_portals(self.not_built)

    def update_portals(self, not_built):
        """
        updates self.built_portals
        :param not_built: a list of bortals that are yet builded
        """
        #try:
        built_loccations = list(self.portal_locations)
        print "before", built_loccations
        for location in not_built:
            built_loccations.remove(location)
        print "after", built_loccations
        built_portals = []
        for location in built_loccations:
            portal = Portals.portal_on_location(self.game, location)
            if portal:
                built_portals.append(portal)
        print "final", built_portals
        self.built_portals = built_portals
        #except Exception as msg:
        #    print msg, "update_portals"

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
        if self.zigzag_delta[1] > 0:
            target_location = enemy_castle.location.add(self.zigzag_delta[0])
        else:
            target_location = enemy_castle.location.subtract(self.zigzag_delta[0])
        start_location = my_castle.location.towards(target_location, self.radius)
        return self.get_object_ring_locations(game, my_castle.location, start_location, 1, 0)[0]
        #except Exception as msg:
        #    print msg, "get_next_location"

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
                    self.portal_locations.append(portals_sorted[0].location)
                    self.radius = game.get_my_castle().distance(portals_sorted[0]) + self.radius_delta + 50
                    next_location = next_location = self.get_next_location()

            self.radius += self.radius_delta
            self.zigzag_delta[1] *= -1
            self.portal_locations.append(next_location)
        #except Exception as msg:
        #    print msg, "add_infrastructure"

    def build_and_maintain(self):
        #try:
        locations = list(self.portal_locations)
        locations.reverse()
        self.not_built = self.build_structure_ring(self.game, locations, self.elfDict, 0)
        #except Exception as msg:
        #    print msg, "build_and_maintain"
#