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

    def host_game(self):
        self.server = Server(self.get_my_ip())

        ip = self.get_my_ip()
        self.players.append(Player("host", ip))

        return self.get_my_ip()

    def connect_to_game(self, ip):
        self.players.append(Player("host", ip))
        self.players.append(Player("guest", self.get_my_ip()))
        self.phase = 1

    def disconnect(self):
        self.server.close_connection()
        self.players = []
        self.player_on_turn = 0
        self.phase = 0

    def get_my_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
