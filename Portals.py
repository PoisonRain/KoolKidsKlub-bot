from elf_kingdom import *


class Portal():
    """
    class for portals contain stuff like enemies around portal and other usful funcs
    TO DO:
    enemy in radius
    """

    def __init__(self, game, portal):
        self.portal = portal

    def enemy_creatures_in_radius(self, game, radius):
        """
        (lava,elf,ice)
        return a a tuple containing how many of each enemy creatures in a tuple
        tuple form is: (lava,elf,ice) example: (5,1,0) in the given radius or None if
        there are none delete dis: Elf, IceTroll, LavaGiant
        """

        lava_giants, ice_trolls, elfs = 0, 0, 0
        for creature in game.get_enemy_creatures():
            if self.portal.distance(creature) < radius:
                if creature.type == "Elf":
                    elfs += 1
                elif creature.type == "IceTroll":
                    ice_trolls += 1
                elif creature.type == "LavaGiant":
                    lava_giants += 1
        return (lava_giants, elfs, ice_trolls)


def closest_portals_sorted(game, point, radius):
    my_portals = game.get_my_portals()
    my_portals.sort(key=lambda x: x.location.distance(point), reverse=False)

