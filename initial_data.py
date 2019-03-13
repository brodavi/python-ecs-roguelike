import libtcodpy as libtcod

title = 'libtcod tutorial revised'

screen_width = 80
screen_height = 50
map_width = 80
map_height = 45
room_max_size = 10
room_min_size = 6
max_rooms = 30
fov_algorithm = 0
fov_light_walls = True
fov_radius = 10
max_monsters_per_room = 3

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(screen_width, screen_height, title, False)
con = libtcod.console_new(screen_width, screen_height)
