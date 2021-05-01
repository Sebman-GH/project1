import socket
import threading
import os

BUFFER = 32
PORT = 6067
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.0.105"
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "/disconnect"
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"NEW CONNECTION FROM: {addr}")
    while True:
        try:
            chs_temp = conn.recv(1)
            if chs_temp == b"1": msg_recv(conn,addr)
            if chs_temp == b"2": file_recv(conn,addr)
        except:
            print(f"User {addr} has disconnected.Active connections {threading.activeCount() - 2}")
            break

def msg_recv(conn,addr):

    msg_lenth = conn.recv(BUFFER).decode(FORMAT)
    if msg_lenth:
        msg_lenth = int(msg_lenth)
        msg = conn.recv(msg_lenth).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            print(f"User {addr} has disconnected.Active connections: {threading.activeCount() - 2}")
        else: 
            print(f"[{addr}]: {msg}")

def file_recv(conn,addr):
    try:
        filename_lenth = int(conn.recv(BUFFER))
        filename = str(conn.recv(filename_lenth).decode('utf-8'))
        print(f'Receiving new file {filename} from {addr}...')
        file_lenth = int(conn.recv(BUFFER))
        with open(filename, 'wb+') as file:
            data_count = 0
            file_data = conn.recv(16)
            file.write(file_data)
            data_count += 16
            while data_count < file_lenth:
                file_data = conn.recv(16)
                file.write(file_data)
                data_count += 16
        file.close
        print(f"New file {filename} from {addr} received!")
        if conn.recv(1) == b'y':
            os.system(f"start {filename}")
        else:
            pass
    except:
        print(f"New file {filename} not received.")
    

def start():
    server.listen()
    print(f"Server started on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active connections: { threading.activeCount() - 1 } ")

print("Server is starting")
start()
