import socket
import threading


class Client:
    def __init__(self, host, port=12345):
        self.s = socket.socket()
        self.host = host
        self.port = port
        self.s.connect((self.host, self.port))
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            message = self.receive_message()
            if message:
                print(f"Client Received: {message}")

    def send_message(self, message):
        self.s.sendall(message.encode("utf-8"))

    def receive_message(self):
        return self.s.recv(1024).decode("utf-8")

    def close_connection(self):
        self.s.close()