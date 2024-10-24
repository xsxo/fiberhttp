from ._exceptions import TimeoutException, ConnectionErrorException
from typing import Union
from ssl import SSLSocket, SSLContext, PROTOCOL_TLS_CLIENT
from socket import socket, AF_INET, SOCK_STREAM
from certifi import where

def new_connection(host:str, port:int) -> Union[socket, SSLSocket]:
    try:
        connection = socket(AF_INET, SOCK_STREAM)
        connection.connect((host, port))

        if port == 443:
            context : SSLContext = SSLContext(PROTOCOL_TLS_CLIENT)
            context.load_verify_locations(where())
            connection = context.wrap_socket(connection, server_hostname=host)

    except TimeoutError:
        raise TimeoutException()

    except:
        ConnectionErrorException()
    
    return connection
    
def new_connection_proxy(host:str, port:int) -> socket:
    try:
        connection = socket(AF_INET, SOCK_STREAM)
        connection.connect((host, port))

    except TimeoutError:
        raise TimeoutException()
    
    except:
        ConnectionErrorException()   

    return connection
    
def load_ssl(connection:socket) -> SSLSocket:
    context = SSLContext()
    ssl_connection = context.wrap_socket(connection)
    context.load_verify_locations(where())
    return ssl_connection