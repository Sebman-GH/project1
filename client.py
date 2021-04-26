import socket
import os
from time import sleep

HEADER = 16
PORT = 6067
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main_menu(*fst_start):
    try:
        if fst_start[0] == True:
            SERVER = '192.168.56.1'
            #SERVER = input("Input the server IP you would like to connect:")
            ADDR = (SERVER,PORT)
            print("Connecting...")
            try:
                client.connect(ADDR)
                print("Connected to the server.")
                sleep(0.5)
            except:
                print("Failed connect to the server!")
                sleep(1)
                main_menu(True)
    except IndexError:
        pass
    chs_temp = input("Choose the option: \n 1.Send the message \n 2.Send the file \n 3.All commands in the program (/help) \n")
    if chs_temp == "/disconnect": send_message("/disconnect")
    elif chs_temp == '1': send_message()
    elif chs_temp == '2': send_file()
    elif chs_temp == '3': help_list()
    else: 
        print("Wrong input!")
        main_menu()

def send_message(*msg):
    while True:
        if msg == (): msg = input("Enter what you would like to send:")
        if msg == "/return": main_menu()
        if type(msg) == tuple: msg = msg[0]
        try:
            client.send(b"1")
            message = msg.encode(FORMAT)
            client.send(lenth_sending(message))
            client.send(message)
            print("Message sent successfull")
        except: 
            print("Failed to send message")
            main_menu(True)
        if msg == "/disconnect": 
            quit()
        msg = ()

def send_file():
    os.system("dir")
    filename = input("Enter file name what you would like to send(in same directory): ")
    if filename == "/disconnect": send_message("/disconnect")
    if filename == "/return": main_menu()
    try:
        with open(filename,'rb') as file:
            data = file.read()
            filename = filename.encode(FORMAT)
            client.send(b"2")
            client.send(lenth_sending(filename))
            client.send(filename)
            client.send(lenth_sending(data))
            client.sendall(data)
            if input("Open file after sending? (y/n)\n") == 'y': client.send(b'y')
            else: client.send(b'n')
            print("File sent")
            file.close()
    except:
        print("Failed to send file.")
    main_menu()

def lenth_sending(string):
        string_lenth = str(len(string)).encode(FORMAT)
        string_lenth += b' ' * (HEADER - len(string_lenth))
        return string_lenth

def cmd_input():
    pass

def help_list():
    print('/return - returning to the main menu \n/disconnect - disconnecting from server and close program from any menu')
    os.system("pause")
    main_menu()

print("Sender v2 (updated 04.26.2021)")
main_menu(True)