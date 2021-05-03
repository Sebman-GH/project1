import socket
import os
from time import sleep

sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Client_func():

    def __init__(self, PORT, BUFFER, FORMAT):
        self.PORT = PORT
        self.BUFFER = BUFFER
        self.FORMAT = FORMAT

    def main_menu(self, *fst_start):
        try:
            if fst_start[0] == True:
                SERVER = input("Input the server IP you would like to connect:")
                if SERVER == "l": SERVER = "192.168.0.102"
                ADDR = (SERVER,self.PORT)
                print("Connecting...")
                try:
                    sock_client.connect(ADDR)
                    print("Connected to the server.")
                    sleep(0.5)
                except:
                    print("Failed connect to the server!")
                    sleep(1)
                    self.main_menu(True)
        except IndexError:
            pass
        chs_temp = input("Choose the option: \n 1.Send the message \n 2.Send file to the server \n 3.Send command in cmd \n 4.All commands in the program (/help) \n")
        if chs_temp == "/disconnect": self.send_message("/disconnect")
        elif chs_temp == '1': self.send_message()
        elif chs_temp == '2': self.send_file()
        elif chs_temp == '3': self.cmd_input()
        elif chs_temp == '4': self.help_list()
        else: 
            print("Wrong input!")
            self.main_menu()

    def send_message(self, *msg):
        while True:
            if msg == (): msg = input("Enter what you would like to send:")
            if msg == "/return": self.main_menu()
            if type(msg) == tuple: msg = msg[0]
            try:
                sock_client.send(b"1")
                message = msg.encode(self.FORMAT)
                sock_client.send(self.lenth_sending(message))
                sock_client.send(message)
                print("Message sent successfull")
            except: 
                print("Failed to send message")
                self.main_menu(True)
            if msg == "/disconnect": 
                quit()
            msg = ()

    def send_file(self):
        os.system("dir")
        filename = input("Enter file name what you would like to send(in same directory): ")
        if filename == "/disconnect": self.send_message("/disconnect")
        elif filename == "/return": self.main_menu()
        try:
            sock_client.send(b"2")
            with open(filename,'rb') as file:
                data = file.read()

                sock_client.send(self.lenth_sending(filename.encode(self.FORMAT)))
                sock_client.send(filename.encode(self.FORMAT))

                sock_client.send(self.lenth_sending(data))
                for i in range(0,len(data),self.BUFFER):
                    sock_client.send((data[i : i + self.BUFFER]))

                if input("Open file after sending? (y/n)\n") == 'y': sock_client.send(b'y')
                else: sock_client.send(b'n')
                print("File sent")
                file.close()
        except:
            print("Failed to send or open file.")
        self.main_menu()

    def lenth_sending(self, string):
            string_lenth = str(len(string)).encode(self.FORMAT)
            string_lenth += b' ' * (self.BUFFER - len(string_lenth))
            return string_lenth

    def cmd_input(self):
        try:
            cmd_command = input("Enter command you would to execute: ")
            if cmd_command == "/return": self.main_menu()
            elif cmd_command == "/disconnect": self.send_message("/disconnect")

            sock_client.send(b"3")
            sock_client.send(self.lenth_sending(cmd_command.encode(self.FORMAT)))
            sock_client.send(cmd_command.encode(self.FORMAT))
            print("Command sent.Waiting for returning output...")

            returned_lenth = int(sock_client.recv(self.BUFFER).decode(self.FORMAT))
            returned_output = sock_client.recv(returned_lenth).decode(self.FORMAT)
            os.system("cls")
            print("Server executed program and returned: \n" + returned_output)

            #if input("Execute more? (y/n): ") == 'y': self.cmd_input()
            self.cmd_input()
        except:
            print("Cant execute command")

    def get_file(self):
        pass

    def help_list(self):
        print('/return - returning to the main menu \n/disconnect - disconnecting from server and close program from any menu')
        os.system("pause")
        self.main_menu()

if __name__ == "__main__":
    print("Sender v2.2 (updated 01.05.2021)")
    client = Client_func(6067, 16, 'utf-8')
    client.main_menu(True)