import libtcodpy as libtcod

import initial_data as init

def can_see_through(entity):
    """Can this entity be seen through?"""
    return (entity['Solid'] < 0.75) or (entity['Opacity'] < 0.75)

def can_pass_through(entity):
    """Can this entity be passed through?"""
    return (entity['Solid'] < 0.75) or (entity['Size'] < 0.75)

fov_map = None
def make_fov_map(tiles):
    """Take the list of tiles and feed it to libtcod to generate the fov_map, taking into account tiles that block sight"""
    global fov_map
    fov_map = libtcod.map_new(init.map_width, init.map_height)

    for tile in tiles:
        libtcod.map_set_properties(fov_map, tile['Position']['x'], tile['Position']['y'], can_see_through(tile), can_pass_through(tile))
    return fov_map
