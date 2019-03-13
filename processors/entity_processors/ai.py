import libtcodpy as libtcod
import initial_data as init
import colors
import math
from random import randint

def distance(x1, y1, x2, y2):
    """Euclidean distance"""
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx ** 2 + dy ** 2)

def from_a_to_b(x1, y1, x2, y2):
    """Obtain the closest coord in the direction of the target"""
    dist = distance(x1, y1, x2, y2)
    dx = x2 - x1
    dy = y2 - y1

    if dist == 0:
        print('something is wrong.. distance is 0?')
        dx = 0
        dy = 0
    else:
        dx = int(round(dx / dist))
        dy = int(round(dy / dist))
    return (dx, dy)

def move_astar(entity, entities, target, fov_map):
    """Use the A* algorithm to find a path to target, returning the next step along that path"""

    # TODO: maybe we re-use the existing fov map, but just un-set this entity and the target temporarily
    # that should save an entities iteration for making everything but entity and target unwalkable

    # Create a FOV map that has the dimensions of the map
    fov = libtcod.map_new(init.map_width, init.map_height)

    # Scan the current map each turn and set all the walls as unwalkable
    for ent in entities:
        if ent != entity and ent != target and 'Position' in ent:
            libtcod.map_set_properties(fov, ent['Position']['x'], ent['Position']['y'], ent['Opacity'] < 0.5, ent['Solid'] < 0.5)

    # Allocate a A* path
    # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
    my_path = libtcod.path_new_using_map(fov, 1.41)

    # Compute the path between self's coordinates and the target's coordinates
    libtcod.path_compute(my_path, entity['Position']['x'], entity['Position']['y'], target['Position']['x'], target['Position']['y'])

    # Debugging A*
    for i in range (libtcod.path_size(my_path)):
        (x, y) = libtcod.path_get(my_path, i)
        for ent in entities:
            if (i < libtcod.path_size(my_path) - 1) and 'Position' in ent and ent['Position']['x'] == x and ent['Position']['y'] == y and 'A*Highlight' in ent:
                ent['A*Highlight'] = True

    # Check if the path exists, and in this case, also the path is shorter than 25 tiles
    # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
    # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
    if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
        # Find the next coordinates in the computed full path
        (next_x, next_y) = libtcod.path_walk(my_path, True)
        dx = next_x - entity['Position']['x']
        dy = next_y - entity['Position']['y']
    else:
        # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
        # it will still try to move towards the player (closer to the corridor opening)
        (dx, dy) = from_a_to_b(entity['Position']['x'], entity['Position']['y'], target['Position']['x'], target['Position']['y'])

    # Delete the path to free memory
    libtcod.path_delete(my_path)
    return (dx, dy)

def process_ai(entity, entities, fov_map):
    """Check Goal, perform actions to reach goal"""
    results = []
    if entity['Goal'] == 'RIP':
        return results
    for ent in entities:
        if 'Player' in ent:
            player = ent
            break

    if entity['Goal'] == 'APPROACH':
        # NOTE: TODO:  we will want to have something like ['Goal']['Target'] at some point
        if not 'Movement' in player:
            # if player is dead #TODO: fix this hack
            entity['Goal'] = None
            return results

        if distance(entity['Position']['x'], entity['Position']['y'], player['Position']['x'], player['Position']['y']) == 1:
            (dx, dy) = from_a_to_b(entity['Position']['x'], entity['Position']['y'], player['Position']['x'], player['Position']['y'])
        else:
            # determine which direction to move to get closer to the player
            (dx, dy) = move_astar(entity, entities, player, fov_map)
        entity['Movement']['x'] = dx
        entity['Movement']['y'] = dy

    if entity['Goal'] == None:
        if libtcod.map_is_in_fov(fov_map, entity['Position']['x'], entity['Position']['y']) and 'Movement' in player: # NOTE: checking if player is dead... so weird.
            # if the entity is in fov, change goal to APPROACH
            entity['Goal'] = 'APPROACH'
            # let's go ahead and move the entity rather than wasting a turn
            (dx, dy) = move_astar(entity, entities, player, fov_map)

        else:
            # Move randomly
            invalid = True
            attempts = 0
            while invalid:
                attempts += 1
                invalid = False
                entity['Movement']['x'] = randint(-1, 1)
                entity['Movement']['y'] = randint(-1, 1)
                destination_x = entity['Position']['x'] + entity['Movement']['x']
                destination_y = entity['Position']['y'] + entity['Movement']['y']

                entities_at = []
                for ent in entities:
                    # TODO: I don't like this... checking Position first... we should have something like
                    # 'positionEntities' or something... this wouldn't be a think if we did "PURE" ECS
                    if 'Position' in ent and ent['Position']['x'] == destination_x and ent['Position']['y'] == destination_y:
                        entities_at.append(ent)

                for ent in entities_at:
                    if (ent['Solid'] > 0.75) and (ent['Size'] > 0.75):
                        invalid = True

                if attempts > 10:
                    # too many attempts to move randomly into solid obstacles... forget it
                    results.append({
                        'notification': {
                            'text': '{0} has given up trying to wander'.format(entity['Name']),
                            'color': colors.white
                        }
                    })
                    entity['Movement']['x'] = 0
                    entity['Movement']['y'] = 0
                    invalid = False
    return results
