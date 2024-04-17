import numpy as np
from ships import *


class Player:
    def __init__(self, name):
        self.name = name
        self.grid = np.zeros((10, 10))
        self.enemy_grid = np.zeros((10, 10))
        self.ships = {
            'battleship': [Battleship()],
            'cruiser': [Cruiser(), Cruiser()],
            'submarine': [Submarine(), Submarine(), Submarine()],
            'destroyer': [Destroyer(), Destroyer(), Destroyer(), Destroyer()]
        }

