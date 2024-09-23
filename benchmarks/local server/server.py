import socket
from random import randint
from threading import Thread

HOST = 'localhost'
PORT = 80

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()
print(f"Server listening on https://{HOST}:{PORT}")

def recv_send(ssl_socket):
    while True:
        try:
            ssl_socket.recv(1024)
            data = f"random={str(randint(1, 100000000000))}"
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: text/html\r\n"
            response += f"Content-Length: {len(data)}\r\n"
            response += "\r\n"
            response += data

            ssl_socket.send(response.encode('utf-8'))
        except:
            break

while True:
    client_socket, client_address = server_socket.accept()
    Thread(target=recv_send, args=(client_socket,)).start()