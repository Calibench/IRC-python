import socket
import threading

HEADER = 64  # 64 bytes that is being sent from the client
FORMAT = 'utf-8'  # used to decode the bytes received from the client
DISCONNECT_MESSAGE = "!DISCONNECT"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # Gets the computer's IP
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    while True:
        try:
            msg = client.recv(2048).decode(FORMAT)
            if msg:
                print(msg)
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

try:
    while True:
        msg = input()
        if msg == DISCONNECT_MESSAGE:
            send(DISCONNECT_MESSAGE)
            break
        send(msg)
finally:
    client.close()
