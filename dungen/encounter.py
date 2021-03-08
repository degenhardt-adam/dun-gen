"""Generates one encounter"""


__author__ = "Adam Degenhardt"


class Encounter():
    """Represents one encounter in an encounter room"""

    # Iterated every time we make a new encounter
    next_id = 1

    def __init__(self, arcana):
        # Which arcana are on this floor
        self._arcana = arcana
        self.id = Encounter.next_id
        Encounter.next_id = Encounter.next_id + 1

    def generate(self, difficulty):
        self._enemies = "This is where enemies would go... IF I HAD ANY"

    def renderHTML(self):
        assert(self._enemies is not None)
        return '<pre>' + self._enemies + '<br /></pre>'
        
