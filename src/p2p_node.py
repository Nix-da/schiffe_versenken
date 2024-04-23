from pythonp2p import Node
from pythonp2p.node import PORT


class P2PNode(Node):

    def __init__(self, host='localhost'):
        super().__init__(host)
        self.buffer = []
        self.start()

    def on_message(self, message, sender, private):
        self.buffer.append(message)

    def connect_to(self, host, port=PORT):
        super().connect_to(host, port)
        self.buffer.append("connected," + host + "," + str(port))

    def send_message(self, message, reciever=None):
        super().send_message(message, reciever)


node = P2PNode('192.168.178.20')
node.connect_to('192.168.178.128')
node.send_message("pc to laptop")

