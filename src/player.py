import numpy as np
from ships import *
from GUI_constants import *
import ast


class Player:
    def __init__(self, name):
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

        self.node = None
        self.on_turn = True


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
        # print("placed ship at" + str((x, y)) + " with orientation " + orientation)
        return True

    def all_ships_placed(self):
        for ships in self.ships.values():
            for ship in ships:
                if ship.state == 0:
                    return False
        return True

    def on_attack(self, x, y):
        # if there is a ship in this position
        if self.get_coordinate_state(x, y) >= 1:
            ship = self.get_coordinate_ship(x, y)
            ship.hit(x, y)

            # if this ship is sunk
            if ship.state == 3:
                for coord in ship.coordinates:
                    self.grid[coord[0]][coord[1]] = 3
                print(ship.__class__.__name__ + " sunk!")
                if all(ship.state == 3 for ship in self.get_ships_list()):
                    print("You lost!")
                return "result;sunk;" + str(x) + ";" + str(y) + ";" + ship.__class__.__name__ + ";" + str(ship.coordinates)
            else:
                self.grid[x][y] = 2
                return "result;hit;" + str(x) + ";" + str(y)
        # if there is no ship in this position
        else:
            #self.grid[x][y] = 1
            return "result;miss;" + str(x) + ";" + str(y)

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
        try:
            message = message.split(";")
            # actions
            if message[0] == "action":
                if message[1] == "attack":
                    result = self.on_attack(int(message[2]), int(message[3]))
                    self.on_turn = True
                    print("your turn")
                    print(" ")
                    print(" ")
                    self.node.send_message(result)
            # results
            if message[0] == "result":
                self.on_turn = False
                if message[1] == "miss":
                    print("return missed")
                    self.enemy_grid[int(message[2])][int(message[3])] = 1
                if message[1] == "hit":
                    print("return hit")
                    self.enemy_grid[int(message[2])][int(message[3])] = 2
                if message[1] == "sunk":
                    print("return sunk")
                    string_coords = ast.literal_eval(message[5])
                    coords = [ast.literal_eval(t) for t in string_coords]
                    for coord in coords:
                        print(coord)
                        self.enemy_grid[coord[0]][coord[1]] = 3

        except:
            pass
