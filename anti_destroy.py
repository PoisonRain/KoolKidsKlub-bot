""" add to do_turn to make it win against destroy """

if game.turn == 1:
        try:
            if game.get_enemy_portals()[0].location.equals(Location(1968,1831)):
                bot_name = 'destroy'
        except Exception as e:
            print e
               
if bot_name == 'destroy':
    try:
        if len(my_elves) > 0:
            if len(game.get_enemy_mana_fountains()) > 0:
                if my_elves[0].in_attack_range(game.get_enemy_mana_fountains()[0]):
                    my_elves[0].attack(game.get_enemy_mana_fountains()[0])
                else:
                    my_elves[0].move_to(game.get_enemy_mana_fountains()[0])

    except Exception as e:
        print e
