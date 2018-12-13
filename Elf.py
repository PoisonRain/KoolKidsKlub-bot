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

    def attack_closest_thing(self, num):
        if num == 0:
            enemies_to_check = self.game.get_enemy_living_elves()
        elif num == 1:
            enemies_to_check = self.game.get_enemy_portals()
        elif num == 2:
            enemies_to_check =self.game.get_enemy_ice_trolls()
        elif num == 3:
            enemies_to_check = self.game.get_enemy_lava_giants()

        if enemies_to_check():
            closest_enemy = enemies_to_check[0]
            for enemy in enemies_to_check:
                if enemy.distance(self.elf) < enemies_to_check.distance(self.elf):
                    closest_enemy = enemy
        self.go_and_attack(closest_enemy)

    def attack_closest_elf(self):
        self.attack_closest_thing(0)

    def attack_closest_portal(self):
        self.attack_closest_thing(1)

    def attack_closest_ice_troll(self):
        self.attack_closest_thing(2)

    def attack_closest_lava_giant(self):
        self.attack_closest_thing(3)
