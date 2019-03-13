import libtcodpy as libtcod

import colors
import initial_data as init

########==========-------- Helper Functions ---------============#############


########==========-------- The Processors ---------============#############

def process_mouseover(entity, fov_map, mouse):
    """Handle what happens to an entity when the mouse is over it"""
    results = []

    if 'HoverColor' in entity:
        del entity['HoverColor']

    # Determine if map entity is in player's (for now) FOV, possibly adjusting color
    if entity['Position']['x'] == mouse.cx and entity['Position']['y'] == mouse.cy:
        # adding a hover color?
        entity['HoverColor'] = colors.purple
        results.append({
            'identify': {
                'text': entity['Name'],
                'z': entity['ZOrder']
            }
        })

    return results


############============-------- The Main Show ---------============#############

def process_mouse_move(entity, entities, fov_map, mouse):
    """A convenience function to apply several mousing processor functions to entities"""
    # you should really try to be clear on what your processors need and expect
    mouseover_actions = []
    if 'Name' in entity:
        mouseover_actions = process_mouseover(entity, fov_map, mouse)

    return mouseover_actions
