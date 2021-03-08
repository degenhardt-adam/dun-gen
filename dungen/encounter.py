"""Generates one encounter"""


__author__ = "Adam Degenhardt"


from enum import Enum, unique


@unique
class Difficulty(Enum):
    EASY = 0
    INTERMEDIATE = 1
    DIFFICULT = 2


class Encounter():
    """Represents one encounter in an encounter room"""

    # Iterated every time we make a new encounter
    next_id = 1

    def __init__(self, arcana):
        # Which arcana are on this floor
        self._arcana = arcana
        self.id = Encounter.next_id
        Encounter.next_id = Encounter.next_id + 1

    def generate_enemies(self, difficulty):
        assert(difficulty in [d for d in Difficulty])
        if difficulty == Difficulty.EASY:
            self._enemies = "Easy encounter"
        elif difficulty == Difficulty.INTERMEDIATE:
            self._enemies = "Intermediate encounter"
        elif difficulty == Difficulty.DIFFICULT:
            self._enemies = "Hard encounter"

    def renderHTML(self):
        assert(self._enemies is not None)
        return '<pre>' + self._enemies + '<br /></pre>'
        
