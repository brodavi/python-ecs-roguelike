import libtcodpy as libtcod

def handle_keys(key, game_state):
    if game_state == 'SHOW_INVENTORY':
        return handle_inventory_keys(key)
    if game_state == 'DEFAULT':
        return handle_action_keys(key)
    if game_state == 'PLAYER_DEAD':
        return handle_player_dead_keys(key)
    return {}

def handle_inventory_keys(key):
    """Use items, wield weapons, do stuff"""
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}

def handle_action_keys(key):
    """Generate an action dictionary for the captured key"""

    key_char = chr(key.c)
    # print('------got ', key_char, '------')

    # Movement keys
    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}
    elif key_char == 'g':
        return {'pickup': True}
    elif key_char == 'i':
        return {'use': True}
    elif key_char == 'd':
        return {'drop': True}

    # elif key.vk == libtcod.KEY_A:
    #     return {'attack': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_player_dead_keys(key):
    """Very limited interaction... for now"""
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}
