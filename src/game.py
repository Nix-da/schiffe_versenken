from player import Player
from server import Server
import socket


class Game:

    def __init__(self):
        self.server = None
        self.players = []
        self.player_on_turn = 0
        self.phase = 0  # 0 = connecting, 1 = placing ships, 2 = attacking, 3 = game over

    def reset(self):
        self.phase = 1
        self.player_on_turn = 0

    def get_phase(self):
        return self.phase

    def host_game(self, port=12345):
        self.server = Server(self.get_my_ip(), port)

        ip = self.get_my_ip()
        self.players.append(Player("host", ip, port))

        return self.get_my_ip()

    def connect_to_game(self, ip, port=12345):
        self.players.append(Player("host", ip, port))
        self.phase = 1

    def disconnect(self):
        self.server.close_connection()
        self.players = []
        self.player_on_turn = 0
        self.phase = 0



    def handle_server_messages(self):
        if self.server.buffer:
            message = self.server.buffer.pop(0).split(",")
            if message[1] == "attack":
                x, y = int(message[2]), int(message[3])
                self.players[self.player_on_turn].attack(self.players[not self.player_on_turn], x, y)
                self.player_on_turn = not self.player_on_turn
                print("Other players turn")
            if message[0] == "connected":
                self.players.append(Player("guest", message[1]))
                self.phase = 1
                print("all Players connected")
