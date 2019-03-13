import libtcodpy as libtcod

def process_memory(entity, fov_map):
    """Determine if entity (just wall for now) has been seen by player (and only player, for now)"""
    # if it is in the current FOV as defined by the player's fov, consider it explored
    if libtcod.map_is_in_fov(fov_map, entity['Position']['x'], entity['Position']['y']):
        entity['Seen'] = True
    return []
