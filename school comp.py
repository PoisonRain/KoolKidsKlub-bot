"""
This is an example for a bot.
"""
from elf_kingdom import *

lava_giant_max_speed = 200
RELEVANT_ATTACK_SPAWN_DISTANCE = 15 * lava_giant_max_speed

# HAYKE
PORTAL_DEFENSE_DISTANCE = 3000
DEFENSE_DISTANCE = 2000
SPAWN_ICE = False


def do_turn(game):
    """
    Makes the bot run a single turn.

    :param game: the current game state.
    :type game: Game
    """
    # Give orders to my elves.
    # handle_elves(game)
    # Give orders to my portals.
    # handle_portals(game)
    handle_attack_portals(game)
    defense_portals(game)  # hayke
    handle_attack_elves(game)
    handle_defense_elf(game)
    defense_portals(game)


def handle_attack_portals(game):
    enemy_elves = game.get_enemy_living_elves()
    enemy = game.get_enemy()
    enemy_castle = game.get_enemy_castle()
    portals = game.get_my_portals()
    attack_portals = list()
    for portal in portals:
        if portal.in_range(enemy_castle, RELEVANT_ATTACK_SPAWN_DISTANCE):
            attack_portals.append(portal)
    for portal in attack_portals:
        for elf in enemy_elves:
            if portal.in_range(elf, game.elf_attack_range + 4 * game.elf_max_speed) and portal.can_summon_ice_troll():
                print('summon ice troll in attack portal')
                portal.summon_ice_troll()
        if portal.can_summon_lava_giant() and game.get_my_mana() > 80:
            portal.summon_lava_giant()
            print('summon lava giant in attack portal')


def handle_defense_elf(game):
    """
    Gives orders to my elves.

    :param game: the current game state.
    :type game: Game
    """

    """ defending elf boi"""
    defense_elf = game.get_all_my_elves()[0]
    Defense_portal_location = game.get_my_castle().location.towards(game.get_enemy_castle().location,
                                                                    1000)  # the location

    if defense_elf.is_alive():
        # if in range of enemy portal, destory portal
        elf_acted = False

        if game.get_enemy_portals() is not None:
            for portal in game.get_enemy_portals():
                if defense_elf.in_attack_range(portal):
                    defense_elf.attack(portal)
                    elf_acted = True
                    break
        if not elf_acted:
            # if portal not built, build portal
            Defense_portal_built = False  # if a portal is already built it will change to True
            if game.get_my_portals is not None:
                for portal in game.get_my_portals():
                    if portal.location == Defense_portal_location:
                        Defense_portal_built = True

            if not Defense_portal_built:
                if defense_elf.location != Defense_portal_location:
                    defense_elf.move_to(Defense_portal_location)
                elif game.can_build_portal_at(Defense_portal_location) & defense_elf.can_build_portal():
                    defense_elf.build_portal()

            else:
                for elf in game.get_all_enemy_elves():
                    try:
                        if defense_elf.in_attack_range(elf):
                            defense_elf.attack(elf)
                            elf_acted = True
                            break

                        elif defense_elf.in_range(elf.location, 600):
                            defense_elf.move_to(elf.location)
                            elf_acted = True
                            break
                    except:
                        print 'enemy elf dead'

                if not elf_acted:
                    for creature in game.get_enemy_creatures():
                        try:
                            if defense_elf.in_attack_range(creature):
                                defense_elf.attack(creature)
                                break
                            elif defense_elf.in_range(creature.location, 600):
                                defense_elf.move_to(creature.location)
                                break
                        except:
                            print 'creature dead'

    """ end defending elf boi """
    # Go over all the living elves.


def handle_elves(game):
    """
    Gives orders to my elves.

    :param game: the current game state.
    :type game: Game
    """
    # Get enemy castle.
    enemy_castle = game.get_enemy_castle()  # type: Castle
    # Go over all the living elves.
    for elf in game.get_my_living_elves():
        # Try to attack enemy castle, if not move to it.
        if elf.in_attack_range(enemy_castle):
            # Attack!
            elf.attack(enemy_castle)
            # Print a message.
            print 'elf ', elf, ' attacks ', enemy_castle

        else:
            # Move to enemy castle!
            elf.move_to(enemy_castle)
            # Print a message.
            print 'elf ', elf, 'moves to ', enemy_castle


def handle_portals(game):
    """
    Gives orders to my portals.

    :param game: the current game state.
    :type game: Game
    """
    # Go over all of my portals.
    for portal in game.get_my_portals():
        # If the portal can summon a lava giant, do that.
        if portal.can_summon_lava_giant():
            # Summon the lava giant.
            portal.summon_lava_giant()
            # Print a message.
            print 'portal ', portal, ' summons a lava giant'


# HAYKE
def defense_portals(game):
    my_castel = game.get_my_castle()
    my_portals = game.get_my_portals()
    enemy_elf = game.get_enemy_living_elves()
    enemy_lava = game.get_enemy_lava_giants()
    for elf in enemy_elf:
        if my_castel.distance(elf) < DEFENSE_DISTANCE:
            print "summon"
            spawn_ice(game, my_castel)
        else:
            SPAWN_ICE = False


def spawn_ice(game, my_castel):
    my_portals = game.get_my_portals()
    for portal in my_portals:
        if my_castel.distance(portal) < PORTAL_DEFENSE_DISTANCE:
            if portal.can_summon_ice_troll:
                portal.summon_ice_troll()
            # SPAWN_ICE = True
            # summon_ice(game,my_portals,my_castel)


def summon_ice(game, my_portals, my_castel):
    if my_portals[0] != None:
        closest_portal = my_portals[0]
        for portal in my_portals:
            if my_castel.distance(portal) < closest_portal:
                closest_portal = portal
    if SPAWN_ICE and closest_portal.can_summon_ice_troll:
        closest_portal.summon_ice_troll()


# Eyal
# Attack Bois
def handle_attack_elves(game):
    # constants
    if game.get_all_my_elves()[1].is_alive():
        lava_giant_max_speed = 200
        relevant_attack_spawn_distance = 15 * lava_giant_max_speed
        my_portals = game.get_my_portals()
        enemy_portals = game.get_enemy_portals()
        enemy_castle = game.get_enemy_castle()
        attack_elf = game.get_all_my_elves()[1]
        is_built = False
        can_attack = True
        try:
            portal_to_attack = enemy_portals[0]
        except:
            print "no enemy portal"
            can_attack = False

        # checking if needs to attack a portal or build a portal
        for portal in my_portals:
            if portal.in_range(enemy_castle, relevant_attack_spawn_distance):
                is_built = True
                break

        # if there are no portals built, build a portal
        if is_built == False:
            if attack_elf.in_range(enemy_castle, relevant_attack_spawn_distance):
                if attack_elf.can_build_portal():
                    attack_elf.build_portal()
                else:
                    attack_elf.move_to(enemy_castle)
            else:
                attack_elf.move_to(enemy_castle)

        # if there is a portal built attack an enemy portal
        elif can_attack:
            for portal in enemy_portals:
                if portal.location.distance(attack_elf.location) < portal_to_attack.location.distance(
                        attack_elf.location):
                    portal_to_attack = portal
            if attack_elf.in_attack_range(portal_to_attack):
                attack_elf.attack(portal_to_attack)
            else:
                attack_elf.move_to(portal_to_attack)


# HAYKE
def defense_portals(game):
    my_castel = game.get_my_castle()
    enemy_giants = game.get_enemy_lava_giants()
    my_portals = game.get_my_portals()
    try:
        closest_portal = my_portals[0]
        for portal in my_portals:
            if my_castel.distance(portal) < closest_portal:
                closest_portal = portal
        for giant in enemy_giants:
            if closest_portal.in_range(giant,
                                       game.lava_giant_attack_range + 4 * game.lava_giant_max_speed) and closest_portal.can_summon_ice_troll():
                print('summon ice troll in defense portal')
                closest_portal.summon_ice_troll()
    except:
        pass


def adefense_portals(game):
    my_castel = game.get_my_castle()
    my_portals = game.get_my_portals()
    enemy_elf = game.get_enemy_living_elves()
    enemy_lava = game.get_enemy_lava_giants()
    my_ice_trolls = game.get_my_ice_trolls()
    lava_bool = False
    Elf_bool = False
    threat_level = 0
    for elf in enemy_elf:
        if my_castel.distance(elf) < DEFENSE_DISTANCE:
            threat_level = threat_level + 2
            SPAWN_ICE = True
        else:
            Elf_bool = False
    for lava in enemy_lava:
        if my_castel.distance(lava) < DEFENSE_DISTANCE:
            threat_level = threat_level + 0.5
            SPAWN_ICE = True
        else:
            lava_bool = False
    # spawn_ice(game,my_castel)
    if lava_bool == False and Elf_bool == False:
        SPAWN_ICE = False
    summon_ice(game, my_portals, my_castel)


def spawn_ice(game, my_castel):
    my_portals = game.get_my_portals()
    for portal in my_portals:
        if my_castel.distance(portal) < PORTAL_DEFENSE_DISTANCE:
            if portal.can_summon_ice_troll():
                # portal.summon_ice_troll()
                SPAWN_ICE = True

                # summon_ice(game,my_portals,my_castel)


def summon_ice(game, my_portals, my_castel):
    if my_portals[0] != None:
        closest_portal = my_portals[0]
        for portal in my_portals:
            if my_castel.distance(portal) < closest_portal:
                print 'test1'
                closest_portal = portal
        print (str(SPAWN_ICE) + "lll  " + str(closest_portal.can_summon_ice_troll()))
        if SPAWN_ICE and closest_portal.can_summon_ice_troll() and my_castel.distance(
                closest_portal) < PORTAL_DEFENSE_DISTANCE:
            print"2"
            closest_portal.summon_ice_troll()


