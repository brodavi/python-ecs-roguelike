import libtcodpy as libtcod
from random import randint, choice

from processors.tick_processor import process_tick
from processors.mouse_move_processors import process_mouse_move
from processors.click_processors import process_click
from processors.rendering_processors import process_all_rendering

from fov_functions import make_fov_map
from input_handlers import handle_keys
import initial_data as init
import colors
import game_map
from render_ui import render_bar, render_to_panel, add_notification, render_inventory_menu

def place_in_random_room(thing, rooms):
    """Assumes thing has a position to assign a random spot to"""
    room = choice(rooms)
    new_x = randint(room['x1'] + 1, room['x2'] - 1)
    new_y = randint(room['y1'] + 1, room['y2'] - 1)
    thing['Position']['x'] = new_x
    thing['Position']['y'] = new_y

def processAllEntities(processor, player, entities, fov_map, mouse):
    """Runs all the entities through whatever processor is given"""
    actions = []
    for entity in entities:
        actions += processor(entity, entities, fov_map, mouse)
        # NOTE: re-computing fov here for every entity. weird. but the reason is that
        # each entity has a chance to change the fov map (moving into / out of fov, creating shadows, affecting A*, etc)
        libtcod.map_compute_fov(fov_map, player['Position']['x'], player['Position']['y'], init.fov_radius, init.fov_light_walls, init.fov_algorithm)
    return actions

def main():
    """The main program. Initializes data, then runs through the main loop until user quits."""
    previous_game_state = 'NONE'
    game_state = 'INIT'

    entities = []
    tiles = []
    for y in range(init.map_height):
        for x in range(init.map_width):
            tiles.append({
                'Name': 'wall',
                'Position': { 'x': x, 'y': y, 'z': 0 },
                'Char': '#',
                'Color': colors.dark_wall,
                'Size': 1,
                'Opacity': 1,
                'Solid': 1,
                'Seen': False,
                'Health': 100,
                'Map': True,
                'Defense': 0,
                'ZOrder': 0,
                'A*Highlight': False
            })

    player = {
        'Name': 'player',
        'Player': True,
        'Color': colors.white,
        'Char': '@',
        'Movement': { 'x': 0, 'y': 0, 'z': 0 },
        'Position': { 'x': 0, 'y': 0, 'z': 1 },
        'Opacity': 1,
        'Compressability': 0,
        'Size': 0.85,
        'Solid': 1,
        'Health': 20,
        'MaxHealth': 20,
        'Attack': 3,
        'Defense': 0,
        'Alive': True,
        'ZOrder': 2, # above items / bodies
        'Inventory': { 'capacity': 20, 'items': [] },
        'Action': ''
    }

    monsters = []
    number_of_monsters = randint(init.min_monsters, init.max_monsters)
    for i in range(number_of_monsters):
        if randint(0, 100) < 50:
            # add an orc
            monsters.append({
                'Name': 'orc',
                'Color': colors.desaturated_green,
                'Char': 'o',
                'Movement': { 'x': 0, 'y': 0, 'z': 0 },
                'Position': { 'x': 0, 'y': 0, 'z': 1 },
                'Opacity': 1,
                'Size': 0.85,
                'Solid': 0.85,
                'Health': 6,
                'Attack': 1,
                'Defense': 0,
                'Goal': None,
                'Alive': True,
                'ZOrder': 2,
                'Inventory': { 'capacity': 3, 'items': [] },
                'Action': ''
            })
        else:
            # Add a troll
            monsters.append({
                'Name': 'troll',
                'Color': colors.darker_green,
                'Char': 'T',
                'Movement': { 'x': 0, 'y': 0, 'z': 0 },
                'Position': { 'x': 0, 'y': 0, 'z': 1 },
                'Opacity': 1,
                'Size': 0.85,
                'Solid': 0.85,
                'Health': 9,
                'Attack': 2,
                'Defense': 0,
                'Goal': None,
                'Alive': True,
                'ZOrder': 2,
                'Inventory': { 'capacity': 3, 'items': [] },
                'Action': ''
            })

    items = []
    number_of_items = randint(init.min_items, init.max_items)
    for i in range(number_of_items):
        items.append({
            'Name': 'healing potion',
            'Color': colors.violet,
            'Char': '!',
            'Position': { 'x': 0, 'y': 0, 'z': 0 },
            'Opacity': 1,
            'Size': 0.2,
            'Solid': 1,
            'Healing': 5,
            'ZOrder': 1
        })

    # mutating the tiles into a map, returning the corners of the rooms
    rooms = game_map.make_map(tiles)

    # add stuff to rooms, randomly
    for thing in [player] + monsters + items:
        place_in_random_room(thing, rooms)

    # note we are giving initialize_fov tiles, not rooms
    fov_map = make_fov_map(tiles)

    # add everything into the entities list for processing
    entities = [player] + monsters + items + tiles

    # notifications are the game messages displayed for the player to read
    notifications = []

    keyb = libtcod.Key()
    mouse = libtcod.Mouse()

    while True:
        ###################### Here is the main loop... do the processing ###################

        # TODO: drop cool-downs until someone is at 0
        # take that turn for that entity
            # if not player's turn, continue looping
            # if player's turn, get input

        actions = []

        if game_state == 'INIT':
            actions += processAllEntities(process_tick, player, entities, fov_map, mouse)
            game_state = 'DEFAULT'

        if game_state == 'DEFAULT':
            if not keyb.vk == libtcod.KEY_NONE:
                # process all entities [tick]
                actions += processAllEntities(process_tick, player, entities, fov_map, mouse)

            if mouse.x:
                # process all entities [mousing]
                actions += processAllEntities(process_mouse_move, player, entities, fov_map, mouse)

            if mouse.lbutton_pressed or mouse.rbutton_pressed:
                # process all entities [clicking]
                actions += processAllEntities(process_click, player, entities, fov_map, mouse)

############################# The Rendering ################################

        # render all entitites in z order
        entities_in_render_order = sorted(entities, key=lambda x: x['ZOrder'])
        for entity in entities_in_render_order:
            process_all_rendering(entity, fov_map)

        # render everything
        libtcod.console_blit(init.con, 0, 0, init.screen_width, init.screen_height, 0, 0, 0)

        # render the UI
        libtcod.console_set_default_background(init.panel, libtcod.black)
        libtcod.console_clear(init.panel)

        # render any notifications or identify imperitives
        for action in actions:
            notification = action.get('notification')
            identify = action.get('identify')
            pickupables = action.get('pickupables')
            if notification:
                # get notifications ready to render (wrapping, scrolling, etc...)
                add_notification(notifications, notification)
            if identify:
                # render the coords
                render_to_panel(init.panel, 10, 6 - identify['z'], identify['text'])
            if pickupables:
                print('pickupables: ', pickupables)

        # render the game messages, one line at a time
        y = 1
        for notification in notifications:
            libtcod.console_set_default_foreground(init.panel, notification['color'])
            libtcod.console_print_ex(init.panel, init.message_x, y, libtcod.BKGND_NONE, libtcod.LEFT, notification['text'])
            y += 1

        # render the health bar
        render_bar(init.panel, 1, 1, init.bar_width, 'HP', player['Health'], player['MaxHealth'],
                   libtcod.light_red, libtcod.darker_red)

        # render the coords
        # render_to_panel(init.panel, 6, 5, 'X: {0} Y: {1}'.format(player['Position']['x'], player['Position']['y']))
        libtcod.console_blit(init.panel, 0, 0, init.screen_width, init.panel_height, 0, 0, init.panel_y)

        # maybe render the inventory?
        if game_state == 'SHOW_INVENTORY':
            if player['Action'] == 'USE':
                render_inventory_menu('Press the key next to an item to use it, or Esc to cancel.\n', player['Inventory']['items'], 50)
            if player['Action'] == 'DROP':
                render_inventory_menu('Press the key next to an item to drop it, or Esc to cancel.\n', player['Inventory']['items'], 50)

        # flush it all to the screen
        libtcod.console_flush()

        ###################### That's it. Now wait for the player's next action ###################

        # now, get the keyboard input

        # key = libtcod.console_wait_for_keypress(True)

        # 0000001 event mask 1 == key down
        # 0000010 event mask 2 == key up
        # 0000100 event mask 4 == mouse move
        # 0001000 event mask 16 == mouse click

        # 0001101 mouse move & click, key down == 21
        evt = libtcod.sys_wait_for_event(21, keyb, mouse, True)

        # # NOTE: replace above with this to go real-time
        # libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, keyb, mouse


        # map keypress to action
        action = handle_keys(keyb, game_state)

        move = action.get('move')
        pickup = action.get('pickup')
        drop = action.get('drop')
        exit = action.get('exit')
        attack = action.get('action')
        fullscreen = action.get('fullscreen')
        use = action.get('use')
        inventory_index = action.get('inventory_index')
        close_inventory = action.get('close_inventory')
        player_dead = action.get('player_dead')

        ################################# handle keyboard input ###################################

        if 'Movement' in player:
            if move:
                # if user wants to move, set the Movement component, then let the processors handle the rest (follow this pattern with any action?)
                dx, dy = move
                player['Movement']['x'] = dx
                player['Movement']['y'] = dy
            else:
                player['Movement']['x'] = 0
                player['Movement']['y'] = 0

        if pickup:
            player['Action'] = 'PICKUP'

        if drop:
            print('player wants to drop something')
            player['Action'] = 'DROP'
            previous_game_state = game_state
            game_state = 'SHOW_INVENTORY'

        if use:
            print('player wants to use something')
            player['Action'] = 'USE'
            previous_game_state = game_state
            game_state = 'SHOW_INVENTORY'

        if player_dead:
            print('player dead game state')
            game_state = 'PLAYER_DEAD'

        if inventory_index is not None and game_state != 'PLAYER_DEAD' and inventory_index < len(player['Inventory']['items']):
            item = player['Inventory']['items'][inventory_index]
            if player['Action'] == 'USE':
                print('going to try to use ', item['Name'])
                game_state = previous_game_state
                item['Using'] = True # trigger the use of the item
            if player['Action'] == 'DROP':
                print('going to try to drop ', item['Name'], ' contained by ', item['ContainedBy']['Name'])
                game_state = previous_game_state
                item['Dropping'] = True # trigger dropping the item

        if close_inventory:
            game_state = previous_game_state

        if exit:
            print('we hit escape')
            if game_state == 'SHOW_INVENTORY':
                # TODO: if we exit the inventory menu without selecting anything
                # monsters will have an extra turn!
                game_state = previous_game_state
            else:
                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()
