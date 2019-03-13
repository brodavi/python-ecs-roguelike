import libtcodpy as libtcod
from random import randint

import initial_data as init

from components import *
from ecs_world import ecs_world

import colors

getc = ecs_world.component_for_entity

def turn_into_ground(tile):
    getc(tile, Solid).solid = 0
    getc(tile, Color).color = colors.dark_ground

def make_tiles(map_width, map_height):
    return [[ecs_world.create_entity(
        Position(x, y),
        Char('#'),
        Color(colors.dark_wall),
        Size(1),
        Opacity(1),
        Solid(1),
        Compressability(0),
        Seen(False),
        Health(100),
        Map(True)) for y in range(map_height)] for x in range(map_width)]

def entities_at(tiles, x, y):
    entities = []
    for ent, pos in ecs_world.get_component(Position):
        # print(pos)
    # for ent, (sol, siz, pos, comp) in ecs_world.get_components(Solid, Size, Position, Compressability):
        # if (pos.x == x) and (pos.y == y) and (sol.solid > 0.75) and (siz.size > 0.75) and (comp.compressability < 0.5):
        if (pos.x == x) and (pos.y == y):
            entities.append(ent)

    return entities

def create_room(tiles, room):
    for x in range(room['x1'] + 1, room['x2']):
        for y in range(room['y1'] + 1, room['y2']):
            turn_into_ground(tiles[x][y])

def get_center(room):
    center_x = int((room['x1'] + room['x2']) / 2)
    center_y = int((room['y1'] + room['y2']) / 2)
    return (center_x, center_y)

def intersect(room1, room2):
    return (room1['x1'] <= room2['x2'] and room1['x2'] >= room2['x1'] and
            room1['y1'] <= room2['y2'] and room1['y2'] >= room2['y1'])

def get_rect(x, y, w, h):
    x1 = x
    y1 = y
    x2 = x + w
    y2 = y + h
    return { 'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2 }

def create_h_tunnel(tiles, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        turn_into_ground(tiles[x][y])

def create_v_tunnel(tiles, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        turn_into_ground(tiles[x][y])

def place_entities(room):
    # Get a random number of monsters
    number_of_monsters = randint(0, init.max_monsters_per_room)

    for i in range(number_of_monsters):
        # Choose a random location in the room
        x = randint(room['x1'] + 1, room['x2'] - 1)
        y = randint(room['y1'] + 1, room['y2'] - 1)

        superposition = False
        for ent, (mov, pos) in ecs_world.get_components(Movement, Position):
            if x == pos.x and y == pos.y:
                superposition = True

        if not superposition:
            if randint(0, 100) < 50:
                # monster = Entity(x, y, 'o', libtcod.desaturated_green)
                ecs_world.create_entity(
                    Color(colors.desaturated_green),
                    Char('o'),
                    Movement(0, 0),
                    Position(x, y),
                    Opacity(1),
                    Compressability(0.25),
                    Size(.85),
                    Solid(0.85),
                    Health(6),
                    Attack(1),
                    Defense(1),
                    Goal(None)
                )
            else:
                # monster = Entity(x, y, 'T', libtcod.darker_green)
                ecs_world.create_entity(
                    Color(colors.darker_green),
                    Char('T'),
                    Movement(0, 0),
                    Position(x, y),
                    Opacity(1),
                    Compressability(0.25),
                    Size(0.85),
                    Solid(0.85),
                    Health(9),
                    Attack(2),
                    Defense(1),
                    Goal(None)
                )

# we are mutating the tiles datastructure
first_room = None # to pass to dependent (main)
second_room = None # to pass to dependent (main)
def make_map(tiles, max_rooms, room_min_size, room_max_size, map_width, map_height):
    global first_room
    global second_room
    rooms = []
    num_rooms = 0

    for r in range(max_rooms):
        # random width and height
        w = randint(room_min_size, room_max_size)
        h = randint(room_min_size, room_max_size)
        # random position without going out of the boundaries of the map
        x = randint(0, map_width - w - 1)
        y = randint(0, map_height - h - 1)

        # "Rect" class makes rectangles easier to work with
        new_room = get_rect(x, y, w, h)

        # run through the other rooms and see if they intersect with this one
        for other_room in rooms:
            if intersect(new_room, other_room):
                break
        # weird, unreadable thing here means: "if the for loop did not 'break', then do this"
        else:
            # this means there are no intersections, so this room is valid

            # "paint" it to the map's tiles
            create_room(tiles, new_room)

            # center coordinates of new room, will be useful later
            (new_x, new_y) = get_center(new_room)

            if num_rooms == 0:
                first_room = new_room
            else:
                # if second room, save it
                if num_rooms == 1:
                    second_room = new_room

                # all rooms after the first (including the 2nd):
                # connect it to the previous room with a tunnel

                # center coordinates of previous room
                (prev_x, prev_y) = get_center(rooms[num_rooms - 1])

                # flip a coin (random number that is either 0 or 1)
                if randint(0, 1) == 1:
                    # first move horizontally, then vertically
                    create_h_tunnel(tiles, prev_x, new_x, prev_y)
                    create_v_tunnel(tiles, prev_y, new_y, new_x)
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(tiles, prev_y, new_y, prev_x)
                    create_h_tunnel(tiles, prev_x, new_x, new_y)

            # add monsters & stuff
            place_entities(new_room)
            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1

    return rooms

tiles = make_tiles(init.map_width, init.map_height)
rooms = make_map(tiles, init.max_rooms, init.room_min_size, init.room_max_size, init.map_width, init.map_height)
