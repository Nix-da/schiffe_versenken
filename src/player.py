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
                ship.coordinates.append((x + i, y))
                ship.coordinate_states.append(1)
        elif orientation == 'vertical':
            for i in range(ship.length):
                self.grid[y + i][x] = 1
                ship.coordinates.append((x, y + i))
                ship.coordinate_states.append(1)
        ship.state = 1

        return True

    def attack(self, x, y):
        if self.enemy_grid[y][x] > 0:
            print("You already attacked this position")
            return False
        if self.enemy_grid[y][x] == 0:
            self.enemy_grid[y][x] = 1
            '''for ship in self.enemy_ships:
                for i in range(len(ship.coordinates)):
                    if ship.coordinates[i] == (x, y):
                        ship.coordinate_states[i] = 1
                        if all(ship.coordinate_states):
                            ship.state = 1
                            print(f'{ship} was destroyed')'''
            return True
        return False


p = Player('Player 1')
print(p.grid)
p.place_ship(p.ships['battleship'][0], 6, 0, 'horizontal')
print(p.grid)
