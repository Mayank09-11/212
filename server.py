import socket
import threading
import os
import ftplib
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def start_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", ".", perm="elradfmw")
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(("0.0.0.0", 21), handler)
    server.serve_forever()

class MusicServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        print("Server started, waiting for clients...")
        self.clients = []

    def broadcast(self, msg, conn):
        for client in self.clients:
            if client != conn:
                try:
                    client.send(msg)
                except:
                    self.clients.remove(client)

    def handle_client(self, conn, addr):
        print(f"New connection {addr}")
        self.clients.append(conn)
        connected = True
        while connected:
            try:
                msg = conn.recv(1024)
                if msg:
                    print(f"{addr} says: {msg}")
                    self.broadcast(msg, conn)
                else:
                    connected = False
            except:
                connected = False
        conn.close()

    def start(self):
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    ftp_thread = threading.Thread(target=start_ftp_server)
    ftp_thread.start()
    music_server = MusicServer()
    music_server.start()
