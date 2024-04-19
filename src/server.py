import socket


def start_server(ip, port=12345):
    host = ip  # Host IP

    s = socket.socket()  # Create a socket object
    s.bind((host, port))  # Bind to the port

    s.listen(5)  # Now wait for client connection
    print('Server listening....')

    while True:
        conn, addr = s.accept()  # Establish connection with client
        print(f'Got connection from {addr}')
        data = conn.recv(1024)
        print(f'Received {repr(data)}')

        conn.send(b'Thank you for connecting')
        #conn.close()
