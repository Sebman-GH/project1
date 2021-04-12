import socket

HEADER = 16
PORT = 6067
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main_menu(fst_start):
    if fst_start == True:
        
        SERVER = input("Input the server IP you would like to connect:")
        ADDR = (SERVER,PORT)
        print("Connecting...")
        try:
            client.connect(ADDR)
            print("Connected to the server.")
        except:
            print("Failed connect to the server!")
            main_menu(True)
    chs_temp = int(input("Choose the option: \n 1.Send the message \n 2.Send the file(unavaiable now) \n "))
    if chs_temp == 1: send_message()
    elif chs_temp == 2: send_file()
    else: 
        print("Wrong input!")
        main_menu(False)

def send_message(*msg):
    if msg == (): 
        msg = input("Enter what you would like to send:")
    if msg == "/return": main_menu(False)
    try:
        message = msg.encode(FORMAT)
        send_lenth = str(len(message)).encode(FORMAT)
        send_lenth += b' ' * (HEADER - len(send_lenth))
        client.send(send_lenth)
        client.send(message)
    except:
        print("Failed to send message")
        send_message()
    if msg != "/disconnect": 
            print("Message sent successfull")
            send_message()
    else: 
        quit()

def send_file():
    print("Not realised now")
    input()
    main_menu(False)
if __name__ == "__main__":
    print("Sender v1")
    main_menu(True)
    send_message("/disconnect")
socket.close