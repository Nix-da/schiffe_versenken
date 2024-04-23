import numpy as np
from ships import *
from GUI_constants import *


class Player:
    def __init__(self, name, node):
        self.name = name
        self.grid = np.zeros((10, 10))
        self.enemy_grid = np.zeros((10, 10))
        self.ships = {
            'battleship': [Battleship()],
            'cruiser': [Cruiser(), Cruiser()],
            'destroyer': [Destroyer(), Destroyer(), Destroyer()],
            'submarine': [Submarine(), Submarine(), Submarine(), Submarine()]
        }
        self.enemy_ships = {
            'battleship': [Battleship()],
            'cruiser': [Cruiser(), Cruiser()],
            'destroyer': [Destroyer(), Destroyer(), Destroyer()],
            'submarine': [Submarine(), Submarine(), Submarine(), Submarine()]
        }

        self.node = node


    def place_ship(self, ship, x, y, orientation):
        if orientation == 'horizontal':
            if x + ship.length > 10:
                return False
            blockings = [self.grid[y][max(0, x - 1):min(x + ship.length + 1, GRID_SIZE)],
                         self.grid[max(0, y - 1)][x:x + ship.length],
                         self.grid[min(y + 1, GRID_SIZE - 1)][x:x + ship.length]]
            if [item for sublist in blockings for item in sublist].count(1) > 0:
                return False
        if orientation == 'vertical':
            if y + ship.length > 10:
                return False
            blockings = [self.grid[max(0, y - 1):min(y + ship.length + 1, GRID_SIZE), x],
                         self.grid[y:y + ship.length, max(0, x - 1)],
                         self.grid[y:y + ship.length, min(x + 1, GRID_SIZE - 1)]]
            if [item for sublist in blockings for item in sublist].count(1) > 0:
                return False

        if orientation == 'horizontal':
            for i in range(ship.length):
                self.grid[y][x + i] = 1
                ship.state = 1
                ship.coordinates.append((y, x + i))
                ship.coordinate_states.append(1)
        elif orientation == 'vertical':
            for i in range(ship.length):
                self.grid[y + i][x] = 1
                ship.state = 1
                ship.coordinates.append((y + i, x))
                ship.coordinate_states.append(1)
        ship.state = 1
        #print("placed ship at" + str((x, y)) + " with orientation " + orientation)
        return True

    def all_ships_placed(self):
        for ships in self.ships.values():
            for ship in ships:
                if ship.state == 0:
                    return False
        return True

    def attack(self, enemy, x, y):
        # if cell is already attacked
        if self.enemy_grid[x][y] > 0:
            print("You already attacked this position")
            return False

        # if cell is unknown
        if self.enemy_grid[x][y] == 0:

            # if the enemy has a ship in this position
            if enemy.get_coordinate_state(x, y) == 1:
                enemy_ship = enemy.get_coordinate_ship(x, y)
                enemy_ship.hit(x, y)
                if enemy_ship.state == 3:
                    for coord in enemy_ship.coordinates:
                        self.enemy_grid[coord[0]][coord[1]] = 3
                    print(enemy_ship.__class__.__name__ + " sunk!")
                    if all(ship.state == 3 for ship in enemy.get_ships_list()):
                        print("You win!")
                else:
                    self.enemy_grid[x][y] = 2
                    print("Hit!")
                return True

            # if the enemy doesn't have a ship in this position
            self.enemy_grid[x][y] = 1
            print("Miss!")
            return True
        return False

    def get_coordinate_state(self, x, y):
        return self.grid[x][y]

    def get_coordinate_ship(self, x, y):
        for ships in self.ships.values():
            for ship in ships:
                for coord in ship.coordinates:
                    if coord == (x, y):
                        return ship

    def get_ships_list(self):
        return [ship for ships in self.ships.values() for ship in ships]

    def parse_message(self, message):
        command, *args = message.split(",")
        if command == "attack":
            x, y = map(int, args)
            return self.attack(self.node, x, y)
        return False