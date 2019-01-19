from elf_kingdom import *
from math import *


class Aggressive:
    """
    do aggressive things so basically zerg rush
    """
    def __init__(self, game, elfDict, attackDict):
        self.game = game
        self.my_elves = list(elfDict.values())
        self.switch_sides = -1  # switching side on the normal line
        self.attackDict = list(attackDict.values())
        self.dirDict = {}
        self.old_my_portals = []


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

    def attack(self):
        """
        attacks or runs away with the elves
        """
        for elf in [elf for elf in self.my_elves if not elf.elf.already_acted]:
            enemy_close = False
            my_castle = self.game.get_my_castle()
            enemy_elves = self.game.get_enemy_living_elves()
            enemy_trolls = self.game.get_enemy_ice_trolls()
            enemy_portals = self.game.get_enemy_portals()
            enemy_castle = self.game.get_enemy_castle()
            enemy_is_close_dist = 350
            # check for nulls:
            if enemy_elves is None:
                enemy_elves = []
            if enemy_trolls is None:
                enemy_trolls = []
            if enemy_portals is None:
                enemy_portals = []

            for enemy in enemy_trolls:  # check if there are close enemies
                if elf.elf.location.distance(enemy) < enemy_is_close_dist:
                    enemy_close = True
                    break
            if not enemy_close:
                for enemy in enemy_elves:  # check if there are close enemies
                    if elf.elf.location.distance(enemy) < enemy_is_close_dist:
                        enemy_close = True
                        break

            if elf.elf.current_health < 9 and enemy_close:  # if you pussy run
                elf.elf.move_to(my_castle)

            elif len([portal for portal in enemy_portals if portal.location.distance(enemy_castle) < 2500]) > 0:  # attack enemy portals
                    min = self.game.rows + self.game.cols
                    portal_to_attack = None
                    for portal in [portal for portal in enemy_portals if portal.location.distance(enemy_castle) < 2500]:
                        if elf.elf.location.distance(portal.location) < min:
                            min = elf.elf.location.distance(portal.location)
                            portal_to_attack = portal
                    if portal_to_attack is not None:
                        elf.attack(portal_to_attack)

            else:  # if has nothing to attack attack the enemy castle
                elf.attack(enemy_castle)

    def do_aggressive(self, game, elfDict, attackDict):
        self.my_elves = list(elfDict.values())  # update self.my_elves
        self.attackDict = list(attackDict.values())  # update self.attackDict
        self.game = game  # update self.game
        self.update_dirDict(elfDict)  # update dirDict

        flanking_elves = self.build_portals()  # i mean basically build flanking portals

        self.attack()

        for portal in self.attackDict:  # spam lava giants
            if not portal.is_summoning:
                portal.summon_lava_giant()

        return flanking_elves

