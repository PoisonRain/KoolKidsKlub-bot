from elf_kingdom import *


class Aggressive():
    def __init__(self, game, elfDict):
        self.game = game
        self.my_elves = list(elfDict.values())
        self.switch_sides = 1  # switching side on the normal line
        self.attack_portals = {}
        self.old_my_portals = []

    def do_aggressive(self, game, elfDict):
        self.my_elves = list(elfDict.values())  # self.update my_elves
        self.game = game  # update self.game
        enemy_castle = self.game.get_enemy_castle()
        my_portals = self.game.get_my_portals()
        enemy_portals = self.game.get_enemy_portals()
        attack_portal = None

        # update attack_portals
        for uid in self.attack_portals.keys():  # delete destroyed portals
            if uid not in [portal.unique_id for portal in my_portals]:
                del self.attack_portals[uid]

        for elf in self.my_elves:  # add new attack portals
            if elf.elf.is_building is False and elf.was_building is True:
                for portal in my_portals:
                    if portal not in self.old_my_portals:
                        attack_portal = portal
                        break
                if attack_portal is not None:
                    self.attack_portals[attack_portal.unique_id] = attack_portal
                elf.was_building = False

        if len(self.attack_portals) < 2:  # if there are not enough portals
            for elf in self.my_elves[0:2]:  # build portals with all elves (atm builds with only 1):
                location_to_move = elf.move_normal(enemy_castle.location, 750, self.switch_sides)
                if elf.elf.location == location_to_move:  # check if elf is in designated location
                    if elf.elf.can_build_portal():  # if able to built portal
                        elf.elf.build_portal()
                        elf.was_building = True
                else:  # if not at location to build move to the location
                    elf.move(location_to_move)
                # switches the side
                if self.switch_sides == 1:
                    self.switch_sides = -1
                else:
                    self.switch_sides = 1

        self.old_my_portals = my_portals  # update old portal list

        if enemy_portals:  # attack enemy portals
            for elf in [elf for elf in self.my_elves if not elf.elf.already_acted]:
                min = self.game.rows + self.game.cols
                portal_to_attack = None
                for portal in [portal for portal in enemy_portals if portal.location.distance(enemy_castle) < 2500]:
                    if elf.elf.location.distance(portal.location) < min:
                        min = elf.elf.location.distance(portal.location)
                        portal_to_attack = portal

                if elf.elf.in_attack_range(portal_to_attack):
                    elf.elf.attack(portal_to_attack)
                else:
                    elf.elf.move_to(portal_to_attack)

        elif elf.elf.in_attack_range(enemy_castle):  # if not able to attack enemy portals  attack enemy castle
            elf.elf.attack(enemy_castle)
        else:
            elf.elf.move_to(enemy_castle)

        for portal in self.attack_portals.values():  # spam lava giants
            if not portal.is_summoning:
                portal.summon_lava_giant()

