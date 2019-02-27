from elf_kingdom import *

CASTLE_DEFENSE_RANGE = 2000
ICE_TO_LAVA_RATIO = 1
PORTAL_SELF_DEFENSE_RANGE = 800
PORTAL_HELP_DEFEND_RANGE = 200
DEFENSE_PORTAL_RANGE = 2000
CASTLE_DEFEND_FROM_ELFS = 800

class Portals:
    """
    class for portals contain stuff like enemies around portal and other useful funcs
    defend castle with mana cap, attack using given portal list + mana cap using attack list (ie: lava,lava,ice)
    """

    def __init__(self, game, portals):
        self.portals = portals
        self.game = game
        self.attackList = Attack_List()
        self.my_castle = game.get_my_castle()

    @staticmethod
    def get_portal_on_location(game, loc):
        """
        get the portal on the location
        :param game: the game instence
        :param loc: the location on which you check if the portal exists
        :return: the portal if it exists False else
        """
        portals = game.get_my_portals()
        for portal in portals:
            if portal.location.equals(loc):
                return portal
        return False

    def portals_update(self, game):
        self.game = game
        self.portals = game.get_my_portals()
        self.attackList.update_turns()
        self.my_castle = game.get_my_castle()

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

    def closest_enemy_to_portal(self, portal):
        """
        a func that returns the closest enemy to a portal and its distance (used because ice attack the closest enemy)
        :param portal: portal to find enemy and distance from
        :return: the portal, the closest enemy(regardless of its type) and the distance or false if there are no enemies
        """
        if len(self.game.get_enemy_creatures()) == 0:
            return False
        closest = self.game.get_enemy_creatures()[0]
        for enemy in self.game.get_enemy_creatures():
            if portal.distance(enemy) < portal.distance(closest):
                closest = enemy
        return portal, closest, portal.distance(closest)

    def portals_defend_castle(self, mana_cap):
        """
        defend the castle using defense portals ( defense portals are all portals in CASTLE_DEFENSE_RANGE of the castle)
        the defense gives priority to defend from lava golems and uses the closest portal to the closest enemy to the
        castle. doesnt spam ice - for each ice in range of defense one ice less will need to be spawned
        :param mana_cap: the limit of which defense will stop spawning
        :return: returns false if no defense was spawned
        """
        defense_portals, lavas, elfs = [], [], []
        ice_to_spawn = 0
        if self.game.get_my_mana() < mana_cap:
            return False
        for portal in self.game.get_my_portals():
            if portal.distance(self.my_castle) < CASTLE_DEFENSE_RANGE:
                defense_portals.append(self.closest_enemy_to_portal(portal))

        for elf in self.game.get_enemy_living_elves():
            if self.my_castle.distance(elf) < CASTLE_DEFENSE_RANGE:
                elfs.append(elf)
                ice_to_spawn += 1
        for lava in self.game.get_enemy_lava_giants():
            if self.my_castle.distance(lava) < CASTLE_DEFENSE_RANGE:
                lavas.append(lava)
                ice_to_spawn += 1
        for ice in self.game.get_my_ice_trolls():
            if self.my_castle.distance(ice) < CASTLE_DEFENSE_RANGE:
                ice_to_spawn -= 1
        elfs.sort(key=lambda x: x.location.distance(self.my_castle), reverse=False)
        lavas.sort(key=lambda x: x.location.distance(self.my_castle), reverse=False)
        lavas.extend(elfs)
        lavas.extend(elfs)
        enemies = lavas

        while self.game.get_my_mana() > mana_cap and len(defense_portals) > 0 and len(enemies) > 0 and ice_to_spawn > 0:

            portal = None
            for portals in defense_portals:
                if portals is not False and len(enemies) > 0 and len(defense_portals) > 0 and portals[1] == enemies[0]:
                    if portal is None:
                        portal = portals
                        enemies.remove(enemies[0])
                        defense_portals.remove(portal)
                    elif portal[2] > portals[2]:
                        portal = portals
                        enemies.remove(enemies[0])
                        defense_portals.remove(portal)
            if len(enemies) > 0:
                enemies.remove(enemies[0])
            if portal is not None:
                if self.summon_defense(portal[0]):
                    ice_to_spawn -= 1
            if self.game.get_my_mana() < mana_cap or len(defense_portals) == 0 or len(enemies) == 0:
                break

    def closest_portals_sorted(self, point):
        """
        note: used to be portal instead of point, may be better suited in a utility class / file
        :param point: point to form the list around
        :return: list of the closest portals to the given point
        """
        my_portals = self.game.get_my_portals()
        my_portals.sort(key=lambda x: x.location.distance(point), reverse=False)
        return my_portals

    def portals_around_map_object(self, point, range, portal_list):
        # docs is like this because the webkit gods DEMAND IT and whoever stands in their way will be a foribidden libary
        # get a list of portals around a given point from a given list of portals to allow using on both enemy and
        # friendly portals
        # :param point: location on the map to search around, needs to be map object
        # :param range: range of which to count portals around the point
        # :param portal_list: list of portals to check if they are around the given point in the given range
        # :return: list of friendly or enemy portals around the given point in the given range
        portals = []
        for portal in portal_list:
            if portal.distance(point) < range:
                portals.append(portal)
        return portals

    def defend_portal(self, portal, mana_cap):
        """
        defend the given portal with a set mana cap. the function also uses nearby portals if they are in
        range(PORTAL_HELP_DEFEND_RANGE)
        :param portal: portal to defend
        :param mana_cap: the limit of which defense can be spawned
        :return: return false if mana_cap is not met or if there are no elfs in range
        """
        elf_in_range = False
        count = 0
        if self.game.get_my_mana() < mana_cap:
            return False
        for elf in self.game.get_enemy_living_elves():  # for each enemy elf add 2 to count ( spawn more defense for elf)
            if portal.distance(elf) < PORTAL_SELF_DEFENSE_RANGE:
                count += 1
                elf_in_range = True
        if not elf_in_range:
            return False  # return if there are no elfs in range - so nuffin to defend from
        elf_in_range = False  # reset it for future use
        for ice in self.game.get_enemy_ice_trolls():  # for each enemy ice add 1 ice to count of how many defense to spawn
            if portal().distance(ice) < PORTAL_SELF_DEFENSE_RANGE:
                count += 1
        for ice in self.game.get_my_ice_trolls():  # for each friendly ice subtract 1 ice to prevent spam
            if portal().distance(ice) < PORTAL_SELF_DEFENSE_RANGE:
                count -= 1
        closest_portals = self.closest_portals_sorted(self.game.get_my_castle())
        print(str(count) + ' dddddddd')
        for i in range(int(count)):
            print(str(i) + 'print i and stuff idk')
            if self.game.get_my_mana() > mana_cap and closest_portals[i].distance(portal) < PORTAL_HELP_DEFEND_RANGE:
                # use all nearby portals(that are needed for the amount of enemies) to defend if they are within range
                if not self.summon_defense(portal):
                    print ' lol ree'
                    i -= 1

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
        return false if cant summon defense or true if summoned defense
        """
        if portal.can_summon_ice_troll():
            portal.summon_ice_troll()
            return True
        else:
            return False

    def dumb_castle_defense(self, mana_cap):
        ice_to_spawn = 0
        defense_portals = self.closest_portals_sorted(self.game.get_my_castle())
        for elf in self.game.get_enemy_living_elves():
            if self.my_castle.distance(elf) < CASTLE_DEFENSE_RANGE:
                ice_to_spawn += 1
        for lava in self.game.get_enemy_lava_giants():
            if self.my_castle.distance(lava) < CASTLE_DEFENSE_RANGE:
                ice_to_spawn += 1
        for ice in self.game.get_my_ice_trolls():
            if self.my_castle.distance(ice) < CASTLE_DEFENSE_RANGE:
                ice_to_spawn -= 1
        for portal in defense_portals:
            if portal.distance(self.game.get_my_castle()) < CASTLE_DEFENSE_RANGE and portal.can_summon_ice_troll() and self.game.get_my_mana() > mana_cap and ice_to_spawn > 0:
                portal.summon_ice_troll()

    def dumb_portal_defense(self, mana_cap):
        for poratl in self.game.get_my_portals():




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
