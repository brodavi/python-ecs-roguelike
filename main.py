import libtcodpy as libtcod

import esper

from components import *
from processors import FOVProcessor, MovementProcessor, RenderProcessor, MemoryProcessor, AIProcessor, HealthProcessor
from input_handlers import handle_keys

import colors
import game_map
from ecs_world import ecs_world
from player import create_player

getc = ecs_world.component_for_entity

def main():
    fov_processor = FOVProcessor()
    movement_processor = MovementProcessor()
    render_processor = RenderProcessor()
    memory_processor = MemoryProcessor()
    ai_processor = AIProcessor()
    health_processor = HealthProcessor()

    ecs_world.add_processor(movement_processor, priority=2)
    ecs_world.add_processor(fov_processor, priority=1)
    ecs_world.add_processor(render_processor)
    ecs_world.add_processor(memory_processor)
    ecs_world.add_processor(ai_processor)
    ecs_world.add_processor(health_processor)

    player = create_player()

    # force the player into the center of the first room
    first_room_center = game_map.get_center(game_map.first_room)
    getc(player, Position).x = first_room_center[0]
    getc(player, Position).y = first_room_center[1]

    # initial process of the esper world
    ecs_world.process()

    while True:
        # get the keypress
        key = libtcod.console_wait_for_keypress(True)

        print('got key: ', key)

        # map keypress to action
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        attack = action.get('action')
        fullscreen = action.get('fullscreen')

        if attack:
            # ask for attack info
            print('attack?')

        if move:
            # if user wants to move, set the Movement component, then let the processors handle the rest (follow this pattern with any action?)
            dx, dy = move
            getc(player, Movement).x = dx
            getc(player, Movement).y = dy

        if exit:
            print('we hit escape')
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # after collecting all the actions, run all processors
        ecs_world.process()

        # /do stuff

if __name__ == '__main__':
    main()
