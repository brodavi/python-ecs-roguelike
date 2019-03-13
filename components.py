import libtcodpy as libtcod

##################################
## Here are a couple of Components
##################################

class Goal:
    def __init__(self, goal=None):
        self.goal = goal

class Defense:
    def __init__(self, defense=1):
        self.defense = defense

class Attack:
    def __init__(self, attack=1):
        self.attack = attack

class Health:
    def __init__(self, health=100):
        self.health = health

class Map:
    def __init__(self, map=False):
        self.map = map

class Seen:
    def __init__(self, seen=False):
        self.seen = seen

class LastKnownPosition:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Player:
    def __init__(self, player=False):
        self.player = True

class Solid:
    def __init__(self, solid=1.0):
        self.solid = solid

class Opacity:
    def __init__(self, opacity=1.0):
        self.opacity = opacity

class Compressability:
    def __init__(self, compressability=0.0):
        self.compressability = compressability

class Size:
    def __init__(self, size=1.0):
        self.size = size

class Position:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class Movement:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class Color:
    def __init__(self, color=libtcod.white):
        self.color = color

class Char:
    def __init__(self, char='@'):
        self.char = char
