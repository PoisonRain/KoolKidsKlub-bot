from BotObject import BotObject
from elf_kingdom import *

class Elf(object):
    def __init__(self, game, elf):
        self.game = game
        self.elf = elf

    def go_and_attack(self, other):
        if self.elf.is_alive():
            if self.elf.in_attack_range(other):
                self.elf.attack(other)
            else:
                self.elf.move_to(other)

    # basically a switch
    # num represents what enemy to attack, with no input it searches for any enemy
    def attack_closest_thing(self, num = -1):
        if num == 0:
            enemies_to_check = self.game.get_enemy_living_elves()
        elif num == 1:
            enemies_to_check = self.game.get_enemy_portals()
        elif num == 2:
            enemies_to_check = self.game.get_enemy_ice_trolls()
        elif num == 3:
            enemies_to_check = self.game.get_enemy_lava_giants()
        elif num == 4:
            enemies_to_check = self.game.get_enemy_creatures()
        elif num == -1:
            enemies_to_check = self.game.get_enemy_creatures()+self.game.get_enemy_living_elves()

        if self.elf.is_alive():
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

    def attack_closest_enemy(self):
        self.attack_closest_thing(4)

    def build_portal_at(self, loc):
        if self.elf.location == loc:
            if self.elf.can_build_portal():
                self.elf.build_portal()
        else:
            self.elf.move_to(loc)

