import libtcodpy as libtcod

import colors

def process_death(entity, fov_map):
    """Check for death and destruction"""
    # player killed the thing... or something killed the player...
    # TODO: drop a corpse, items?
    if 'Alive' in entity and entity['Alive'] and entity['Health'] < 1:
        entity['Alive'] = False
        entity['Color'] = colors.dark_red
        entity['Solid'] = 0.4 # NOTE! should we make states?.. "rock" "blob" "puddle", etc...
        entity['ZOrder'] = 1 # the creature is now an 'item'
        entity['Goal'] = 'RIP' # NOTE! we are assuming AI? is this a code smell?
        # Tell fov_map to consider this entity passable and invisible
        libtcod.map_set_properties(fov_map, entity['Position']['x'], entity['Position']['y'], True, True)
        del entity['Movement']
        return [{
            'notification': {
                'text': entity['Name'] + ' just died.',
                'color': colors.dark_red
            }
        }, { 'player_dead': True }]
    if 'Map' in entity and entity['Health'] < 1:
        entity['Solid'] = 0
        entity['Health'] = 100
        # NOTE! although it makes sense to give the "ground" a fresh start (maybe player wants to dig?)
        # a bonus benefit is that the dead map entity won't trigger this eventuality!!!!! watch for this elsewhere too!!!!!!!!
        entity['Color'] = colors.dark_ground
        # Tell fov_map to consider this entity passable and invisible
        libtcod.map_set_properties(fov_map, entity['Position']['x'], entity['Position']['y'], True, True)
        return [{
            'notification': {
                'text': entity['Name'] + ' was destroyed.',
                'color': colors.grey
            }
        }]
    return []
