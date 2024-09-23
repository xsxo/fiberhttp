from typing import Union
from ssl import create_default_context, SSLSocket, SSLContext
from socket import socket, AF_INET, SOCK_STREAM
from certifi import where

def new_connection(host:str, port:int) -> Union[socket, SSLSocket]:
    connection = socket(AF_INET, SOCK_STREAM)
    connection.connect((host, port))

    if port != 443:
        connection.setblocking(0)
        return connection
    else:
        context : SSLContext = create_default_context()
        context.load_verify_locations(where())
        ssl_connection = context.wrap_socket(connection, server_hostname=host)
        ssl_connection.setblocking(0)

        return ssl_connection
    
def new_connection_proxy(host:str, port:int) -> socket:
    connection = socket(AF_INET, SOCK_STREAM)
    connection.connect((host, port))

    return connection
    
def load_ssl(connection:socket, host) -> SSLSocket:
    context = create_default_context()
    ssl_connection = context.wrap_socket(connection, server_hostname=host)
    ssl_connection.setblocking(0)
    
    return ssl_connection