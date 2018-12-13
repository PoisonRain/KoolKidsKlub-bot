import BotObject
from elf_kingdom import *


class Elf(BotObject):
    def __init__(self, game, elf):
        super.__init__(game)
        self.game = game
        self.elf = elf

    def go_and_attack(self, other):
        if self.elf.in_attack_range(other):
            self.elf.attack(other)
        else:
            self.elf.move_to(other)

    def attack_closest_elf(self):
        if self.game.get_enemy_living_elves():
            enemy_elves = self.game.get_enemy_living_elves()
            closest_elf = enemy_elves[0]
            for elf in enemy_elves:
                if elf.distance(self.elf) < closest_elf.distance(self.elf):
                    closest_elf = elf
            self.go_and_attack(closest_elf)

    def attack_closest_portal(self):
        if self.game.get_enemy_portals():
            enemy_portals = self.game.get_enemy_portals()
            closest_portal = enemy_portals[0]
            for portal in enemy_portals:
                if portal.distance(self.elf) < enemy_portals.distance(self.elf):
                    closest_portal = portal
            self.go_and_attack(closest_portal)

    def attack_closest_ice_troll(self):
        if self.game.get_enemy_ice_trolls():
            enemy_ice_trolls = self.game.get_enemy_ice_trolls()
            closest_ice_troll = enemy_ice_trolls[0]
            for ice_troll in enemy_ice_trolls:
                if ice_troll.distance(self.elf) < enemy_ice_trolls.distance(self.elf):
                    closest_ice_troll = ice_troll
            self.go_and_attack(closest_ice_troll)

    def attack_closest_lava_giant(self):
        if self.game.get_enemy_lava_giants():
            enemy_lava_giants = self.game.get_enemy_lava_giants()
            closest_lava_giant = enemy_lava_giants[0]
            for lava_giant in enemy_lava_giants:
                if lava_giant.distance(self.elf) < enemy_lava_giants.distance(self.elf):
                    closest_lava_giant = lava_giant
            self.go_and_attack(closest_lava_giant)
