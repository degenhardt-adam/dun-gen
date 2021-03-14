"""Generates one encounter"""


__author__ = "Adam Degenhardt"


from enum import Enum, unique
from random import choice, randrange, shuffle


@unique
class Difficulty(Enum):
    EASY = 0
    INTERMEDIATE = 1
    DIFFICULT = 2


class Enemy():
    """Represents one enemy in an encounter"""
    def __init__(self, arcana, level):
        self.arcana = arcana
        self.level = level # Level above or below dungeon's world level


class Encounter():
    """Represents one encounter in an encounter room"""

    def __init__(self, arcana, name):
        # Which arcana are on this floor
        self._arcana = arcana
        self.name = name
        self._enemies = []

    def generate_enemies(self, difficulty):
        assert(difficulty in [d for d in Difficulty])

        if difficulty == Difficulty.EASY:
            option = randrange(1, 4)
            if option == 1:
               self._enemies.append(Enemy(choice(self._arcana), 1))
            elif option == 2:
               self._enemies.append(Enemy(choice(self._arcana), 0))
               self._enemies.append(Enemy(choice(self._arcana), -1))
            elif option == 3:
               self._enemies.append(Enemy(choice(self._arcana), -1))
               self._enemies.append(Enemy(choice(self._arcana), -1))

        elif difficulty == Difficulty.INTERMEDIATE:
            option = randrange(1, 4)
            if option == 1:
               self._enemies.append(Enemy(choice(self._arcana), 1))
               self._enemies.append(Enemy(choice(self._arcana), 1))
            elif option == 2:
               self._enemies.append(Enemy(choice(self._arcana), 0))
               self._enemies.append(Enemy(choice(self._arcana), 0))
               self._enemies.append(Enemy(choice(self._arcana), -1))
            elif option == 3:
               self._enemies.append(Enemy(choice(self._arcana), -1))
               self._enemies.append(Enemy(choice(self._arcana), -1))
               self._enemies.append(Enemy(choice(self._arcana), -1))

        elif difficulty == Difficulty.DIFFICULT:
            option = randrange(1, 4)
            if option == 1:
               self._enemies.append(Enemy(choice(self._arcana), 1))
               self._enemies.append(Enemy(choice(self._arcana), 0))
               self._enemies.append(Enemy(choice(self._arcana), 0))
            elif option == 2:
               self._enemies.append(Enemy(choice(self._arcana), 0))
               self._enemies.append(Enemy(choice(self._arcana), 0))
               self._enemies.append(Enemy(choice(self._arcana), -1))
               self._enemies.append(Enemy(choice(self._arcana), -1))
            elif option == 3:
               self._enemies.append(Enemy(choice(self._arcana), -1))
               self._enemies.append(Enemy(choice(self._arcana), -1))
               self._enemies.append(Enemy(choice(self._arcana), -1))
               self._enemies.append(Enemy(choice(self._arcana), -1))

        shuffle(self._enemies)

    def renderHTML(self):
        assert(len(self._enemies) > 0)
        enemies_string = ''
        for enemy in self._enemies:
            level_string = ''
            if enemy.level == 1:
                level_string = ' (WL+1)'
            elif enemy.level == 0:
                level_string = ' (WL)'
            elif enemy.level == -1:
                level_string = ' (WL-1)'
            enemies_string = enemies_string + enemy.arcana.value + level_string + ', '
        enemies_string = enemies_string[0: -2]
        return '<pre> {}. '.format(self.name) + enemies_string + '<br /></pre>'
        
