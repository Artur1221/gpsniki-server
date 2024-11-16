import socket
from threading import Thread

class Server:
    clients = []

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 8080))
        self.socket.listen(100)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket_t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_t.bind(('', 6700))
        self.socket_t.listen(100)

        self.socket_t.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def listen(self):
        print('listening')
        while True:
            conn, addr = self.socket.accept()

            Server.clients.append(conn)
            Thread(target=self.handle_new_client, args=(conn,)).start()

    def handle_new_client(self, conn):
        print('new client')
        while True:
            conn_t, addr_t = self.socket_t.accept()

            message = conn_t.recv(2**20)

            login_bytes = bytes([0x23, 0x41, 0x4c, 0x23, 0x31, 0x0d, 0x0a])

            conn_t.send(login_bytes)

            message = conn_t.recv(2**20)

            self.broadcast(message)
            
            pkg_amt = len(bytes.fromhex(message.hex(" ")).decode('ascii').split('|')) - 1
            
            conn_t.send(bytes([0x23, 0x41, 0x42, 0x23, 0x30 + pkg_amt, 0x0d, 0x0a]))

            conn_t.close()
    
    def broadcast(self, message):
        print('broadcasting')
        for client in self.clients:
            client.send(message)

server = Server()
server.listen()

