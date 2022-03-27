# @Author: Marcel Maluta
# @Date:   2022-03-11T18:59:58+01:00
# @Email:  marcelmaluta@gmail.com
# @Last modified by:   Marcel Maluta
# @Last modified time: 2022-03-12T13:33:58+01:00



import socket
from threading import Thread

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002

separator_token = "<SEP>"

client_sockets = set()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listenForClient(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            msg = msg.replace(separator_token, ": ")

        for client_socket in client_sockets:
            client_socket.send(msg.encode())

while True:
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    client_sockets.add(client_socket)

    t = Thread(target=listenForClient, args=(client_socket,))
    t.daemon = True
    t.start()
