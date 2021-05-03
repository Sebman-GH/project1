import socket
import threading
import os
import subprocess
from re import search
sock_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

class Server_func():
    def __init__(self, SERVER, PORT, BUFFER, FORMAT, DISCONNECT_MESSAGE):
        self.SERVER = SERVER
        self.PORT = PORT
        self.BUFFER = BUFFER
        self.FORMAT = FORMAT
        self.DISCONNECT_MESSAGE = DISCONNECT_MESSAGE

    def handle_client(self, conn, addr):
        print(f"NEW CONNECTION FROM: {addr}")
        while True:
            try:
                chs_temp = conn.recv(1)
                if chs_temp == b"1": self.msg_recv(conn, addr)
                if chs_temp == b"2": self.file_recv(conn, addr)
                if chs_temp == b"3": self.cmd_execute(conn, addr)
            except:
                print(f"User {addr} has disconnected.Active connections {threading.activeCount() - 2}")
                break

    def lenth_sending(self, string):
            string_lenth = str(len(string)).encode(self.FORMAT)
            string_lenth += b' ' * (self.BUFFER - len(string_lenth))
            return string_lenth

    def msg_recv(self, conn, addr):
        try:
            msg_lenth = int(conn.recv(self.BUFFER).decode(self.FORMAT))
            msg = conn.recv(msg_lenth).decode(self.FORMAT)
            if msg == self.DISCONNECT_MESSAGE:
                print(f"User {addr} has disconnected.Active connections: {threading.activeCount() - 2}")
            else: 
                print(f"[{addr}]: {msg}")
        except:
            print("Cant get message")

    def file_recv(self, conn, addr):
        try:
            filename_lenth = int(conn.recv(self.BUFFER).decode(self.FORMAT))
            filename = conn.recv(filename_lenth).decode(self.FORMAT)
            print(f'Receiving new file {filename} from {addr}...')
            file_lenth = int(conn.recv(self.BUFFER))

            with open(filename, 'wb+') as file:
                file_data = conn.recv(self.BUFFER)
                file.write(file_data)
                data_count = self.BUFFER

                while data_count < file_lenth:
                    file_data = conn.recv(self.BUFFER)
                    file.write(file_data)
                    data_count += self.BUFFER
            file.close
            print(f"New file {filename} from {addr} received!")
            
            if conn.recv(1) == b'y':
                #os.system(f"start {filename}")
                subprocess.run(["start", filename])
            else:
                pass
        except:
            print(f"New file {filename} not received.")

    def cmd_execute(self, conn, addr):
        try:
            cmd_command_lenth = int(conn.recv(self.BUFFER).decode(self.FORMAT))
            cmd_command = conn.recv(cmd_command_lenth).decode(self.FORMAT)
            if "format" in cmd_command or "shutdown" in cmd_command or "erase" in cmd_command: cmd_command = "echo Cant execute this command"
            output = subprocess.run(cmd_command, shell = True, stdout = subprocess.PIPE)
            output = output.stdout.decode("cp866")
            conn.send(self.lenth_sending(output.encode(self.FORMAT)))
            conn.send(output.encode(self.FORMAT))
        except:
            print("Cant execute command")

    def start(self):
        try:
            ADDR = (self.SERVER, self.PORT)
            sock_server.bind(ADDR)
            sock_server.listen()
            print(f"Server started on {self.SERVER}")
        except:
            print("Failed to start server! Maybe server already started? ")
            os.system("pause")
            exit()
        while True:
            try:
                conn, addr = sock_server.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                print(f"Active connections: { threading.activeCount() - 1 } ")
            except:
                print(f"Active connections: {threading.activeCount() - 1} " )

if __name__ == "__main__":
    print("Server is starting...")
    try:
        server_ip = socket.gethostbyname_ex(socket.gethostname())[2][1]
        print("Choosed ip: " + server_ip)
    except IndexError:
        server_ip = socket.gethostbyname(socket.gethostname())
        print("Choosed ip: " + server_ip)
    server = Server_func(server_ip, 6067, 16, 'utf-8', "/disconnect")
    server.start()