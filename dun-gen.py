"""Generates one floor of a dungeon for Nat Twentea's The Masks We Wear v3.1"""


__author__ = 'Adam Degenhardt'


from math import floor
from random import randrange


MAX_HALLWAY_LENGTH = 5
DEFAULT_DUNGEON_SIZE = 30


# Room Types
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


# Directions
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3


class Deck:
    """
    A deck of Major Arcana cards. Specific arcana are not represented - only
    the number of cards for each room type.
    """
    def __init__(self):
        self._cards = \
            [STAIRCASE] * 2 + \
            [TREASURE] * 4 + \
            [EMPTY] * 3 + \
            [SAFE] * 2 + \
            [GUARDED_TREASURE] + \
            [HAZARD] * 2 + \
            [DEATH] + \
            [ENEMY] * 7
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
    room_type = NONE


class Dungeon:
    """Represents a dungeon floor. A 2D array of rooms"""
    def __init__(self, dungeon_size=DEFAULT_DUNGEON_SIZE):
        self._rooms = \
            [[Room() for i in range(dungeon_size)] for j in range(dungeon_size)]
        self.dungeon_size = dungeon_size

        # Keep track of the horizontal bounds of the dungeon so it can be cropped during render
        self.leftmost = dungeon_size
        self.rightmost = 0

    def _check_valid_coords(self, x, y):
        assert(x >= 0)
        assert(x < self.dungeon_size)
        assert(y >= 0)
        assert(y < self.dungeon_size)

    def get_room_type(self, x, y):
        self._check_valid_coords(x, y)
        return self._rooms[y][x].room_type

    def room_written(self, x, y):
        return self.get_room_type(x, y) != NONE

    def set_room_type(self, x, y, room_type):
        if self.room_written(x, y):
            renderer = TextRenderer(self)
            renderer.render()
            print('Tried to overwrite room at {}, {}'.format(x, y))
            assert(False)
        self._rooms[y][x].room_type = room_type

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
            if direction == RIGHT:
                if x + i >= self.dungeon_size:
                    return False
                if self.room_written(x + i, y):
                    return False
            elif direction == LEFT:
                if x - i < 0:
                    return False
                if self.room_written(x - i, y):
                    return False
            elif direction == UP:
                if y - i < 0:
                    return False
                if self.room_written(x, y - i):
                    return False
            elif direction == DOWN:
                if y + i >= self.dungeon_size:
                    return False
                if self.room_written(x, y + i):
                    return False
        return True



class TextRenderer:
    """Renders a dungeon in ASCII art"""
    ROW_MARGIN = 16

    sprites = {
        NONE: '  ',
        STAIRCASE: '//',
        TREASURE: '$$',
        EMPTY: '[]',
        SAFE: '<3',
        GUARDED_TREASURE: 'X$',
        HAZARD: '/\\',
        DEATH: '8X',
        ENEMY: '\\O',
        START: '\\\\'
    }

    def __init__(self, dungeon):
        self._dungeon = dungeon

    def render(self):
        # Print legend
        gap = '    '
        print('')
        print( \
            TextRenderer.sprites[START] + ' Entrance' + gap + \
            TextRenderer.sprites[STAIRCASE] + ' Stairs' + gap + \
            TextRenderer.sprites[TREASURE] + ' Treasure' + gap + \
            TextRenderer.sprites[EMPTY] + ' Empty' + gap + \
            TextRenderer.sprites[SAFE] + ' Safe' \
        )
        print( \
            TextRenderer.sprites[GUARDED_TREASURE] + ' Guarded Treasure' + gap + \
            TextRenderer.sprites[HAZARD] + ' Hazard' + gap + \
            TextRenderer.sprites[DEATH] + ' Death' + gap + \
            TextRenderer.sprites[ENEMY] + ' Enemy Encounter' \
        )
        print('')

        # Render dungeon
        border = '*' + ('~' * 60) + '*'
        print(border)
        print('')
        for row in self._dungeon._rooms:
            if not all(room.room_type == NONE for room in row):
                row_render = ' ' * TextRenderer.ROW_MARGIN
                hall_row_render = ' ' * TextRenderer.ROW_MARGIN
                for room in row[self._dungeon.leftmost : self._dungeon.rightmost + 1]:
                    right_hall = '__' if room.right_door_exists else '  '
                    row_render = row_render + TextRenderer.sprites[room.room_type] + right_hall
                    down_hall = ' |' if room.down_door_exists else '  '
                    hall_row_render = hall_row_render + down_hall + '  '
                print(row_render)
                print(hall_row_render)
        print(border)
        print('')


class HTMLRenderer():
    """Renders a dungeon in HTML"""

    sprites = {
        NONE: '  ',
        STAIRCASE: '//',
        TREASURE: '$$',
        EMPTY: '[]',
        SAFE: '<3',
        GUARDED_TREASURE: 'X$',
        HAZARD: '/\\',
        DEATH: '8X',
        ENEMY: '\\O',
        START: '\\\\'
    }

    def __init__(self, dungeon):
        self._dungeon = dungeon

    def render(self):
        document.getElementById('dungeon').innerHTML = 'This is where I would put a dungeon... IF I HAD ANY'


def main():
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
            renderer = TextRenderer(dungeon)
            renderer.render()
            print("No valid directions to branch")
            assert(False)
        return candidates[randrange(len(candidates))]

    # Generate dungeon
    # Start in a random direction
    direction = choose_direction([UP, DOWN, LEFT, RIGHT])

    dungeon.set_room_type(x, y, START)
    while not (deck.cards_drawn() >= 7 and stairs_drawn):
        # Make a door and move to the next position
        if direction == RIGHT:
            dungeon.add_right_door(x, y)
            x = x + 1
        elif direction == DOWN:
            dungeon.add_down_door(x, y)
            y = y + 1
        elif direction == LEFT:
            x = x - 1
            assert(x >= 0)
            dungeon.add_right_door(x, y)
        elif direction == UP:
            y = y - 1
            assert(y >= 0)
            dungeon.add_down_door(x, y)

        # Add a card to the current space
        room = deck.draw()
        if room == STAIRCASE:
            if stairs_drawn:
                room = SAFE
            else:
                stairs_drawn = True
        dungeon.set_room_type(x, y, room)
        hall_length = hall_length + 1

        # Branch if we need to. Choose the start of the new branch randomly
        # from non-end spaces in the current branch
        if hall_length >= MAX_HALLWAY_LENGTH:
            if direction == RIGHT:
                x = x - randrange(1, 4)
                direction = choose_direction([UP, DOWN])
            elif direction == LEFT:
                x = x + randrange(1, 4)
                direction = choose_direction([UP, DOWN])
            elif direction == DOWN:
                y = y - randrange(1, 4)
                direction = choose_direction([RIGHT, LEFT])
            elif direction == UP:
                y = y + randrange(1, 4)
                direction = choose_direction([RIGHT, LEFT])
            hall_length = 1

    # Print the dungeon render
    renderer = HTMLRenderer(dungeon)
    renderer.render()


if __name__ == "__main__":
    main()
