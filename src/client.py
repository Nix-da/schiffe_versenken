import socket


def start_client(ip, port=12345):
    s = socket.socket()  # Create a socket object
    host = ip

    s.connect((host, port))
    s.send(b'Hello server!')

    # receive data from the server
    print(s.recv(1024))
    # close the connection
    #s.close()


def send_message(server, message):
    # convert the message to bytes
    message = message.encode('utf-8')
    # send the message
    server.send(message)
