import libtcodpy as libtcod
import game_map
import colors

def process_movement(entity, entities, fov_map):
    """Handle movement requests, checking for things in the way and possibly damaging them"""
    results = []

    if entity['Movement']['x'] == 0 and entity['Movement']['y'] == 0:
        return results

    destination_x = entity['Position']['x'] + entity['Movement']['x']
    destination_y = entity['Position']['y'] + entity['Movement']['y']

    # check target coordinates for blocking entity (like a wall or a creature)
    entities_at = game_map.entities_at(entities, destination_x, destination_y)

    # check for if this thing is too solid to pass through
    movement_stopped = False
    for ent in entities_at:
        if (ent['Solid'] > 0.75) and (ent['Size'] > 0.75):
            # if this thing is solid, stop movement
            movement_stopped = True

            if ent['Health']:
                # something with Health here... so entity will attack it.
                results.append({
                    'notification': {
                        'text': '{0} will now attack {1} with attack level {2} against its defense of {3}'
                            .format(entity['Name'], ent['Name'], entity['Attack'], ent['Defense']),
                        'color': colors.white
                        }
                    })
                damage = entity['Attack'] - ent['Defense']
                if damage > 0:
                    ent['Health'] -= entity['Attack'] - ent['Defense']
                results.append({
                    'notification': {
                        'text': '{0} health is now {1}'.format(ent['Name'], ent['Health']),
                        'color': colors.red if ent['Health'] < 10 else colors.white
                    }
                })
                break

    if not movement_stopped:
        # First, tell the fov_map that the space the entity had occupied is now clear
        libtcod.map_set_properties(fov_map, entity['Position']['x'], entity['Position']['y'], True, True)
        entity['Position']['x'] = destination_x
        entity['Position']['y'] = destination_y
        # Then, tell fov_map that the space the entity is currently occupying is not clear
        libtcod.map_set_properties(fov_map, entity['Position']['x'], entity['Position']['y'], False, False) # TODO: maybe see around orcs?

    return results
