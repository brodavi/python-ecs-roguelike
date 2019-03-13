import esper
import libtcodpy as libtcod
from random import randint
import math

from components import *
import game_map
import colors
import initial_data as init

from fov_functions import initialize_fov, recompute_fov

from ecs_world import ecs_world
getc = ecs_world.component_for_entity

class HealthProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    def process(self):
        for ent, health in self.world.get_component(Health):
            # player killed the monster... or the monster killed the player... remove the entity
            # TODO: drop a corpse, items?
            if health.health < 1:
                self.world.delete_entity(ent)

def entity_stops_movement(entity):
    return (getc(entity, Solid).solid > 0.75) and (getc(entity, Size).size > 0.75) and (getc(entity, Compressability).compressability < 0.5)

def distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx ** 2 + dy ** 2)

def from_a_to_b(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    dist = distance(x1, y1, x2, y2)
    dx = int(round(dx / dist))
    dy = int(round(dy / dist))
    return (dx, dy)

class AIProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    def process(self):
        for ent, (player, pos) in self.world.get_components(Player, Position):
            player = ent
            playerx = pos.x
            playery = pos.y
        for ent, (mov, pos, attack, goal) in self.world.get_components(Movement, Position, Attack, Goal):
            if goal.goal == 'APPROACH':
                if not libtcod.map_is_in_fov(fov_map, pos.x, pos.y):
                    goal.goal == None
                    break

                # determine which direction to move to get closer to the player
                (dx, dy) = from_a_to_b(pos.x, pos.y, playerx, playery)
                mov.x = dx
                mov.y = dy
                continue

            if goal.goal == None:
                if libtcod.map_is_in_fov(fov_map, pos.x, pos.y):
                    # if the entity is in fov, change goal to APPROACH
                    print('player is close by, and entity ', ent, ' wants to approach')
                    goal.goal = 'APPROACH'
                    continue

                print('entity ', ent, ' wants to move randomly' )
                # if no goal, move randomly
                invalid = True
                attempts = 0
                while invalid:
                    attempts += 1
                    invalid = False
                    mov.x = randint(-1, 1)
                    mov.y = randint(-1, 1)
                    entities_at = game_map.entities_at(game_map.tiles, pos.x + mov.x, pos.y + mov.y)

                    for entity in entities_at:
                        if entity_stops_movement(entity):
                            invalid = True

                    if attempts > 10:
                        print('too many attempts to wander aimlessly into something... I give up, just standing still now.')
                        # too many attempts to move randomly into solid obstacles... forget it
                        mov.x = 0
                        mov.y = 0
                        invalid = False

class MemoryProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    def process(self):
        for ent, (pos, seen) in self.world.get_components(Position, Seen):
            # if it is in the current FOV as defined by the player's fov, consider it explored
            if libtcod.map_is_in_fov(fov_map, pos.x, pos.y):
                seen.seen = True

fov_map = initialize_fov() # TODO: maybe just leave this to fov_functions.py? why even have this here?
class FOVProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    def process(self):
        for ent, (player, pos) in self.world.get_components(Player, Position): # TODO: figure out a better way to find the player entity
            print('NOTE: player entity is: ', ent)
            recompute_fov(fov_map, pos.x, pos.y, init.fov_radius, init.fov_light_walls, init.fov_algorithm)

        for ent, (sol, col, pos, opa) in self.world.get_components(Solid, Color, Position, Opacity):
            if ecs_world.has_component(ent, Movement): # excludes player and monsters
                break

            if libtcod.map_is_in_fov(fov_map, pos.x, pos.y):
                # if this thing is in FOV....
                if (sol.solid > 0.75) and (opa.opacity > 0.75):
                    # print('and this thing is solid')
                    col.color = colors.light_wall
                else:
                    # else this is ground... visible in FOV
                    col.color = colors.light_ground
            else:
                # else this thing is not in FOV....
                if (sol.solid > 0.75) and (opa.opacity > 0.75):
                    # print('this solid wall is outside fov')
                    col.color = colors.dark_wall
                else:
                    # else this is ground... outside of FOV
                    col.color = colors.dark_ground

class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        # process the movement of anything that has movement and position
        for ent, (mov, pos) in self.world.get_components(Movement, Position):
            if (mov.x == 0) and (mov.y == 0):
                print('entity ', ent, ' is not moving')
                # skip anything that isn't moving anyway
                continue

            dx = pos.x + mov.x
            dy = pos.y + mov.y

            # check for blocking
            entities_at = game_map.entities_at(game_map.tiles, dx, dy) # TODO: see, this doesn't make any sense... just keep tiles in game_map.py as a "global" there or something

            # check for if this thing is too solid to pass through
            movement_stopped = False
            for entity in entities_at:
                if entity_stops_movement(entity):
                    # if this thing is solid, stop movement
                    movement_stopped = True

                    if ecs_world.has_component(entity, Health):
                        # something with Health here... so entity will attack it.
                        print('entity ', ent, ' will now attack ', entity, ' with attack level ', getc(ent, Attack).attack)
                        getc(entity, Health).health -= getc(ent, Attack).attack
                        print(entity, ' health is now ', getc(entity, Health).health)
                        break

            if not movement_stopped:
                # if ecs_world.has_component(ent, Goal):
                #     print('hey this entity ', ent, ' is getting movement-processed (position is gonna be updated!) and it has a goal. dx dy  ', dx, dy)
                pos.x = dx
                pos.y = dy

class RenderProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        seencount = 0
        unseencount = 0
        for ent, (col, char, pos) in self.world.get_components(Color, Char, Position):
            if libtcod.map_is_in_fov(fov_map, pos.x, pos.y) or (ecs_world.has_component(ent, Map) and getc(ent, Seen).seen):
                # set "character" color?
                libtcod.console_set_default_foreground(init.con, col.color)

                # put the entity somewhere
                libtcod.console_put_char(init.con, pos.x, pos.y, char.char, libtcod.BKGND_NONE)

        # blit to the console.... huh? a hidden grid?
        libtcod.console_blit(init.con, 0, 0, init.screen_width, init.screen_height, 0, 0, 0)
        # actually throw it all up there...
        libtcod.console_flush()

        for ent, (mov, pos) in self.world.get_components(Movement, Position):
            # put a space over the entity for next time... ONLY entities with Movement component
            libtcod.console_put_char(init.con, pos.x, pos.y, ' ', libtcod.BKGND_NONE)
