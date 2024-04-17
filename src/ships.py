from abc import ABC, abstractmethod


class Ship(ABC):
    def __init__(self, coordinates=None):
        self.length = self.get_length()
        self.coordinates = []
        self.state = 0
        self.coordinate_states = []

    @abstractmethod
    def get_length(self):
        pass


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
