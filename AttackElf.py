from elf_kingdom import *
from Elf import *
import GridSystem
# Attack elf:
# Needs to return a state:
# Low health retreating towards a portal and defending it
# High health attacking enemy portals
#
# If there are no portals built in the attack range: builds a portal FIRST PRIORITY
# If low on health (amount of hp) and has a portal in the attack range and we are winning by (x)
# -points and enemy has more then () ice trolls: gets close to the portal that is closest to the enemy castle and defends it
# Maintain two portals in the offensive half of the map (not necessarily in the attack range)
# Attack the closest enemy portal on the offensive half
# Attack closest enemy elf
# Attack enemy castle

class AttackElf(Elf):
    def __init__(self, game):
        super(AttackElf, self).__init__(game, game.get_all_my_elves()[1])
        self.game = game
        self.elf = game.get_all_my_elves()[1]

    def build_by_grid(self, x_start):
        loc_build = Location(0, 0)
        for y in range(1, 3):
            if GridSystem.GridSystem.check_build_in_grid(self.game, (x_start, y)):
                loc_build = GridSystem.GridSystem.check_build_in_grid(self.game, (x_start, y))
                break
        else:
            for y in range(1, 3):
                for x in range(x_start, 5):
                    if GridSystem.GridSystem.check_build_in_grid(self.game,(x, y)):
                        GridSystem.GridSystem.check_build_in_grid(self.game,(x, y))
                        break
                if loc_build != 0:
                    break
            else:
                for y in range(0, 4):
                    for x in range(x_start, 5):
                        if GridSystem.GridSystem.check_build_in_grid(self.game, (x, y)):
                            loc_build = GridSystem.GridSystem.check_build_in_grid(self.game, (x, y))
                            break
                    if loc_build != 0:
                        break
        return loc_build

    # return elf in defence(0) or offence(1) mode
    def handle(self):
        my_portals = self.game.get_my_portals()
        att_port_count = 0
        portals_2 = 0
        portals_3 = 0
        portals_4 = 0
        if my_portals:
            for portal in my_portals:
                if portal.location > self.game.rows / 2:
                    att_port_count += 1
                    for y in range(0, 4):
                        if GridSystem.GridSystem.is_portal_at_grid(self.game, portal, (2, y)):
                            portals_2 += 1
                        if GridSystem.GridSystem.is_portal_at_grid(self.game, portal, (3, y)):
                            portals_3 += 1
                        if GridSystem.GridSystem.is_portal_at_grid(self.game, portal, (4, y)):
                            portals_4 += 1

        #   0 1 2 3 4
        # 0 * * * * * 0
        # 1 * * * * * 1
        # 2 * * * * * 2
        # 3 * * * * * 3
        #   0 1 2 3 4

        if self.game.turn <= 50:
            if portals_2 < 2:
                loc_build = self.build_by_grid(2)
                super(AttackElf,self).build_portal_at(loc_build)
                return 1

        elif self.game.turn <= 200:
            if portals_3 < 1:
                loc_build = self.build_by_grid(3)
                super(AttackElf,self).build_portal_at(loc_build)
                return 1

        elif self.game.turn <= 300:
            if portals_4 < 1:
                loc_build = self.build_by_grid(4)
                super(AttackElf,self).build_portal_at(loc_build)
                return 1

        else:
            if portals_3 < 3:
                loc_build = self.build_by_grid(3)
                super(AttackElf,self).build_portal_at(loc_build)
                return 1








