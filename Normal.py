from elf_kingdom import *
from Portals import *
from newMath import move_point_by_angle

# constants
DEFENSE_MANA_CAP = 60  # limit to when we stop defending due to low mana
MANE_DRAIN_RANGE = 1500  # the distance of checking if there is a creature in range of the enemy castel we dont want to spawn from
LAVA_DRAIN_MANA_LIMIT = 100  # needs tweaking of course
ENEMY_LOW_MANA_ATTACK = 50  # the limit to become a more aggresive version of normal while considering to enemy mana
NORMAL_ATTACK_MODE_MANA_CAP = 100  # the limit to become a more aggresive version of normal while considering our mana
CASTLE_DEFENSE = 5000  # range of which elfs will try to destroy enemy portals, TODO: make it using range of map
ELF_DEFENSE_BOOST_RANGE = 400  # range of attack targets portal will spawn defense to help the elfs
ELF_DEFENSE_BOOST_MANA = 100  # mana cap to spawn defense to help elfs attack
ENEMY_FOUNTAIN_NO_PORTALS_RANGE = 400  # range of an enemy fountain of which there can be no enemy portals for us to


# attack it( on elf's way back to base)


class Normal:
    """
     the normal mode, theoreticlly the mode we will be in most of the time. aims to reduce enemy mana and maintain
     our attack portals and portals in general
     TODO: maintain / build mana fountains
     TODO: add uses for spells
     """

    def __init__(self, game, elfDict, attackDict, aggressive):
        """

        :param aggressive: instance of aggressive mode, used to make attack portals
        :var portals: instance of portals class, used to control portals + some utilities functions
        """
        self.game = game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]
        self.switch_sides = -1  # switching side on the normal line
        self.attackDict = list(attackDict.values())
        self.dirDict = {}
        self.old_my_portals = []
        self.aggressive = aggressive
        self.my_castle = game.get_my_castle()

        self.portals = Portals(game, game.get_my_portals())  # create an instance of portals object to summon etc.

    @staticmethod
    def portal_on_location(game, loc):
        """
        get a location and checks if there is a portal(friendly) there
        :param game: the game instance
        :param loc: the location on which the portal(friendly) should be
        :return: True if there is a portal there, False else
        """
        my_portals = game.get_my_portals()
        for portal in my_portals:
            if portal.location.equals(loc):
                return True
        return False

    @staticmethod
    def get_closest_elf(game, loc, elfDict):
        """
        returns the key of the closest elf to the designated location
        :param game: game instance
        :param loc: designated location
        :param elfDict: elfDict..
        :return: the key of the closest elf
        """
        min_dist = elfDict.values()[0].elf.distance(loc)
        elfKey = elfDict.keys()[0]
        for key in elfDict.keys():
            if elfDict[key].elf.distance(loc) < min_dist:
                min_dist = elfDict[key].elf.distance(loc)
                elfKey = key
        return elfKey

    def maintain_defence(self, game, elfDict):
        """
        build portals at the designated locations
        :param game: the game instance
        :param elfDict: elfDict
        """

        my_castle = game.get_my_castle().location
        enemy_castle = game.get_enemy_castle().location
        middle_portal = my_castle.towards(enemy_castle, 500)
        left_portal = move_point_by_angle(my_castle, middle_portal, -50)
        right_portal = move_point_by_angle(my_castle, middle_portal, 50)
        if len(elfDict) > 0:
            if not self.portal_on_location(game, middle_portal):
                elf = elfDict[self.get_closest_elf(game, middle_portal, elfDict)]
                elf.build_portal(middle_portal)
                print
                ' cock sucker'
            if not self.portal_on_location(game, left_portal):
                elf = elfDict[self.get_closest_elf(game, left_portal, elfDict)]
                elf.build_portal(left_portal)
                print
                ' cock sucker'
            if not self.portal_on_location(game, right_portal):
                elf = elfDict[self.get_closest_elf(game, right_portal, elfDict)]
                elf.build_portal(right_portal)

    def do_normal(self, game, elfDict, attackDict):
        """
        updates normal
        does all of what the normal mode is meant to do, defend, drain mana, maintain portals.
        :param elfDict: usable elfs
        :param attackDict: attack portals
        :return: elfs being used
        """
        self.normal_update(game, elfDict, attackDict)

        self.maintain_defence(game, elfDict)  # doesnt work yet - eyal do it

        flanking_elves = self.build_portals(elfDict, attackDict)  # build the flanking poratls, might need to be in
        # an if with mana and our elfs taken into account
        self.normal_elf_defendcastle(elfDict)
        self.normal_defense()  # defend the castle (if there are enemies in range)

        print
        attackDict
        if self.game.get_my_mana() >= LAVA_DRAIN_MANA_LIMIT:  # drain enemy mana if our mana is above our set limite
            self.normal_enemy_mana_drain(self.attackDict)
        if self.game.get_enemy_mana() < ENEMY_LOW_MANA_ATTACK and self.game.get_my_mana() > NORMAL_ATTACK_MODE_MANA_CAP:
            self.normal_attack_lowMana(self.attackDict)  # become more aggresive in normal if the enemy is low on
            # on mana and we have enough.

        self.normal_elf_defendcastle(elfDict)

        return flanking_elves

    def normal_defense(self):
        """
        defend the castle if are above the mana cap using the Portals class
        """
        if self.game.get_my_mana() > DEFENSE_MANA_CAP:
            self.portals.portals_defend_castle(DEFENSE_MANA_CAP)

    def normal_update(self, game, elfDict, attackDict):
        """
        Update everything that changes between turns or needs updating
        :param game: updated instance of game
        :param elfDict: usable elfs
        :param attackDict: attack portals
        """
        self.game = game  # update game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]  # update self.my_elves
        self.attackDict = list(attackDict.values())  # update self.attackDict
        self.game = game  # update self.game
        self.update_dirDict(elfDict)  # update dirDict
        self.portals.portals_update(game)  # update portals (the object)
        self.my_castle = game.get_my_castle()

    def update_dirDict(self, elfDict):
        """
        gets updated elfDict checks for new entries gives them in an altering manner a direction to go
        and deletes dead elves from the dictionary
        """
        for uid in elfDict.keys():
            if uid not in self.dirDict:
                self.dirDict[uid] = self.switch_sides
                if self.switch_sides == 1:
                    self.switch_sides = -1
                else:
                    self.switch_sides = 1

    def normal_enemy_mana_drain(self, attack_portals):
        """
        send a lava golem if: there is no lava golem near the enemy castel already and no enemy ice troll
        drains enemy mana
        :param attack_portals: portals used to attack
        """
        lava = ice = True
        for creature in self.game.get_my_lava_giants():
            if creature.distance(self.game.get_enemy_castle()) < MANE_DRAIN_RANGE:
                lava = False
        for creature in self.game.get_enemy_ice_trolls():
            if creature.distance(self.game.get_enemy_castle()) < MANE_DRAIN_RANGE:
                ice = False
        if (ice == False and lava == False):
            for portal in attack_portals:
                if portal.can_summon_lava_giant():
                    portal.summon_lava_giant()
                    lava = ice = True

    def normal_attack_lowMana(self, attack_portals):
        """
        when enemy has low mana increese attack according to the attack list
        instead of the mana drain spam.
        :param attack_portals: portals used to attack
        """
        self.portals.poratls_attack(attack_portals, NORMAL_ATTACK_MODE_MANA_CAP)

    def build_portals(self, elfDict, attackDict):
        """
        build portals at the designated flanking points using aggressive
        :param elfDict: usable elfs
        :param attackDict: portals used to attack
        :return: elfs being used
        """
        flanking_elves = self.aggressive.outside_aggressive_buildportals(self.game, elfDict,
                                                                         attackDict)  # game, elfDict, attackDict
        return flanking_elves
        # enemy_castle = self.game.get_enemy_castle()
        # flanking_elves = []
        # distance_from_tgt = 900
        #
        # if len(self.attackDict) < 2:  # if there are not enough portals
        #     for elf in self.my_elves[0:2]:  # build portals with all elves (atm builds with only 1):
        #         location_to_move = elf.move_normal(enemy_castle.location, distance_from_tgt, self.dirDict[elf.elf.unique_id])
        #         if elf.elf.location.equals(location_to_move):  # check if elf is in designated location
        #             if elf.elf.can_build_portal():  # if able to built portal
        #                 elf.elf.build_portal()
        #                 elf.was_building = True
        #         else:  # if not at location to build move to the location
        #             elf.move(location_to_move)
        #         flanking_elves.append(elf)
        # return flanking_elves

    def normal_elf_defendcastle(self, elfDict):
        """
        use the elfs to defend the castle, break portals and fountains near the castle, use both elfs to destroy faster
        and take less damage logic: normal is all about preparing to attack we want elfs to have their health
        if there are nearby portals and enemies to defend the elfs from the portal will summon defense, currently
        only one (due to change need to be tested in game and see how it is)
        :param elfDict:
        :return:
        """
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]  # update self.my_elves
        enemy_poratls = self.game.get_enemy_portals()
        enemy_fountains = self.game.get_enemy_mana_fountains()
        if self.game.get_enemy_portals() is None:
            enemy_poratls = []
        if self.game.get_enemy_mana_fountains() is None:
            enemy_fountains = []
        targets = self.sorted_map_objects(self.game.get_my_castle(), (enemy_fountains, enemy_poratls))  # get a sorted
        # list of targets, closest to the castle, can append whatever priority you want after sorting to have certain
        # buildings higher priority
        for target in targets:
            if self.my_castle.distance(target) < CASTLE_DEFENSE:
                for i in range(2):  # use 2 elfs (assuming they add more elfs in the future)
                    if target is not None:
                        if len(self.my_elves) > i and not self.my_elves[i].elf.already_acted:
                            fountains_on_path = self.get_fountains_on_path(self.my_elves[i])
                            print
                            fountains_on_path
                            if len(fountains_on_path) > 0:
                                print
                                'lol wtfffff'
                                self.my_elves[i].attack(fountains_on_path[0])
                            else:
                                self.my_elves[i].attack(target)
                            if self.game.get_my_mana() > ELF_DEFENSE_BOOST_MANA:  # summon defense to help the elfs if there is a need
                                defense_portals = self.portals.closest_portals_sorted(target)
                                if len(defense_portals) > 0 and defense_portals[0].distance(
                                        target) < ELF_DEFENSE_BOOST_RANGE:
                                    enemies = self.portals.enemy_creatures_in_radius(400, target)
                                    if enemies[1] > 0 or enemies[2] > 0:
                                        self.portals.summon_defense(defense_portals[0])

    def sorted_map_objects(self, point, objects):
        """
        get a tuple of lists of map objects and a point and sort them closest to point first
        :param point: location on the map to sort from, needs to be map object
        :param objects: map objects tuple of lists
        :return: sorted_objects the sorted list of map object closest being first
        """
        # print objects
        # print len(objects)
        if isinstance(objects, list):
            sorted_objects = objects
        else:
            sorted_objects = [j for i in objects for j in i]
        if len(sorted_objects) > 0:
            sorted_objects.sort(key=lambda x: x.distance(point.get_location()), reverse=False)
        return sorted_objects

    def get_fountains_on_path(self, elf):
        fountains = []
        d = (self.game.get_enemy_mana_fountains())
        for fountain in self.sorted_map_objects(elf.elf, d):
            if fountain.distance(self.game.get_my_castle()) < elf.elf.distance(self.game.get_my_castle()) and len(
                    self.portals.portals_around_map_object(fountain, ENEMY_FOUNTAIN_NO_PORTALS_RANGE,
                                                           self.game.get_enemy_portals())) == 0:
                fountains.append(fountain)
        print
        'dddddd'
        print
        fountains
        return fountains



