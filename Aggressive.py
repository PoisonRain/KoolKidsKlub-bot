from elf_kingdom import *


class Aggressive:
    """
    do aggressive things so basically zerg rush
    """
    def __init__(self, game, elfDict, attackDict):
        self.game = game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]
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
        def closest_attacl_portal(elf):
            elf = elf.elf
            min = self.game.rows = self.game.cols
            for portal in self.attackDict:
                dist = elf.location.distance(portal)
                if dist < min:
                    min = dist
            return min

        enemy_castle = self.game.get_enemy_castle()
        flanking_elves = []
        attack_portal_amount = 2
        amount_of_assigned_elves = attack_portal_amount - len(self.attackDict)
        distance_from_tgt = 900
        if len(self.my_elves) < amount_of_assigned_elves:  # check if the amount of elves i want to assign is to big
            amount_of_assigned_elves = len(self.my_elves)
        elves_by_distance = sorted(self.my_elves, key=closest_attacl_portal, reverse=True)

        if len(self.attackDict) < attack_portal_amount:  # if there are not enough portals
            for elf in elves_by_distance[0:amount_of_assigned_elves]:  # build portals with all assigned elves
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
            enemy_elves = self.game.get_enemy_living_elves()
            enemy_trolls = self.game.get_enemy_ice_trolls()
            enemy_portals = self.game.get_enemy_portals()
            enemy_castle = self.game.get_enemy_castle()
            my_castle = self.game.get_my_castle()
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
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]  # update self.my_elves
        self.attackDict = list(attackDict.values())  # update self.attackDict
        self.game = game  # update self.game
        self.update_dirDict(elfDict)  # update dirDict

        flanking_elves = self.build_portals()  # i mean basically build flanking portals

        self.attack()

        for portal in self.attackDict:  # spam lava giants while mana above 60
            if (game.get_my_mana() - 40) < 60:
                break
            if not portal.is_summoning:
                portal.summon_lava_giant()

        return flanking_elves

