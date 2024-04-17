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
        self.enemy_ships = {
            'battleship': [Battleship()],
            'cruiser': [Cruiser(), Cruiser()],
            'submarine': [Submarine(), Submarine(), Submarine()],
            'destroyer': [Destroyer(), Destroyer(), Destroyer(), Destroyer()]
        }

    def place_ship(self, ship, x, y, orientation):
        if x + ship.length > 10 and orientation == 'horizontal':
            print("Ship can't be placed here")
            return False
        if y + ship.length > 10 and orientation == 'vertical':
            print("Ship can't be placed here")
            return False

        if orientation == 'horizontal':
            for i in range(ship.length):
                self.grid[y][x + i] = 1
                ship.state = 1
                ship.coordinates.append((x + i, y))
                ship.coordinate_states.append(1)
        elif orientation == 'vertical':
            for i in range(ship.length):
                self.grid[y + i][x] = 1
                ship.state = 1
                ship.coordinates.append((x, y + i))
                ship.coordinate_states.append(1)
        ship.state = 1

        return True

    def attack(self, enemy, x, y):
        # if cell is already attacked
        if self.enemy_grid[x][y] > 0:
            print("You already attacked this position")
            return False

        # if cell is unknown
        if self.enemy_grid[x][y] == 0:

            # if the enemy has a ship in this position
            if enemy.grid[x][y] == 1:
                self.enemy_grid[x][y] = 2
                print("Hit!")
                #for ship in enemy.ships:
                    #for coord in ship.coordinates:


                return True

            # if the enemy doesn't have a ship in this position
            self.enemy_grid[x][y] = 1
            print("Miss!")
            return True
        return False

    def get_coordinate_state(self, x, y):
        return self.grid[x][y]

    def get_coordinate_ship(self, x, y):
        for ship in self.ships:
            for coord in ship.coordinates:
                if coord == (x, y):
                    return ship
