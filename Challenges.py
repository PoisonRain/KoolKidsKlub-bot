

__meta_class__ = type


def is_challenge(game):
    """
    :return: a tuple (week #, challenge #) for example (1, 4) or False if its not a challenge
    """
    print Week(game).print_all()
    week_one = WeekOne(game).check_all()
    if week_one:
        return week_one



class Week:
    def __init__(self, game):
        self.game = game
        self.my_portals = game.get_my_portals()
        self.enemy_portals = game.get_enemy_portals()
        self.my_castle = game.get_my_castle()
        self.enemy_castle = game.get_enemy_castle()
        self.my_mana = game.get_my_mana()
        self.default_mana_per_turn = game.default_mana_per_turn
        self.my_elves = game.get_my_living_elves()
        self.enemy_elves = game.get_enemy_living_elves()
        self.enemy_mana = game.get_enemy_mana()
        self.my_mana_per_turn = self.default_mana_per_turn + len(game.get_my_mana_fountains()) * \
                                game.mana_fountain_mana_per_turn
        self.enemy_mana_per_turn = self.default_mana_per_turn + len(game.get_enemy_mana_fountains()) * \
                                        game.mana_fountain_mana_per_turn
        self.enemy_trolls = game.get_enemy_ice_trolls()
        self.enemy_giants = game.get_enemy_lava_giants()

    def check_all(self):
        pass

    def print_all(self):
        print self.anything_to_location(self.enemy_portals), "enemy_portals"
        print self.anything_to_location(self.enemy_castle), "enemy_castle"
        print self.anything_to_location(self.enemy_trolls), "enemy_trolls"
        print self.anything_to_location(self.enemy_elves), "enemy_elves"
        print self.anything_to_location(self.enemy_giants), "enemy_giants"
        print self.anything_to_location(self.enemy_mana), "enemy_mana"
        print self.anything_to_location(self.enemy_mana_per_turn), "enemy_mana_per_turn"
        print self.anything_to_location(self.my_portals), "my_portals"
        print self.anything_to_location(self.my_castle), "my_castle"
        print self.anything_to_location(self.my_elves), "my_elves"
        print self.anything_to_location(self.my_mana), "my_mana"
        print self.anything_to_location(self.my_mana_per_turn), "my_mana_per_turn"
        print self.anything_to_location(self.default_mana_per_turn), "default_mana_per_turn"

    @staticmethod
    def anything_to_location(anything):
        try:
            if anything is not None:
                return [object.location for object in anything]
            return []
        except TypeError:
            try:
                return anything.location
            except AttributeError:
                return anything
        except AttributeError:
            return anything



class WeekOne(Week):
    def __init__(self, game):
        Week.__init__(self, game)

    def check_all(self):
        if self.one():
            tup = (1, 1)
            return tup

    def one(self):
        if self.anything_to_location(self.enemy_portals) != [(1968, 1831)]:
            return False
        if self.anything_to_location(self.enemy_castle) != (700, 5800):
            return False
        if self.anything_to_location(self.enemy_trolls) != []:
            return False
        if self.anything_to_location(self.enemy_elves) != []:
            return False
        if self.anything_to_location(self.enemy_giants) != []:
            return False
        if self.anything_to_location(self.enemy_mana) != 12:
            return False
        if self.anything_to_location(self.enemy_mana_per_turn) != 12:
            return False
        if self.anything_to_location(self.my_portals) != []:
            return False
        if self.anything_to_location(self.my_castle) != (3100, 700):
            return False
        if self.anything_to_location(self.my_elves) != [(3100, 700)]:
            return False
        if self.anything_to_location(self.my_mana) != 0:
            return False
        if self.anything_to_location(self.my_mana_per_turn) != 0:
            return False
        if self.anything_to_location(self.default_mana_per_turn) != 0:
            return False
        return True























