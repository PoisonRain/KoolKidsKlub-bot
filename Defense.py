from elf_kingdom import *

class Defense:
    def __init__(self, game, elfDict):
        self.game = game
        self.elfDict = elfDict

    def do_defence(self, game, elfDict):
        self.elfDict = elfDict
        self.game = game
        danger_close = 2000  # distance from enemy portals that's considered to close
        elf_portal_pairs = [(elf, portal) for elf, portal in elfDict.values(), game.get_enemy_portals()]
