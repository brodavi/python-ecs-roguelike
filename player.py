from ecs_world import ecs_world

from components import *

import colors

def create_player():
    return ecs_world.create_entity(
        Player(True),
        Color(colors.white),
        Char('@'),
        Movement(0, 0),
        Position(0, 0),
        Opacity(1),
        Compressability(0),
        Size(.85),
        Solid(1),
        Health(20),
        Attack(3),
        Defense(3)
    )
