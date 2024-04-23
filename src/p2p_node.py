from pythonp2p import Node
from pythonp2p.node import PORT
from player import Player


class P2PNode(Node):

    def __init__(self, host='localhost', player=None):
        super().__init__(host)
        self.player = player
        self.buffer = []
        self.start()

    def on_message(self, message, sender, private):
        self.buffer.append(message)

    def connect_to(self, host, port=PORT):
        super().connect_to(host, port)

    def send_message(self, message, reciever=None):
        super().send_message(message, reciever)
