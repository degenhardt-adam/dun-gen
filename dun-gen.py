from enum import Enum, unique
from random import randrange


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


class Deck():
    _cards = \
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

MAX_HALLWAY_LENGTH = 5
DUNGEON_SIZE = 15

@unique
class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class Room:
    right_door_exists = False
    down_door_exists = False
    room_type = RoomType.NONE


def main():
    
    deck = Deck()

    dungeon = [[Room() for i in range(DUNGEON_SIZE)] for j in range(DUNGEON_SIZE)]

    x = DUNGEON_SIZE / 2
    y = DUNGEON_SIZE / 2
    hall_length = 1
    stairs_drawn = False
    cards_drawn = 0

    def can_build_direction(direction):
        for i in range(1, MAX_HALLWAY_LENGTH):
            if direction == Direction.RIGHT:
                if x + i >= DUNGEON_SIZE:
                    return False
                if dungeon[y][x + i].room_type != RoomType.NONE:
                    return False
            elif direction == Direction.LEFT:
                if x - i < 0:
                    return False
                if dungeon[y][x - i].room_type != RoomType.NONE:
                    return False
            elif direction == Direction.UP:
                if y - i < 0:
                    return False
                if dungeon[y - i][x].room_type != RoomType.NONE:
                    return False
            elif direction == Direction.DOWN:
                if y + i >= DUNGEON_SIZE:
                    return False
                if dungeon[y + i][x].room_type != RoomType.NONE:
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

    dungeon[y][x].room_type = RoomType.START
    while not (cards_drawn >= 7 and stairs_drawn):
        # Make a door and move to the next position
        if direction == Direction.RIGHT:
            dungeon[y][x].right_door_exists = True
            x = x + 1
        elif direction == Direction.DOWN:
            dungeon[y][x].down_door_exists = True
            y = y + 1
        elif direction == Direction.LEFT:
            x = x - 1
            assert(x >= 0)
            dungeon[y][x].right_door_exists = True
        elif direction == Direction.UP:
            y = y - 1
            assert(y >= 0)
            dungeon[y][x].down_door_exists = True

        # Add a card to the dungeon
        room = deck.draw()
        if room == RoomType.STAIRCASE:
            if stairs_drawn:
                room = RoomType.SAFE
            else:
                stairs_drawn = True
        dungeon[y][x].room_type = room
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
    border = '*' + ('~' * 4 * DUNGEON_SIZE) + '*'
    print(border)
    print('')
    for row in dungeon:
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
