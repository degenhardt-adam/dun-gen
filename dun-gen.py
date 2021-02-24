from enum import Enum, unique
from random import randrange


MAX_HALLWAY_LENGTH = 5
DEFAULT_DUNGEON_SIZE = 15

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

    def draw(self):
        assert(len(self._cards) >= 0)
        return self._cards.pop(randrange(len(self._cards)))


class Room:
    right_door_exists = False
    down_door_exists = False
    room_type = RoomType.NONE


class Dungeon:
    def __init__(self, dungeon_size=DEFAULT_DUNGEON_SIZE):
        self._rooms = \
            [[Room() for i in range(dungeon_size)] for j in range(dungeon_size)]
        self._dungeon_size = dungeon_size

    def _check_valid_coords(self, x, y):
        assert(x >= 0)
        assert(x < self._dungeon_size)
        assert(y >= 0)
        assert(y < self._dungeon_size)

    def get_room_type(self, x, y):
        self._check_valid_coords(x, y)
        return self._rooms[y][x].room_type

    def room_written(self, x, y):
        return self.get_room_type(x, y) != RoomType.NONE

    def set_room_type(self, x, y, room_type):
        assert(not self.room_written(x, y))
        self._rooms[y][x].room_type = room_type

    def add_right_door(self, x, y):
        self._check_valid_coords(x, y)
        assert(self._rooms[y][x].right_door_exists == False)
        self._rooms[y][x].right_door_exists = True

    def add_down_door(self, x, y):
        self._check_valid_coords(x, y)
        assert(self._rooms[y][x].down_door_exists == False)
        self._rooms[y][x].down_door_exists = True


SPRITES = {
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

@unique
class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def main():
    
    deck = Deck()
    dungeon_size = 15
    dungeon = Dungeon(dungeon_size)

    x = dungeon_size / 2
    y = dungeon_size / 2
    hall_length = 1
    stairs_drawn = False
    cards_drawn = 0

    def can_build_direction(direction):
        for i in range(1, MAX_HALLWAY_LENGTH):
            if direction == Direction.RIGHT:
                if x + i >= dungeon_size:
                    return False
                if dungeon.room_written(x + i, y):
                    return False
            elif direction == Direction.LEFT:
                if x - i < 0:
                    return False
                if dungeon.room_written(x - i, y):
                    return False
            elif direction == Direction.UP:
                if y - i < 0:
                    return False
                if dungeon.room_written(x, y - i):
                    return False
            elif direction == Direction.DOWN:
                if y + i >= dungeon_size:
                    return False
                if dungeon.room_written(x, y + i):
                    return False
        return True

    def choose_direction(candidate_directions):
        for candidate in candidate_directions:
            if not can_build_direction(candidate):
                candidate_directions.remove(candidate)
        assert(len(candidate_directions) > 0)
        return candidate_directions[randrange(len(candidate_directions))]

    # Generate dungeon
    # Start in a random direction
    direction = choose_direction([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])

    dungeon.set_room_type(x, y, RoomType.START)
    while not (cards_drawn >= 7 and stairs_drawn):
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
        cards_drawn = cards_drawn + 1

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

    # Print legend
    gap = '    '
    print('')
    print( \
        SPRITES[RoomType.START] + ' Entrance' + gap + \
        SPRITES[RoomType.STAIRCASE] + ' Stairs' + gap + \
        SPRITES[RoomType.TREASURE] + ' Treasure' + gap + \
        SPRITES[RoomType.EMPTY] + ' Empty' + gap + \
        SPRITES[RoomType.SAFE] + ' Safe' \
    )
    print( \
        SPRITES[RoomType.GUARDED_TREASURE] + ' Guarded Treasure' + gap + \
        SPRITES[RoomType.HAZARD] + ' Hazard' + gap + \
        SPRITES[RoomType.DEATH] + ' Death' + gap + \
        SPRITES[RoomType.ENEMY] + ' Enemy Encounter' \
    )
    print('')

    # Render dungeon
    border = '*' + ('~' * 4 * DEFAULT_DUNGEON_SIZE) + '*'
    print(border)
    print('')
    for row in dungeon._rooms:
        if not all(room.room_type == RoomType.NONE for room in row):
            row_render = ' '
            hall_row_render = ' '
            for room in row:
                right_hall = '__' if room.right_door_exists else '  '
                row_render = row_render + SPRITES[room.room_type] + right_hall
                down_hall = ' |' if room.down_door_exists else '  '
                hall_row_render = hall_row_render + down_hall + '  '
            print(row_render)
            print(hall_row_render)
    print(border)
    print('')


if __name__ == "__main__":
    main()
