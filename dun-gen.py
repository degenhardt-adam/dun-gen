from enum import Enum, unique
from random import randrange


@unique
class Room(Enum):
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


SPRITES = {
    Room.NONE: '  ',
    Room.STAIRCASE: '//',
    Room.TREASURE: '$$',
    Room.EMPTY: '[]',
    Room.SAFE: '<3',
    Room.GUARDED_TREASURE: 'X$',
    Room.HAZARD: '/\\',
    Room.DEATH: '8X',
    Room.ENEMY: '\\O',
    Room.START: '\\\\'
}


@unique
class Direction(Enum):
    RIGHT = 0
    DOWN = 1


def main():
    cards = \
        [Room.STAIRCASE] * 2 + \
        [Room.TREASURE] * 4 + \
        [Room.EMPTY] * 3 + \
        [Room.SAFE] * 2 + \
        [Room.GUARDED_TREASURE] + \
        [Room.HAZARD] * 2 + \
        [Room.DEATH] + \
        [Room.ENEMY] * 7
    
    def draw():
        return cards.pop(randrange(len(cards)))
    
    rows, columns = (16, 16)
    dungeon = [[Room.NONE for i in range(columns)] for j in range(rows)]

    x = 0
    y = 0
    direction = Direction.DOWN
    hall_length = 1
    stairs_drawn = False
    cards_drawn = 0

    dungeon[y][x] = Room.START
    while not (cards_drawn >= 7 and stairs_drawn):
        # Move to the next position
        if direction == Direction.RIGHT:
            x = x + 1
        elif direction == Direction.DOWN:
            y = y + 1

        # Add a card to the dungeon
        room = draw()
        if room == Room.STAIRCASE:
            if stairs_drawn:
                room = Room.SAFE
            else:
                stairs_drawn = True
        dungeon[y][x] = room
        hall_length = hall_length + 1
        cards_drawn = cards_drawn + 1

        # Branch if we need to
        if hall_length >= 5:
            if direction == Direction.RIGHT:
                x = x - randrange(1, 4)
                direction = Direction.DOWN
            elif direction == Direction.DOWN:
                y = y - randrange(1, 4)
                direction = Direction.RIGHT
            hall_length = 1

    # Render dungeon
    for row in dungeon:
        if not all(room == Room.NONE for room in row):
            row_render = ''
            for room in row:
                row_render = row_render + SPRITES[room] + ' '
            print(row_render)


if __name__ == "__main__":
    main()
