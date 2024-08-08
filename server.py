import socket
import threading
import time

HEADER = 64  # 64 bytes that is being sent from the client
FORMAT = 'utf-8'  # used to decode the bytes received from the client
DISCONNECT_MESSAGE = "!DISCONNECT"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # Gets the computer's IP
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []

# Broadcast message to all connected clients
def broadcast(message, _conn):
    for client in clients:
        if client != _conn:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

# Handles the individual clients connected
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    clients.append(conn)

    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                if msg == DISCONNECT_MESSAGE:
                    connected = False

                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                formatted_msg = f"[{current_time}] {addr}: {msg}"
                print(formatted_msg)
                broadcast(formatted_msg.encode(FORMAT), conn)
        except:
            connected = False

    conn.close()
    clients.remove(conn)
    print(f"[DISCONNECTED] {addr} disconnected.")

# Starts the server
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\n[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] Server is starting...")
start()
