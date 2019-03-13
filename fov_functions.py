import libtcodpy as libtcod

from components import *

import initial_data as init

from ecs_world import ecs_world
getc = ecs_world.component_for_entity

import game_map

def should_block_sight(entity):
    return (getc(entity, Solid).solid > 0.75) and (getc(entity, Opacity).opacity > 0.75)

def should_block_passing(entity):
    return (getc(entity, Solid).solid > 0.75) and (getc(entity, Size).size > 0.75)

def initialize_fov():
    fov_map = libtcod.map_new(init.map_width, init.map_height)

    for y in range(init.map_height):
        for x in range(init.map_width):
            libtcod.map_set_properties(fov_map, x, y, not should_block_sight(game_map.tiles[x][y]), not should_block_passing(game_map.tiles[x][y]))

    return fov_map

def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)
