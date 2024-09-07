from ssl import create_default_context, SSLSocket
from socket import socket, AF_INET, SOCK_STREAM

def extract_port(url:str) -> int:
    if len(url.split(':')) == 3 or ':' in url and ':/' not in url:
        return url.split(':')[2]
    elif 'http://' in url:
        return 80
    
    return 443

def new_connection(host:str, port:int, time_out:int) -> socket | SSLSocket:
    connection = socket(AF_INET, SOCK_STREAM)
    connection.connect((host, port))

    if port == 80:
        connection.setblocking(False)
        connection.settimeout(time_out)
        return connection
    else:
        context = create_default_context()
        # context.load_verify_locations(where())
        ssl_connection = context.wrap_socket(connection, server_hostname=host)
        ssl_connection.setblocking(0)
        ssl_connection.settimeout(time_out)
        return ssl_connection

def new_raw_request(method, api, headers, data) -> str:
    return f"""{method} {api} HTTP/1.1\r
{headers}
\r
{data}
"""