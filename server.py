# @Author: Marcel Maluta
# @Date:   2022-03-11T18:59:58+01:00
# @Email:  marcelmaluta@gmail.com
# @Last modified by:   Marcel Maluta
# @Last modified time: 2022-05-26T11:18:55+02:00



import socket
from threading import Thread

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002

separator_token = "<SEP>"

client_sockets = set()
messages = ""

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def send_message(msg):
    for client_socket in client_sockets:
        client_socket.send(msg.encode())

def listenForClient(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
            globals()["messages"] += msg + "\n"
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
            print(f"[-] Client disconnected: {cs}")

        send_message(msg)

while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    client_sockets.add(client_socket)
    client_socket.send(messages.encode())

    t = Thread(target=listenForClient, args=(client_socket,))
    t.daemon = True
    t.start()
