"""Generates one floor of a dungeon for Nat Twentea's The Masks We Wear v3.1"""


__author__ = 'Adam Degenhardt'


from enum import Enum, unique
from math import floor
from random import randrange

from .encounter import Encounter

MAX_HALLWAY_LENGTH = 5
DEFAULT_DUNGEON_SIZE = 30


@unique
class RoomType(Enum):
    NONE = 0
    STAIRCASE = 1
    TREASURE = 2
    EMPTY = 3
    SAFE = 4
    GUARDED_TREASURE = 5
    HAZARD = 6
    DEATH = 7
    ENEMY = 8
    START = 9


class Deck:
    """
    A deck of Major Arcana cards. Specific arcana are not represented - only
    the number of cards for each room type.
    """
    def __init__(self):
        self._cards = \
            [RoomType.STAIRCASE] * 2 + \
            [RoomType.TREASURE] * 4 + \
            [RoomType.EMPTY] * 3 + \
            [RoomType.SAFE] * 2 + \
            [RoomType.GUARDED_TREASURE] + \
            [RoomType.HAZARD] * 2 + \
            [RoomType.DEATH] + \
            [RoomType.ENEMY] * 7
        self._initial_count = len(self._cards)

    def draw(self):
        assert(len(self._cards) >= 0)
        return self._cards.pop(randrange(len(self._cards)))

    def cards_drawn(self):
        return self._initial_count - len(self._cards)


class Room:
    """Represents one room in the dungeon"""
    right_door_exists = False
    down_door_exists = False
    room_type = RoomType.NONE
    # Encounter if this is an encounter room
    encounter = None


class Dungeon:
    """Represents a dungeon floor. A 2D array of rooms"""
    def __init__(self, dungeon_size=DEFAULT_DUNGEON_SIZE):
        self._rooms = \
            [[Room() for i in range(dungeon_size)] for j in range(dungeon_size)]
        self.dungeon_size = dungeon_size

        # Keep track of the horizontal bounds of the dungeon so it can be cropped during render
        self.leftmost = dungeon_size
        self.rightmost = 0

        # Keep track of encounters so we can generate them at the end
        self.encounters = []

    def _check_valid_coords(self, x, y):
        assert(x >= 0)
        assert(x < self.dungeon_size)
        assert(y >= 0)
        assert(y < self.dungeon_size)

    def get_room_type(self, x, y):
        self._check_valid_coords(x, y)
        return self._rooms[y][x].room_type

    def room_written(self, x, y):
        return self.get_room_type(x, y) != RoomType.NONE

    def set_room_type(self, x, y, room_type):
        if self.room_written(x, y):
            renderer = HTMLRenderer(self)
            renderer.render()
            print('Tried to overwrite room at {}, {}'.format(x, y))
            assert(False)
        self._rooms[y][x].room_type = room_type
        if room_type in [RoomType.ENEMY, RoomType.GUARDED_TREASURE]:
            self._rooms[y][x].encounter = Encounter(None) # TODO: supply arcana
            self.encounters.append(self._rooms[y][x].encounter)

        # Update horizontal bounds
        if x < self.leftmost:
            self.leftmost = x
        if x > self.rightmost:
            self.rightmost = x

    def add_right_door(self, x, y):
        self._check_valid_coords(x, y)
        assert(self._rooms[y][x].right_door_exists == False)
        self._rooms[y][x].right_door_exists = True

    def add_down_door(self, x, y):
        self._check_valid_coords(x, y)
        assert(self._rooms[y][x].down_door_exists == False)
        self._rooms[y][x].down_door_exists = True

    def can_build_direction(self, direction, x, y):
        self._check_valid_coords(x, y)
        for i in range(1, MAX_HALLWAY_LENGTH):
            if direction == Direction.RIGHT:
                if x + i >= self.dungeon_size:
                    return False
                if self.room_written(x + i, y):
                    return False
            elif direction == Direction.LEFT:
                if x - i < 0:
                    return False
                if self.room_written(x - i, y):
                    return False
            elif direction == Direction.UP:
                if y - i < 0:
                    return False
                if self.room_written(x, y - i):
                    return False
            elif direction == Direction.DOWN:
                if y + i >= self.dungeon_size:
                    return False
                if self.room_written(x, y + i):
                    return False
        return True

    def generate_encounters(self):
        # TODO: set difficulty based on number of encounters
        for encounter in self.encounters:
            encounter.generate(None)



class HTMLRenderer:
    """Renders a dungeon in ASCII art"""
    ROW_MARGIN = 16

    sprites = {
        RoomType.NONE: '  ',
        RoomType.STAIRCASE: '//',
        RoomType.TREASURE: '$$',
        RoomType.EMPTY: '[]',
        RoomType.SAFE: '<3',
        RoomType.GUARDED_TREASURE: 'X$',
        RoomType.HAZARD: '/\\',
        RoomType.DEATH: '8X',
        RoomType.ENEMY: '\\O',
        RoomType.START: '\\\\'
    }

    def __init__(self, dungeon):
        self._dungeon = dungeon

    def render(self):
        render_string = '<style>pre {margin: 0.0}</style>'

        def add_line(line):
            nonlocal render_string
            render_string = render_string + '<pre>' + line + '<br /></pre>'

        # Print legend
        gap = '    '
        add_line('')
        add_line( \
            HTMLRenderer.sprites[RoomType.START] + ' Entrance' + gap + \
            HTMLRenderer.sprites[RoomType.STAIRCASE] + ' Stairs' + gap + \
            HTMLRenderer.sprites[RoomType.TREASURE] + ' Treasure' + gap + \
            HTMLRenderer.sprites[RoomType.EMPTY] + ' Empty' + gap + \
            HTMLRenderer.sprites[RoomType.SAFE] + ' Safe' \
        )
        add_line( \
            HTMLRenderer.sprites[RoomType.GUARDED_TREASURE] + ' Guarded Treasure' + gap + \
            HTMLRenderer.sprites[RoomType.HAZARD] + ' Hazard' + gap + \
            HTMLRenderer.sprites[RoomType.DEATH] + ' Death' + gap + \
            HTMLRenderer.sprites[RoomType.ENEMY] + ' Enemy Encounter' \
        )
        add_line('')

        # Render dungeon
        border = '*' + ('~' * 60) + '*'
        add_line(border)
        add_line('')
        for row in self._dungeon._rooms:
            if not all(room.room_type == RoomType.NONE for room in row):
                row_render = ' ' * HTMLRenderer.ROW_MARGIN
                hall_row_render = ' ' * HTMLRenderer.ROW_MARGIN
                for room in row[self._dungeon.leftmost : self._dungeon.rightmost + 1]:
                    right_hall = '__' if room.right_door_exists else '  '
                    row_render = row_render + HTMLRenderer.sprites[room.room_type] + right_hall
                    down_hall = ' |' if room.down_door_exists else '  '
                    hall_row_render = hall_row_render + down_hall + '  '
                add_line(row_render)
                add_line(hall_row_render)
        add_line(border)
        add_line('')

        # Render encounters
        add_line('Encounters:')
        add_line('')
        for encounter in self._dungeon.encounters:
            render_string = render_string + encounter.renderHTML()
        add_line('')
        add_line(border)
        add_line('')

        return render_string


@unique
class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def generate():
    deck = Deck()
    # Must be around this size or larger or sometimes the generator gets "stuck" 
    # down branches with no legal direction to branch to
    dungeon_size = 30
    dungeon = Dungeon(dungeon_size)

    x = floor(dungeon_size / 2)
    y = floor(dungeon_size / 2)
    hall_length = 1
    stairs_drawn = False

    def choose_direction(candidate_directions):
        """
        Pick a direction in which we could build a full hallway without hitting
        an existing room or going off the grid
        """
        candidates = [c for c in candidate_directions if dungeon.can_build_direction(c, x, y)]
        if len(candidates) == 0:
            renderer = HTMLRenderer(dungeon)
            renderer.render()
            print("No valid directions to branch")
            assert(False)
        return candidates[randrange(len(candidates))]

    # Generate dungeon
    # Start in a random direction
    direction = choose_direction([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])

    dungeon.set_room_type(x, y, RoomType.START)
    while not (deck.cards_drawn() >= 7 and stairs_drawn):
        # Make a door and move to the next position
        if direction == Direction.RIGHT:
            dungeon.add_right_door(x, y)
            x = x + 1
        elif direction == Direction.DOWN:
            dungeon.add_down_door(x, y)
            y = y + 1
        elif direction == Direction.LEFT:
            x = x - 1
            assert(x >= 0)
            dungeon.add_right_door(x, y)
        elif direction == Direction.UP:
            y = y - 1
            assert(y >= 0)
            dungeon.add_down_door(x, y)

        # Add a card to the current space
        room = deck.draw()
        if room == RoomType.STAIRCASE:
            if stairs_drawn:
                room = RoomType.SAFE
            else:
                stairs_drawn = True
        dungeon.set_room_type(x, y, room)
        hall_length = hall_length + 1

        # Branch if we need to. Choose the start of the new branch randomly
        # from non-end spaces in the current branch
        if hall_length >= MAX_HALLWAY_LENGTH:
            if direction == Direction.RIGHT:
                x = x - randrange(1, 4)
                direction = choose_direction([Direction.UP, Direction.DOWN])
            elif direction == Direction.LEFT:
                x = x + randrange(1, 4)
                direction = choose_direction([Direction.UP, Direction.DOWN])
            elif direction == Direction.DOWN:
                y = y - randrange(1, 4)
                direction = choose_direction([Direction.RIGHT, Direction.LEFT])
            elif direction == Direction.UP:
                y = y + randrange(1, 4)
                direction = choose_direction([Direction.RIGHT, Direction.LEFT])
            hall_length = 1

    dungeon.generate_encounters()

    # Print the dungeon render
    renderer = HTMLRenderer(dungeon)
    return renderer.render()

if __name__ == "__main__":
    print(generate())
