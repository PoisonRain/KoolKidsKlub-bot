from elf_kingdom import *
CASTLE_DEFENSE_RANGE = 2000
ICE_TO_LAVA_RATIO = 1

class Portals():
    """
    class for portals contain stuff like enemies around portal and other usful funcs
    defend castle with mana cap, attack using given portal list + mana cap using attack list (ie: lava,lava,ice)
    """

    def __init__(self, game, portals):
        self.portals = portals
        self.game = game
        self.attackList = Attack_List()

    def portals_update(self, game):
        self.game = game
        self.portals = game.get_my_portals()
        self.attackList.update_turns()

    def enemy_creatures_in_radius(self, radius, portal):
        """
        (lava,elf,ice)
        return a a tuple containing how many of each enemy creatures in a tuple
        tuple form is: (lava,elf,ice) example: (5,1,0) in the given radius or None if
        there are none
        """

        lava_giants, ice_trolls, elfs = 0, 0, 0
        for creature in self.game.get_enemy_creatures():
            if portal.distance(creature) < radius:
                if creature.type == "Elf":
                    elfs += 1
                elif creature.type == "IceTroll":
                    ice_trolls += 1
                elif creature.type == "LavaGiant":
                    lava_giants += 1
        return (lava_giants, elfs, ice_trolls)

    def closest_portals_sorted(self, point):
        """return a sorted list of the portals closest to the given point"""
        my_portals = self.game.get_my_portals()
        my_portals.sort(key=lambda x: x.location.distance(point), reverse=False)
        return my_portals

    def portals_defend_castle(self, mana_cap):
        """ summon ice trolls according to a ratio of lava / ice in a certain range of the castle
        summon from the closest portal to the lava that isnt further from the castle than the lava
         note: might have to keep count of ice's being made to prevent spam? TBD"""

        enemy_lava = self.game.get_enemy_lava_giants()
        count = 0
        lavas_inrange = []
        for lava in enemy_lava: # get lavas in a certain range and put em in a list + count
            if self.game.get_my_castle().distance(lava) < CASTLE_DEFENSE_RANGE:
                lavas_inrange.append(lava)
                count += 1
        for ice in self.game.get_my_ice_trolls(): # for each lava subtract an ice so prevent spam
            if self.game.get_my_castle().distance(ice) < CASTLE_DEFENSE_RANGE:
                count -= 1
        closest_portals = self.closest_portals_sorted(self.game.get_my_castle())
        if len(closest_portals) == 0: # exit if we have no defense portals
            return
        for i in range(count/ICE_TO_LAVA_RATIO): # find the closest portal to lava giant that isnt further than the castle
            if self.game.get_my_mana() < mana_cap:
                return
            portal = closest_portals[0]
            for p in closest_portals[1:]:
                if (p.distance(lavas_inrange[i]) < portal.distance(lava[i])
                        and p.distance(self.game.get_my_castle()) < lavas_inrange[i].distance(self.game.get_my_castle()) and p.can_summon_ice_troll()):
                    portal = p
            portal.summon_ice_troll()

    def poratls_attack(self, attack_portals, mana_cap):
        """attack using an attack list( so the attack uses both lava and ice in a set order)"""
        for portal in attack_portals:
            if self.game.get_my_mana() < mana_cap:  # exit if we dont have enough mana
                return
            if self.attackList.check_next() == "lava":  # check what is next to summon on attack list and summon it
                if portal.can_summon_lava_giant():
                    portal.summon_lava_giant()
                    self.attackList.get_next()
            if self.attackList.check_next() == "ice":
                if portal.can_summon_ice_troll():
                    portal.summon_ice_troll()
                    self.attackList.get_next()  # move the list index forward


class Attack_List():
    """func for the list of which creatures to spawn in which order, restets index every X turns"""

    def __init__(self):
        self.a_list = ["lava", "lava", "ice"]
        self.location = 0
        self.turn_counter = 0

    def check_next(self):  # return next creature to spawn without changing index
        return self.a_list[self.location]

    def get_next(self):
        """ return next creature to spawn + changing the index to point to the next one on the list"""
        self.location += 1
        if self.location > len(self.a_list):  # reset location to start of list if spawned last creature
            self.location = 0
        self.turn_counter = 0
        return self.a_list[self.location - 1]

    def update_turns(self):
        """update turns passed since last call and reset location if too long passed"""
        if self.turn_counter > 6:
            self.location = 0
        self.turn_counter += 1
