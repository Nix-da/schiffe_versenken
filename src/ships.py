from abc import ABC, abstractmethod


class Ship(ABC):
    def __init__(self, coordinates=None):
        self.length = self.get_length()
        self.coordinates = []
        self.state = 0
        # state 0: not placed
        # state 1: placed
        # state 2: hit
        # state 3: sunk
        self.coordinate_states = []

    @abstractmethod
    def get_length(self):
        pass


    def hit(self, x, y):
        index = self.coordinates.index((x, y))
        self.coordinate_states[index] = 2
        self.state = 2
        if self.coordinate_states.count(2) == self.length:
            self.state = 3
            self.coordinate_states = [3] * self.length
            return True


class Battleship(Ship):
    def get_length(self):
        return 5


class Cruiser(Ship):
    def get_length(self):
        return 4


class Destroyer(Ship):
    def get_length(self):
        return 3


class Submarine(Ship):
    def get_length(self):
        return 2
