from elf_kingdom import *
from newMath import *
import Elf

locs = []


class Start:
    """ make a starting frame for the game, build starter portals, fountains etc
    for normal to maintain"""

    def __init__(self, game, elfDict, portal_amount=4, portal_range=1500, fountain_amount=2, fountain_range=None):
        """
        initiates start
        :param game: the game instance
        :param elfDict: the elfDict dictenary
        :param portal_amount: the amout of defence portals to be built
        :param portal_range: the radius the portals should be built from my_castle
        :param fountain_amount: the amout of fountains to be built
        :param fountain_range: the radius the fountains should be built from my_castle
        """
        if fountain_range is None:
            fountain_range = game.castle_size + game.mana_fountain_size + 100
        self.game = game
        self.elfDict = elfDict
        self.defense_portal_locs = self.get_structure_ring_locations(game, portal_range, portal_amount)
        self.fountain_locs = self.get_structure_ring_locations(game, fountain_range, fountain_amount)

    def get_structure_ring_locations(self, game, radius_from_castle, amount, structure_type=0):
        """returns a list of where to place a semi-ring of portals around our
        castle(degree shift from the line between both castles)

        :param game: the game instance
        :param radius_from_castle: how far away the points should be from the center point
        :param amount: how many points, the more points the denser theyll be
        :param structure_type: 0 = portal, 1 = fountain
        """
        start_location = game.get_my_castle().location  # change this to change the center point
        end_location = start_location.towards(game.get_enemy_castle().location,
                                              radius_from_castle)  # change this to change the line end point

        target_points = [end_location]  # list of locations to build portals in

        strt_alpha = get_alpha_from_points(start_location, end_location)
        pos_alpha = strt_alpha + 5
        neg_alpha = strt_alpha - 5

        while len(
                target_points) < amount and pos_alpha < strt_alpha + 360 and neg_alpha > strt_alpha - 360:  # while the amount is not reached and the points didnt go a full circle

            pos_point = get_point_by_alpha(pos_alpha % 360, start_location, end_location)
            if self.can_build_portals_by_list(game, pos_point, target_points):
                target_points.append(pos_point)
                print 'pos_point: ' + str(pos_point)
                if len(target_points) >= amount:
                    break

            pos_alpha += 5
            neg_point = get_point_by_alpha(neg_alpha % 360, start_location, end_location)
            if self.can_build_portals_by_list(game, neg_point, target_points):
                target_points.append(neg_point)
                print 'neg_point: ' + str(neg_point)
                if len(target_points) >= amount:
                    break

            neg_alpha -= 5

        print target_points
        return target_points

    @staticmethod
    def can_build_portal_at_updated(game, portal_location):
        """ pretty useless atm, here to fix the bugs with can_build_portal_at if they accure again"""
        return game.can_build_portal_at(
            portal_location)  # and 0 < portal_location.col < game.cols and 0 < portal_location < game.rows

    def can_build_portals_by_list(self, game, portal_location, future_portals_list):
        """ tests whether a portal would be able to be placed in a location, after the portals in the given
        list are built

        :param game: the game instance
        :param portal_location: the location to check for building a portal
        :param future_portals_list: the locations where portal will be built
        """
        if not self.can_build_portal_at_updated(game, portal_location):
            return False
        for other_location in future_portals_list:
            if portal_location.in_range(other_location,
                                        game.portal_size * 2):  # 100 is a random number to prevent them from being stuck together
                return False
        return True

    @staticmethod
    def build_structure_ring(locs, elfDict):
        """ take the locations(that were generated in get_structure_ring_locations() and trys to build the portals there
        using the closest elf to build each portal by order(technique might change in the future)
        if not built, returned in a list

        :param locs: the locations to build the portals
        :param elfDict: a dictionary of the Elf class instances
        :return: the locations that were not yet built in this turn, and should be used for the next run of the function
        """
        elfDict = dict(elfDict)
        locs = list(locs)

        for loc in locs:
            worker_elf = Elf.Elf.get_closest_elf(loc, elfDict)
            did_build = worker_elf.build_portal(loc)
            print did_build
            elfDict.pop(worker_elf.elf.unique_id, None)
            if did_build:
                locs.remove(loc)
            if not elfDict:
                break
        return locs

    @staticmethod
    def get_living_elves_dict(elfDict):
        "takes in a dict of elves and returns a dict of only the living ones (was used for debugging)"""
        newDict = {}
        print elfDict
        for elf_id in elfDict:
            print elf_id
            if elfDict[elf_id].elf.is_alive():
                newDict[elf_id] = elfDict[elf_id]
        return newDict

    def do_start(self, elfDict):
        """
        runs one turn in start
        :param elfDict: the elfDict dictanary
        :return: True if has finished building everything; else False
        """
        if self.defense_portal_locs is not []:
            self.defense_portal_locs = self.build_structure_ring(self.defense_portal_locs, elfDict)
            return False
        elif self.fountain_locs is not []:
            self.fountain_locs = self.build_structure_ring(self.fountain_locs, elfDict)
            return False
        return True
