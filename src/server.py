import socket
import threading


class Server:
    def __init__(self, host, port=12345):
        self.s = socket.socket()
        self.host = host
        self.port = port
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        self.clients = []
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        self.buffer = []

    def run(self):
        while True:
            c, addr = self.s.accept()
            self.clients.append((c, addr))
            print(f"Server connected to: {addr}")
            self.buffer.append("connected,"+str(addr))
            client_thread = threading.Thread(target=self.handle_client, args=(c,))
            client_thread.start()

    def handle_client(self, client):
        while True:
            message = self.receive_message(client)
            if message:
                print(f"Server Received: {message}")
                self.buffer.append(message)

    def send_message(self, client, message):
        client.sendall(message.encode("utf-8"))

    def receive_message(self, client):
        return client.recv(1024).decode("utf-8")

    def close_connection(self):
        for client, _ in self.clients:
            client.close()
        self.s.close()
