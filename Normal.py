from elf_kingdom import *
from Portals import *

DEFENSE_MANA_CAP = 60  # limit to when we stop defending due to low mana
MANE_DRAIN_RANGE = 1500  # the distance of checking if there is a creature in range of the enemy castel we dont want to spawn from
LAVA_DRAIN_MANA_LIMIT = 100  # needs tweaking of course
ENEMY_LOW_MANA_ATTACK = 50   # the limit to become a more aggresive version of normal while considering to enemy mana
NORMAL_ATTACK_MODE_MANA_CAP = 100  # the limit to become a more aggresive version of normal while considering our mana

class Normal:

    def __init__(self, game, elfDict, attackDict):
        self.game = game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]
        self.switch_sides = -1  # switching side on the normal line
        self.attackDict = list(attackDict.values())
        self.dirDict = {}
        self.old_my_portals = []

        self.portals = Portals(game,game.get_my_portals())  # create an instance of portals object to summon etc.

    def do_normal(self, attack_portals, game, elfDict, attackDict, attacklist):
        """do everything that normal needs to do"""
        self.normal_update(game, elfDict, attackDict)

        self.build_portals() # build the flanking poratls, might need to be in an if with mana and our elfs taken into account

        self.normal_defense()

        if self.game.get_my_mana() >= LAVA_DRAIN_MANA_LIMIT:  # drain enemy mana if our mana is above our set limite
            self.normal_enemy_mana_drain(attack_portals)
        if self.game.get_enemy_mana() < ENEMY_LOW_MANA_ATTACK and self.game.get_my_mana() > NORMAL_ATTACK_MODE_MANA_CAP:
            self.normal_attack_lowMana(attacklist, attackDict)  # become more aggresive in normal if the enemy is low on
                                                                # on mana and we have enough.

    def normal_defense(self):
        if self.game.get_my_mana() > DEFENSE_MANA_CAP:
            self.portals.portals_defend_castle(DEFENSE_MANA_CAP)


    def normal_update(self, game, elfDict, attackDict):
        """Update everything that changes between turns or needs updating"""
        self.game = game  # update game
        self.my_elves = list(elfDict.values())  # update self.my_elves
        self.attackDict = list(attackDict.values())  # update self.attackDict
        self.game = game  # update self.game
        self.update_dirDict(elfDict)  # update dirDict
        self.portals.portals_update(game)  # update portals (the object)

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
        """send a lava golem if: there is no lava golem near the enemy castel already and no enemy ice troll"""
        lava, ice = True
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
                    lava, ice = True

    def normal_attack_lowMana(self, attack_portals):
        """" when enemy has low mana increese attack according to the attack list
          instead of the mana drain spam. """
        self.portals.poratls_attack(attack_portals, NORMAL_ATTACK_MODE_MANA_CAP)

    def build_portals(self):
        """
        build portals at the designated flanking points
        """
        enemy_castle = self.game.get_enemy_castle()
        flanking_elves = []
        distance_from_tgt = 900

        if len(self.attackDict) < 2:  # if there are not enough portals
            for elf in self.my_elves[0:2]:  # build portals with all elves (atm builds with only 1):
                location_to_move = elf.move_normal(enemy_castle.location, distance_from_tgt, self.dirDict[elf.elf.unique_id])
                if elf.elf.location.equals(location_to_move):  # check if elf is in designated location
                    if elf.elf.can_build_portal():  # if able to built portal
                        elf.elf.build_portal()
                        elf.was_building = True
                else:  # if not at location to build move to the location
                    elf.move(location_to_move)
                flanking_elves.append(elf)
        return flanking_elves

