from typing import Union
from ssl import SSLSocket, SSLContext, CERT_NONE, PROTOCOL_TLS_CLIENT
from socket import socket, AF_INET, SOCK_STREAM
from certifi import where

def new_connection(host:str, port:int) -> Union[socket, SSLSocket]:
    connection = socket(AF_INET, SOCK_STREAM)
    connection.connect((host, port))

    # if port != 443:
    #     connection.setblocking(0)
    #     return connection
    if port == 443:
        context : SSLContext = SSLContext(PROTOCOL_TLS_CLIENT)
        # context.check_hostname = False
        # context.verify_mode = CERT_NONE
        context.load_verify_locations(where())
        ssl_connection = context.wrap_socket(connection, server_hostname=host)
        # ssl_connection.setblocking(0)

        return ssl_connection
    else:
        return connection
    
def new_connection_proxy(host:str, port:int) -> socket:
    connection = socket(AF_INET, SOCK_STREAM)
    connection.connect((host, port))

    return connection
    
def load_ssl(connection:socket, host) -> SSLSocket:
    context = SSLContext(PROTOCOL_TLS_CLIENT)
    # context.check_hostname = False
    # context.verify_mode = CERT_NONE
    ssl_connection = context.wrap_socket(connection, server_hostname=host)

    # ssl_connection.setblocking(0)
    
    return ssl_connection