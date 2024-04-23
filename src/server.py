import socket
import threading

class Server:
    def __init__(self, host, port):
        self.s = socket.socket()
        self.host = host
        self.port = port
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        self.c, self.addr = self.s.accept()
        while True:
            message = self.receive_message()
            if message:
                print(f"Server Received: {message}")

    def send_message(self, message):
        self.c.sendall(message.encode("utf-8"))

    def receive_message(self):
        return self.c.recv(1024).decode("utf-8")

    def close_connection(self):
        self.s.close()
        self.c.close()