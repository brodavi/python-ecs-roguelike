import libtcodpy as libtcod
from random import randint

import initial_data as init

import colors

def turn_into_ground(tiles, x, y):
    """Turn a wall entity into a ground entity"""
    for tile in tiles:
        if (tile['Position']['x'] == x) and (tile['Position']['y'] == y):
            tile['Position']['z'] = -1 # NOTE: z position has no purpose at the moment
            tile['Name'] = 'ground'
            tile['Solid'] = 0
            tile['Opacity'] = 0
            tile['Color'] = colors.dark_ground

def entities_at(entities, x, y):
    """Return a list of entities at this location"""
    ents = []
    for entity in entities:
        # TODO: I don't like this... checking Position first... we should have something like
        # 'positionEntities' or something... this wouldn't be a think if we did "PURE" ECS
        if 'Position' in entity and (entity['Position']['x'] == x) and (entity['Position']['y'] == y):
            ents.append(entity)

    return ents

def create_room(tiles, room):
    """Carve out a room given the room data"""
    for x in range(room['x1'] + 1, room['x2']):
        for y in range(room['y1'] + 1, room['y2']):
            turn_into_ground(tiles, x, y)

def get_center(room):
    """Return the center coordinates of the room"""
    center_x = int((room['x1'] + room['x2']) / 2)
    center_y = int((room['y1'] + room['y2']) / 2)
    return (center_x, center_y)

def intersect(room1, room2):
    """Whether or not these two rooms intersect"""
    return (room1['x1'] <= room2['x2'] and room1['x2'] >= room2['x1'] and
            room1['y1'] <= room2['y2'] and room1['y2'] >= room2['y1'])

def get_rect(x, y, w, h):
    """Return a rectangle dictionary given these dimensions"""
    x1 = x
    y1 = y
    x2 = x + w
    y2 = y + h
    return { 'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2 }

def create_h_tunnel(tiles, x1, x2, y):
    """Carve out a horizontal tunnel from point x1 to point x2"""
    for x in range(min(x1, x2), max(x1, x2) + 1):
        turn_into_ground(tiles, x, y)

def create_v_tunnel(tiles, y1, y2, x):
    """Carve out a vertical tunnel from point y1 to point y2"""
    for y in range(min(y1, y2), max(y1, y2) + 1):
        turn_into_ground(tiles, x, y)

def make_map(tiles):
    """Take the list of tiles and generate a map from it, carving out rooms and inserting monsters"""
    rooms = []
    num_rooms = 0

    for r in range(init.max_rooms):
        # random width and height
        w = randint(init.room_min_size, init.room_max_size)
        h = randint(init.room_min_size, init.room_max_size)
        # random position without going out of the boundaries of the map
        x = randint(0, init.map_width - w - 1)
        y = randint(0, init.map_height - h - 1)

        # "Rect" class makes rectangles easier to work with
        new_room = get_rect(x, y, w, h)

        # run through the other rooms and see if they intersect with this one
        for other_room in rooms:
            if intersect(new_room, other_room):
                break

        # weird, unreadable thing here means: "if the for loop did not 'break', then do this"
        else:
            # this means there are no intersections, so this room is valid

            create_room(tiles, new_room)

            # center coordinates of new room, will be useful later
            (new_x, new_y) = get_center(new_room)

            # if this is the first room, jump immediately
            # to creating a second room. do not create tunnel
            if num_rooms == 0:
                rooms.append(new_room)
                num_rooms += 1
                continue

            # from the second room on...

            # ---==connect it to the previous room with a tunnel==---

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

            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1

    return rooms
