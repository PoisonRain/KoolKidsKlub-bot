from elf_kingdom import *
from math import sqrt


class Aggressive:
    """
    do aggressive things so basically zerg rush
    """

    def __init__(self, game, elfDict, attackDict):
        self.game = game
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]
        self.switch_sides = 1  # switching side on the normal line
        self.attackDict = list(attackDict.values())
        self.dirDict = {}
        self.old_my_portals = []

    def update_dirDict(self, elfDict):
        """
        gets updated elfDict checks for new entries gives them in an altering manner a direction to go
        and deletes dead elves from the dictionary
        """
        for uid in elfDict.keys():  # add new
            if uid not in self.dirDict:
                self.dirDict[uid] = self.switch_sides
                self.switch_sides *= -1

        for uid in self.dirDict.keys():  # delete old
            if uid not in elfDict:
                del self.dirDict[uid]

    def get_aggresive_score(self, game):
        hp_delta = game.get_my_castle().current_health - game.get_enemy_castle().current_health
        attack_portals_built = self.attack_portals_built(game)
        enemy_mana = game.get_enemy_mana()
        # need to find best factors for performance, after testing.(jacob)
        hp_factor = 1
        attack_portals_factor = 1
        enemy_mana_factor = -0.1

        return hp_delta * hp_factor + attack_portals_built * attack_portals_factor + enemy_mana * enemy_mana_factor

    def attack_portals_built(self, game):  # returns amount of portals built on a certain side
        return len(self.attackDict)  # the side of thr rows needs to be checked

    def outside_aggressive_buildportals(self, game, elfDict, attackDict):
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]  # update self.my_elves
        self.attackDict = list(attackDict.values())  # update self.attackDict
        self.update_dirDict(elfDict)  # update dirDict

        flanking_elves = self.build_portals(game, elfDict, attackDict)  # i mean basically build flanking portals

        return flanking_elves

    def build_portals(self, game, elfDict, attackDict):
        """
        build portals at the designated flanking points
        """
        print "agressive: trying to build portals"
        def closest_attack_portal(Elf):
            if len(self.attackDict) == 0:
                return 1
            elf = Elf.elf  # quarries the elf object from Elf class
            min_dist = elf.location.distance(self.attackDict[0])
            for portal in self.attackDict[1:]:
                dist = elf.location.distance(portal)
                if dist < min_dist:
                    min_dist = dist
            return min_dist

        enemy_castle = self.game.get_enemy_castle()
        flanking_elves = []
        attack_portal_amount = (game.get_myself().mana_per_turn * 3 // 40)
        if attack_portal_amount < 2:
            attack_portal_amount = 2
        amount_of_assigned_elves = attack_portal_amount - len(self.attackDict)
        distance_from_tgt = 600
        if len(self.my_elves) < amount_of_assigned_elves:  # check if the amount of elves i want to assign is to big
            amount_of_assigned_elves = len(self.my_elves)
        elves_by_distance = sorted(self.my_elves, key=closest_attack_portal, reverse=True)

        for elf in elves_by_distance[0:amount_of_assigned_elves]:  # build portals with all assigned elves
            location_to_move = self.move_normal(game, enemy_castle.location, distance_from_tgt,
                                                self.dirDict[elf.elf.unique_id])
            if elf.elf.location.distance(location_to_move) < 50:  # check if elf is in designated location
                if elf.elf.can_build_portal():  # if able to built portal
                    elf.elf.build_portal()
                    elf.was_building = True
            else:  # if not at location to build move to the location
                elf.flank(game, location_to_move)
            flanking_elves.append(elf)
        return flanking_elves

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

            else:  # if has nothing to attack attack the enemy castle
                elf.attack(enemy_castle)

    def do_aggressive(self, game, elfDict, attackDict):
        self.my_elves = [elf for elf in elfDict.values() if not elf.elf.already_acted]  # update self.my_elves
        self.attackDict = list(attackDict.values())  # update self.attackDict
        self.update_dirDict(elfDict)  # update dirDict
        enemy_castle = game.get_enemy_castle()

        if enemy_castle.current_health <= 10:  # rush the enemy castle if its low health
            for elf in self.my_elves:
                if elf.elf.in_attack_range(enemy_castle):
                    elf.attack(enemy_castle)
                else:
                    elf.move_speed_invis(enemy_castle)
            self.my_elves = []

        flanking_elves = self.build_portals(game, elfDict, attackDict)  # i mean basically build flanking portals

        self.attack(game)
        print attackDict
        for portal in self.attackDict:  # spam lava giants while mana above 60
            if (game.get_my_mana() - 40) < 100:
                break
            if not portal.is_summoning:
                portal.summon_lava_giant()

        return flanking_elves

    @staticmethod
    def move_normal(game, tgt, dist, dir=None, srt=None, fix=None):
        """
        the elf (s) moves to a or b from :srt             a
        where e is designated point :tgt      -->   s-----e
        the distance from e to a|b is :dist               b
        :param tgt: The point where you make a normal line to you
        :param dist: The distance you want to go on the perpendicular line
        :param dir: The direction you prefer to go in (up, left) = 1, (down, right) = -1
        :param srt: Optional parameter, starting point; if not set is default to game.get_enemy_castle().location
        :param fix: optional parameter if left None location will move to my_castle until portal is able to be build
        else if set to 1 location will be moved towards tgt else if set to -1 location will be moved towards enemy_castle
        :return: The location the elf should go in
        """
        global pointA, pointB
        if srt is None:
            srt = game.get_my_castle().location

        my_castle = game.get_my_castle()
        enemy_castle = game.get_enemy_castle()

        x_a, y_a = float(tgt.col), float(tgt.row)
        x_b, y_b = float(srt.col), float(srt.row)

        x_d, y_d = x_a - x_b, y_a - y_b
        d = sqrt(x_d ** 2 + y_d ** 2)

        x_d /= d
        y_d /= d

        x_1, y_1 = x_a + dist * y_d, y_a - dist * x_d
        x_2, y_2 = x_a - dist * y_d, y_a + dist * x_d

        pointA = Location(int(y_1), int(x_1))
        pointB = Location(int(y_2), int(x_2))

        def in_boundaries(game, loc, dist):
            if (dist < loc.row < game.rows - dist) and (dist < loc.col < game.cols - dist):
                return True
            return False

        def check_if_able_to_build(loc):  # check if able to build a portal if not move the point over
            global pointA, pointB
            while not game.can_build_portal_at(pointA) and not pointA.equals(loc) and in_boundaries(game, pointA, 50):
                pointA = pointA.towards(loc, 10)
            while not game.can_build_portal_at(pointB) and not pointB.equals(loc) and in_boundaries(game, pointB, 50):
                pointB = pointB.towards(loc, 10)
            if pointA.equals(loc) or pointB.equals(loc):
                print "REEE"

        if fix == -1:
            check_if_able_to_build(enemy_castle)
        elif fix == 1:
            check_if_able_to_build(tgt)
        else:
            check_if_able_to_build(my_castle)

        # choosing pointA or pointB:
        if dir is None:
            enemy_portals = game.get_enemy_castle()
            dest = pointA
            max = 0
            if enemy_portals:
                for point in [pointA, pointB]:
                    for portal in enemy_portals:
                        if point.distance(portal.location) > max:
                            max = point.distance(portal.location)
                            dest = point
                return dest

            else:
                return pointA
        elif dir == 1:
            return pointA
        elif dir == -1:
            return pointB
        else:
            return pointA
