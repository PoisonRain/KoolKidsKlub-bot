from elf_kingdom import *

MANE_DRAIN_RANGE = 1500  # the distance of checking if there is a creature in range of the enemy castel we dont want to spawn from

def normal(game, elfDict):
    
    
    pass


def normal_enemy_mana_drain(game,attack_portals):  # send a lava golem if: there is no lava golem near the enemy castel already and no enemy ice troll
    lava, ice = True
    for creature in game.get_my_lava_giants():
        if creature.distance(game.get_enemy_castle()) < MANE_DRAIN_RANGE:
            lava = False
    for creature in game.get_enemy_ice_trolls():
        if creature.distance(game.get_enemy_castle()) < MANE_DRAIN_RANGE:
            ice = False
    if (ice == False and lava == False):
        for portal in attack_portals:
            if portal.can_summon_lava_giant():
                portal.summon_lava_giant()
                lava,ice = True
            


def normal_attack_lowMana(game, Attack_List,attack_portals):  # when enemy has low mana increese attack according to the attack list
    for portal in attack_portals:                     # instead of the mana drain spam.    
        if Attack_List.check_next() == "lava":
            if portal.can_summon_lava_giant():
                portal.summon_lava_giant()
                Attack_List.get_next()
        if Attack_List.check_next() == "ice":
            if portal.can_summon_ice_troll():
                portal.summon_ice_troll()
                Attack_List.get_next()
    

class Attack_List():  # func for the list of which creatures to spawn in which order, restets index every X turns
    
    def __init__(self): 
        self.a_list = ["lava","lava","ice"]
        self.location = 0
        self.turn_counter = 0
    
    def check_next(self):  # return next creature to spawn without changing index
        return self.a_list[self.location]  
        
    def get_next(self):  # return next creature to spawn + changing the index to point to the next one on the list
        self.location += 1
        if self.location > len(self.a_list):  # reset location to start of list if spawned last creature
            self.location = 0
        self.turn_counter = 0
        return self.a_list[self.location - 1]
    
    def update_turns(self):  # update turns passed since last call
        self.turn_counter += 1
