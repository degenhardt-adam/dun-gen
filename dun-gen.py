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
    
    while len(cards) > 0:
        print(draw())
        


if __name__ == "__main__":
    main()
