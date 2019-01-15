from elf_kingdom import *


class Aggressive():
    def __init__(self, game, elfDict):
        self.game = game
        self.my_elves = list(elfDict.values())
        self.switch_sides = 1  # switching side on the normal line
        self.attack_portals = {}

    def do_aggressive(self):
        enemy_castle = self.game.get_enemy_castle()
        my_portals = self.game.get_my_portals()
        enemy_portals = self.game.get_enemy_portals()

        # update attack_portals
        for uid in self.attack_portals:
            if uid not in [portal.unique_id for portal in my_portals]:
                del self.attack_portals[uid]

        if len(self.attack_portals) < 2:
            for elf in self.my_elves[0:2]:  # build portals with all elves (atm builds with only 1):
                    location_to_move = elf.move_normal(enemy_castle.location, 750, self.switch_sides)
                    if elf.elf.location == location_to_move:  # check if elf is in designated location
                        if elf.elf.can_build_portal():  # if able to built portal
                            elf.elf.build_portal()
                            my_portals = self.game.get_my_portals()
                            self.attack_portals[my_portals[-1].unique_id] = my_portals[-1]
                        else:
                            elf.move(enemy_castle)
                    else:  # if not at location to build move to the location
                        elf.move(location_to_move)

                    # switches the side
                    if self.switch_sides == 1:
                        self.switch_sides = -1
                    else:
                        self.switch_sides = 1
        if enemy_portals:
            for elf in [elf for elf in self.my_elves if not elf.elf.already_acted]:
                min = self.game.rows + self.game.cols
                portal_to_attack = None
                for portal in enemy_portals:
                    if elf.elf.location.distance(portal.location) < min:
                        min = elf.elf.location.distance(portal.location)
                        portal_to_attack = portal

                if elf.elf.in_attack_range(portal_to_attack):
                    elf.elf.attack(portal_to_attack)
                else:
                    elf.elf.move_to(portal_to_attack)
