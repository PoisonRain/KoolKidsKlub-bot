from elf_kingdom import *
from math import sqrt
from Start import Start
from Portals import Portals
from Elf import Elf


class Aggressive:
    """
    do aggressive things so basically zerg rush
    """

    def __init__(self, game, elfDict):
        self.game = game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]
        self.switch_sides = 1  # switching side on the normal line
        self.dirDict = {}
        self.old_my_portals = []
        self.portalutil = Start(game, elfDict)
        self.portal_locs = self.get_attack_portal_location(game)
        self.attack_portal_amount = 2
        self.not_built = []
        self.attack_portals = []

    def update_attack_portals(self, game):
        were_built_locs = list(self.portal_locs)
        for loc in self.not_built:
            try:
                were_built_locs.remove(loc)
            except:
                pass
        were_built_portals = []
        for loc in were_built_locs:
            portal = Portals.get_portal_on_location(game, loc)
            if portal is not False and portal not in were_built_portals:
                were_built_portals.append(portal)
        self.attack_portals += were_built_portals
        if len(self.attack_portals) > self.attack_portal_amount:
            self.attack_portals = self.attack_portals[-self.attack_portal_amount:]

    def get_aggresive_score(self, game):
        hp_delta = game.get_my_castle().current_health - game.get_enemy_castle().current_health
        attack_portals_built = len(self.attack_portals)
        enemy_mana = game.get_enemy_mana()
        elf_delta = len(game.get_my_living_elves()) - len(game.get_enemy_living_elves())
        # need to find best factors for performance, after testing.(jacob)
        hp_factor = 0.1
        attack_portals_factor = 1.5
        enemy_mana_factor = -0.02
        elf_factor = 2

        score = hp_delta * hp_factor + attack_portals_built * attack_portals_factor + enemy_mana * enemy_mana_factor + elf_delta * elf_factor
        print score
        return score

    def build_portals(self, game, elfDict):
        """
        build portals at the designated flanking points
        """
        enemy_castle = game.get_enemy_castle()
        my_portals = game.get_my_portals()
        self.attack_portal_amount = (game.get_myself().mana_per_turn * 3 // 40)
        if self.attack_portal_amount < 2:
            self.attack_portal_amount = 2
            if game.turn == 150 or game.turn == 50 or (game.turn > 150 and game.turn % 200 == 0):
                self.portal_locs = self.get_attack_portal_location(game, self.attack_portal_amount)
            if len([portal for portal in my_portals if portal.location.distance(enemy_castle.location) < 1500]) + len(
                [elf for elf in game.get_my_living_elves() if elf.is_building is True]) < self.attack_portal_amount:
                self.not_built = self.portalutil.build_structure_ring_flanking(game, self.portal_locs, elfDict)

    def attack(self, game):
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
                elf.flank(game, my_castle)

            elif len([portal for portal in enemy_portals if
                      portal.location.distance(enemy_castle) < 2500]) > 0:  # attack enemy portals
                min_dist = self.game.rows + self.game.cols
                portal_to_attack = None
                for portal in [portal for portal in enemy_portals if portal.location.distance(enemy_castle) < 2500]:
                    if elf.elf.location.distance(portal.location) < min_dist:
                        min_dist = elf.elf.location.distance(portal.location)
                        portal_to_attack = portal
                if portal_to_attack is not None and not elf.elf.already_acted:
                    if elf.elf.in_attack_range(portal_to_attack):
                        elf.elf.attack(portal_to_attack)
                    else:
                        elf.flank(game, portal_to_attack, (True, False, False))

            elif len([fountain for fountain in game.get_enemy_mana_fountains() if
                      fountain.location.distance(enemy_castle) < 2500]) > 0:  # attack enemy fountains
                min_dist = self.game.rows + self.game.cols
                fountain_to_attack = None
                for fountain in [fountain for fountain in game.get_enemy_mana_fountains() if
                                 fountain.location.distance(enemy_castle) < 2500]:
                    if elf.elf.location.distance(fountain.location) < min_dist:
                        min_dist = elf.elf.location.distance(fountain.location)
                        fountain_to_attack = fountain
                if fountain_to_attack is not None and not elf.elf.already_acted:
                    if elf.elf.in_attack_range(fountain_to_attack):
                        elf.elf.attack(fountain_to_attack)
                    else:
                        elf.flank(game, fountain_to_attack, (True, False, False))

            else:  # if has nothing to attack attack the enemy castle
                elf.attack(enemy_castle)

    def do_aggressive(self, game, elfDict, normal):
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]  # update self.my_elves
        enemy_castle = game.get_enemy_castle()
        castle_low_health = 16

        if enemy_castle.current_health <= castle_low_health:  # rush the enemy castle if its low health
            for elf in self.my_elves:
                if elf.elf.in_attack_range(enemy_castle):
                    elf.attack(enemy_castle)
                else:
                    elf.move_speed_invis(enemy_castle)
            self.my_elves = []
            normal.normal_update(game, elfDict)
            normal.normal_defense()

        self.build_portals(game, elfDict)  # i mean basically build flanking portals

        self.update_attack_portals(game)

        self.attack(game)

        for portal in self.attack_portals:  # spam lava giants while mana above 60
            if (game.get_my_mana() - 40) < 60:
                break
            if not portal.is_summoning:
                portal.summon_lava_giant()

    def get_attack_portal_location(self, game, amount=2):
        """
        :param game: game instence
        :param amount: the amout of attack portals
        :return: the locations on which you should build attack portals
        """
        radius = 800
        radius_delta = 100
        min_dist_efrom_enemy_portals = 300
        enemy_castle = game.get_enemy_castle()
        my_castle = game.get_my_castle()
        locs = []
        while len(locs) < amount:
            locs = self.portalutil.get_object_ring_locations(game, enemy_castle.location,
                                                             enemy_castle.location.towards(my_castle, radius), 100)
            print locs, "init locs"
            radius += radius_delta
            if len(locs) > amount * 3:
                locs = locs[amount * 3:]
                for loc in locs:
                    for portal in game.get_enemy_portals():
                        if portal.distance(loc) < min_dist_efrom_enemy_portals:
                            locs.remove(loc)
                            break
            print locs, "final locs"
        return locs[-2:]