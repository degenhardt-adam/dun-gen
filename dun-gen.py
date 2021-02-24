from enum import Enum, unique
from random import randrange


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
    right_door_exists = False
    down_door_exists = False
    room_type = RoomType.NONE


class Dungeon:
    def __init__(self, dungeon_size=DEFAULT_DUNGEON_SIZE):
        self._rooms = \
            [[Room() for i in range(dungeon_size)] for j in range(dungeon_size)]
        self.dungeon_size = dungeon_size

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
            renderer = TextRenderer(self)
            renderer.render()
            print('Tried to overwrite room at {}, {}'.format(x, y))
            assert(False)
        self._rooms[y][x].room_type = room_type

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



class TextRenderer:
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
        # Print legend
        gap = '    '
        print('')
        print( \
            TextRenderer.sprites[RoomType.START] + ' Entrance' + gap + \
            TextRenderer.sprites[RoomType.STAIRCASE] + ' Stairs' + gap + \
            TextRenderer.sprites[RoomType.TREASURE] + ' Treasure' + gap + \
            TextRenderer.sprites[RoomType.EMPTY] + ' Empty' + gap + \
            TextRenderer.sprites[RoomType.SAFE] + ' Safe' \
        )
        print( \
            TextRenderer.sprites[RoomType.GUARDED_TREASURE] + ' Guarded Treasure' + gap + \
            TextRenderer.sprites[RoomType.HAZARD] + ' Hazard' + gap + \
            TextRenderer.sprites[RoomType.DEATH] + ' Death' + gap + \
            TextRenderer.sprites[RoomType.ENEMY] + ' Enemy Encounter' \
        )
        print('')

        # Crop empty space around dungeon
        # TODO

        # Render dungeon
        border = '*' + ('~' * 60) + '*'
        print(border)
        print('')
        for row in self._dungeon._rooms:
            if not all(room.room_type == RoomType.NONE for room in row):
                row_render = ' '
                hall_row_render = ' '
                for room in row:
                    right_hall = '__' if room.right_door_exists else '  '
                    row_render = row_render + TextRenderer.sprites[room.room_type] + right_hall
                    down_hall = ' |' if room.down_door_exists else '  '
                    hall_row_render = hall_row_render + down_hall + '  '
                print(row_render)
                print(hall_row_render)
        print(border)
        print('')


@unique
class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def main():
    
    deck = Deck()
    dungeon_size = 30
    dungeon = Dungeon(dungeon_size)

    x = dungeon_size / 2
    y = dungeon_size / 2
    hall_length = 1
    stairs_drawn = False

    def choose_direction(candidate_directions):
        candidates = [c for c in candidate_directions if dungeon.can_build_direction(c, x, y)]
        if len(candidates) == 0:
            renderer = TextRenderer(dungeon)
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

        # Add a card to the dungeon
        room = deck.draw()
        if room == RoomType.STAIRCASE:
            if stairs_drawn:
                room = RoomType.SAFE
            else:
                stairs_drawn = True
        dungeon.set_room_type(x, y, room)
        hall_length = hall_length + 1

        # Branch if we need to
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

    # Print the dungeon render
    renderer = TextRenderer(dungeon)
    renderer.render()


if __name__ == "__main__":
    main()
