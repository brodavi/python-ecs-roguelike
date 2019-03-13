import libtcodpy as libtcod

import colors
import initial_data as init

########==========-------- Helper Functions ---------============#############


########==========-------- The Processors ---------============#############

def process_mouse_click(entity, fov_map, mouse):
    """Handle what happens to an entity when it is clicked on"""
    results = []

    # Determine if map entity is in player's (for now) FOV, possibly adjusting color
    if entity['Position']['x'] == mouse.cx and entity['Position']['y'] == mouse.cy:
        entity['IsTargeted'] = True

    return results

############============-------- The Main Show ---------============#############

def process_click(entity, entities, fov_map, mouse):
    """A convenience function to apply several click processor functions to entities"""
    # you should really try to be clear on what your processors need and expect
    mouse_click_actions = []
    if 'Name' in entity:
        mouse_click_actions = process_mouse_click(entity, fov_map, mouse)

    return mouse_click_actions
