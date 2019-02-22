from elf_kingdom import *

CASTLE_DEFENSE_RANGE = 2000
ICE_TO_LAVA_RATIO = 1


class Portals():
    """
    class for portals contain stuff like enemies around portal and other useful funcs
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

    def enemy_creatures_in_radius(self, radius, target):
        """
        :param radius: radius to count creatures at
        :param target: target to count creatures around
        :return: a tuple of possible creatures in the order (lava,elf,ice) or None of there are no creatures around
        """

        lava_giants, ice_trolls, elfs = 0, 0, 0
        for creature in self.game.get_enemy_creatures():
            if target.distance(creature) < radius:
                if creature.type == "Elf":
                    elfs += 1
                elif creature.type == "IceTroll":
                    ice_trolls += 1
                elif creature.type == "LavaGiant":
                    lava_giants += 1
        return lava_giants, elfs, ice_trolls

    def closest_portals_sorted(self, point):
        """
        note: used to be portal instead of point, may be better suited in a utility class / file
        :param point: point to form the list around
        :return: list of the closest portals to the given point
        """
        my_portals = self.game.get_my_portals()
        my_portals.sort(key=lambda x: x.location.distance(point), reverse=False)
        return my_portals

    def portals_defend_castle(self, mana_cap):
        """
        summon ice trolls according to a ratio of lava / ice in a certain range of the castle
        summon from the closest portal to the lava that isnt further from the castle than the lava
         note: might have to keep count of ice's being made to prevent spam? TBD
        :param mana_cap: mana limit we need to have to be able to attack
        :return: nothing
        """

        enemy_lava = self.game.get_enemy_lava_giants()
        count = 0
        lavas_inrange = []
        for lava in enemy_lava:  # get lavas in a certain range and put em in a list + count
            if self.game.get_my_castle().distance(lava) < CASTLE_DEFENSE_RANGE:
                lavas_inrange.append(lava)
                count += 1
        for ice in self.game.get_my_ice_trolls():  # for each lava subtract an ice so prevent spam
            if self.game.get_my_castle().distance(ice) < CASTLE_DEFENSE_RANGE:
                count -= 1
        closest_portals = self.closest_portals_sorted(self.game.get_my_castle())
        if len(closest_portals) == 0:  # exit if we have no defense portals
            return
        for i in range(
                count / ICE_TO_LAVA_RATIO):  # find the closest portal to lava giant that isnt further than the castle
            if self.game.get_my_mana() < mana_cap:
                return
            portal = closest_portals[0]
            for p in closest_portals[1:]:
                if (p.distance(lavas_inrange[i]) < portal.distance(lavas_inrange[i]) and p.distance(
                        self.game.get_my_castle()) < lavas_inrange[i].distance(
                        self.game.get_my_castle()) and p.can_summon_ice_troll()):
                    portal = p
                    portal.summon_ice_troll()

    def poratls_attack(self, attack_portals, mana_cap):
        """
        attack using an attack list( so the attack uses both lava and ice in a set order)
        :param attack_portals:  list of the portals used to attack
        :param mana_cap: mana limit we need to have to be able to attack
        :return: nothing
        """

        no_defense = False
        for portal in attack_portals:
            if self.game.get_my_mana() < mana_cap:  # exit if we dont have enough mana
                return

            enemies = self.enemy_creatures_in_radius(500, portal)  # get all enemies in radius
            if enemies[1] + enemies[2] == 0:  # if there are no ice or elves no need to summon our own ice
                no_defense = True

            if self.attackList.check_next() == "lava" or no_defense:  # check what is next to summon on attack list and summon it
                if portal.can_summon_lava_giant():
                    portal.summon_lava_giant()
                    self.attackList.get_next()
            if self.attackList.check_next() == "ice":
                if portal.can_summon_ice_troll():
                    portal.summon_ice_troll()
                    self.attackList.get_next()  # move the list index forward
            no_defense = False

    def summon_defense(self, portal):
        """
        simple func to summon defense, might be used using an "attack list" later as using lava to defend is viable.
        """
        if portal.can_summon_ice_troll():
            portal.summon_ice_troll()


class Attack_List():
    """
    class for the list of which creatures to spawn in which order, resets index every X turns
    """

    def __init__(self):
        self.a_list = ["lava", "lava", "ice"]
        self.location = 0
        self.turn_counter = 0

    def check_next(self):  # return next creature to spawn without changing index
        return self.a_list[self.location]

    def get_next(self):
        """
        changing the index to point to the next one on the list
        :return: next create to spawn
        """
        self.location += 1
        if self.location > len(self.a_list) - 1:  # reset location to start of list if spawned last creature
            self.location = 0
        self.turn_counter = 0
        return self.a_list[self.location - 1]

    def update_turns(self):
        """
        update turns passed since last call and reset location if too long passed
        :return: nuffin
        """
        if self.turn_counter > 6:
            self.location = 0
        self.turn_counter += 1
