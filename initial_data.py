import libtcodpy as libtcod

title = 'libtcod tutorial a different approach'

screen_width = 80
screen_height = 50
bar_width = 20
panel_height = 7
panel_y = screen_height - panel_height
message_x = bar_width + 2
message_width = screen_width - bar_width - 2
message_height = panel_height - 1
map_width = 80
map_height = 43
room_max_size = 15
room_min_size = 10
max_rooms = 30
fov_algorithm = 0
fov_light_walls = True
fov_radius = 10
min_items = 10
max_items = 25
min_monsters = 5
max_monsters = 20

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(screen_width, screen_height, title, False)
con = libtcod.console_new(screen_width, screen_height)
panel = libtcod.console_new(screen_width, panel_height)
