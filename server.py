import socket
import threading
import os

HEADER = 16
PORT = 6067
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    DISCONNECT_MESSAGE = "/disconnect"
    print(f"NEW CONNECTION FROM: {addr}")
    connected = True
    while connected == True:
        try:
            msg_lenth = conn.recv(HEADER).decode(FORMAT)
            if msg_lenth:
                msg_lenth = int(msg_lenth)
                msg = conn.recv(msg_lenth).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"User {addr} has disconnected.Active connections: { threading.activeCount() - 2 }")
                else: 
                    print(f"[{addr}]: {msg}")
        except:
            connected = False
            print(f"User {addr} has disconnected.Active connections: { threading.activeCount() - 2 }")

def start():
    server.listen()
    print(f"Server started on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr,))
        thread.start()
        print(f"Active connections: { threading.activeCount() - 1 } ")

print("Server is starting")
start()