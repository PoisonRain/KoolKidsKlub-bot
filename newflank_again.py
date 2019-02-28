import Elf


def flank_or_run(game, elf, target_location):
    my_mana = game.get_my_mana()
    if my_mana > game.portal_cost * 2 + game.invisibility_cost:
        elf.move_invis(target_location)
    else:
        elf.move(target_location)
