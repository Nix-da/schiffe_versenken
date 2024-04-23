from pythonp2p import Node
from pythonp2p.node import PORT


class P2PNode(Node):

    def __init__(self):
        super().__init__()
        self.name = "MyNode"
        self.start()

    def on_message(message, sender, private):
        print(f"Received message from {sender}: {message}")
        # Gets called everytime there is a new message

    def connect_to(self, host, port=PORT):
        print("Connecting to", host, port)
        super().connect_to(host, port)

    def send_message(self, message, reciever=None):
        super().send_message(message, reciever)


node = P2PNode()
node.connect_to('192.178.168.128')
#node = Node()  # start the node
#node.start()

