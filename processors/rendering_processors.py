import libtcodpy as libtcod

import colors
import initial_data as init

########==========-------- The Processors ---------============#############

def process_basic_rendering(entity, fov_map):
    """Handle the rendering of any renderable entities"""
    if 'Obscured' in entity:
        return []
    if 'Map' in entity:

        # If displaying A*, ignore fov colors for this round
        if entity['A*Highlight']:
            entity['Color'] = colors.purple
            entity['A*Highlight'] = False # immediately forget about it

        else:
            # Determine if map entity is in player's (for now) FOV, possibly adjusting color
            if libtcod.map_is_in_fov(fov_map, entity['Position']['x'], entity['Position']['y']):
                # if this thing is in FOV....
                if (entity['Solid'] > 0.75) and (entity['Opacity'] > 0.75):
                    # print('and this thing is solid')
                    entity['Color'] = colors.light_wall
                else:
                    # else this is ground... visible in FOV
                    entity['Color'] = colors.light_ground
            else:
                # else this thing is not in FOV....
                if (entity['Solid'] > 0.75) and (entity['Opacity'] > 0.75):
                    # print('this solid wall is outside fov')
                    entity['Color'] = colors.dark_wall
                else:
                    # else this is ground... outside of FOV
                    entity['Color'] = colors.dark_ground

    if libtcod.map_is_in_fov(fov_map, entity['Position']['x'], entity['Position']['y']) or ('Map' in entity and entity['Seen']) or True:
        # if it is a wall or ground, just display the background, not the character
        if 'Map' in entity:
            libtcod.console_set_char_background(init.con, entity['Position']['x'], entity['Position']['y'], entity['Color'], libtcod.BKGND_SET)

        # set color
        if 'HoverColor' in entity:
            libtcod.console_set_default_foreground(init.con, entity['HoverColor'])
        else:
            libtcod.console_set_default_foreground(init.con, entity['Color'])

        # put the entity somewhere
        libtcod.console_put_char(init.con, entity['Position']['x'], entity['Position']['y'], entity['Char'], libtcod.BKGND_NONE)
    return []

############============-------- The Main Show ---------============#############

def process_all_rendering(entity, fov_map):
    """A convenience function to apply several tick processor functions to entities"""
    basic_rendering_actions = []
    # you should really try to be clear on what your processors need and expect
    # NOTE: Health should come first, because if something is dead, no sense in having it think or move
    if 'Position' in entity:
        basic_rendering_actions = process_basic_rendering(entity, fov_map)

    return basic_rendering_actions
