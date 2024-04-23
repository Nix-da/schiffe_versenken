import socket
import threading

class Peer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        self.client = None
        self.address = None

    def accept_connection(self):
        self.client, self.address = self.server.accept()
        print(f"Connection established with {self.address}")

    def start_receiving(self):
        while True:
            data = self.client.recv(1024)
            print(f"Received: {data.decode('utf-8')}")

    def start_sending(self):
        while True:
            data = input("Enter message: ")
            self.client.send(data.encode('utf-8'))

    def start(self):
        self.accept_connection()
        threading.Thread(target=self.start_receiving).start()
        threading.Thread(target=self.start_sending).start()


p = Peer()