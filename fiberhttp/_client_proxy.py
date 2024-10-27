from ._connections import new_connection_proxy, load_ssl
from ._responses import ExtractResponses
from ._build import Request
from ._exceptions import CreateClientEachThreadException, ProxyConnectionException, TimeoutReadingException
from typing import Optional, Union
from urllib.parse import urlparse, ParseResult
from time import time
from base64 import b64encode
from re import search

class Client_Proxy:
    def __init__(self, proxy:str, timeout:int=10) -> None:
        self.timeout: int = timeout
        self.running: bool = False
        self.connection = None
        self.host_connected : str = ''

        self.proxy : ParseResult = urlparse('http://' + proxy if '://' not in proxy else proxy)

        if self.proxy.username:
            self.proxy_auth = 'Proxy-Authorization: Basic ' + b64encode(f"{self.proxy.username}:{self.proxy.password}".encode()).decode() + '\r\n'  
        else:
            self.proxy_auth = ''
 
    def close(self) -> str:
        self.connection.close()
        return 'closed'

    def action(self, REQ:Request) -> str:
        try:
            self.running = True

            if not REQ.raw_request:
                REQ.load()
            self.connection.send(REQ.raw_request)

            response: bytes = b''
            start = time()

            while time() - start < self.timeout:
                recv = self.connection.recv(4096)
                response += recv

                if not recv:
                    break

                elif b'\r\n\r\n' in response:
                    headers, body = response.split(b'\r\n\r\n', 1)

                    content_length_match = search(rb'Content-Length: (\d+)', headers)
                    transfer_encoding_chunked = b'Transfer-Encoding: chunked' in headers

                    if content_length_match:
                        content_length = int(content_length_match.group(1))
                        if len(body) >= content_length:
                            break
                    elif transfer_encoding_chunked:
                        if b'0\r\n\r\n' in body:
                            break
            else:
                raise TimeoutReadingException()

            if b'Connection: close' in headers:
                self.host_connected = ''
                self.running = False

                try:
                    self.connection.close()
                except:
                    pass

                self.connection = None

            self.running = False
            return response
        except:
            self.host_connected = ''
            self.running = False

            try:
                self.connection.close()
            except:
                pass
            
            self.connection = None
            raise ProxyConnectionException()

    def delete(self, url:str, headers:dict={}):
        return self.get(url, headers, 'DELETE')
    
    def put(self, url:str, headers:dict={}, data: Optional[Union[str, dict]]='', json:dict=None):
        return self.post(url, headers, data, json, 'PUT')
    
    def patch(self, url:str, headers:dict={}, data: Optional[Union[str, dict]]='', json:dict=None):
        return self.post(url, headers, data, json, 'PATCH')

    def post(self, url:str, headers:dict={}, data: Optional[Union[str, dict]]='', json:dict=None, method:str='POST'):
        REQ = Request(method, url, headers, data, json)
        host: str = REQ.parse.hostname

        if not self.connection:
            self.connection = new_connection_proxy(self.proxy.hostname, int(self.proxy.port))
            self.connect(host, REQ.parse.port or (80 if REQ.parse.scheme == 'http' else 443))

        elif host != self.host_connected:
            self.connect(host, REQ.parse.port or (80 if REQ.parse.scheme == 'http' else 443))

        elif self.running:
            raise CreateClientEachThreadException()

        return ExtractResponses(self.action(REQ))

    def get(self, url:str, headers:dict={}, method:str='GET'):
        REQ = Request(method, url, headers)
        host: str = REQ.parse.hostname
        
        if not self.connection:
            self.connection = new_connection_proxy(self.proxy.hostname, int(self.proxy.port))
            self.connect(host, REQ.parse.port or (80 if REQ.parse.scheme == 'http' else 443))

        elif host != self.host_connected:
            self.connect(host, REQ.parse.port or (80 if REQ.parse.scheme == 'http' else 443))

        elif self.running:
            raise CreateClientEachThreadException()
        
        return ExtractResponses(self.action(REQ))

    def send(self, REQ:Request):
        host = REQ.parse.hostname

        if not self.connection:
            self.connection = new_connection_proxy(self.proxy.hostname, int(self.proxy.port))
            self.connect(host, REQ.parse.port or (80 if REQ.parse.scheme == 'http' else 443))

        elif host != self.host_connected:
            self.connect(host, REQ.parse.port or (80 if REQ.parse.scheme == 'http' else 443))

        elif self.running:
            raise CreateClientEachThreadException()

        return ExtractResponses(self.action(REQ))

    def connect(self, host:str, port:int = 0, ssl:bool = True):
        if port:
            port = port
        elif ssl:
            port = 443
        else:
            port = 80

        if not self.connection:
            self.connection = new_connection_proxy(self.proxy.hostname, int(self.proxy.port))

        self.host_connected = host
        
        REQ: str = 'CONNECT ' + host + ':' + str(port) + ' HTTP/1.1\r\n' + self.proxy_auth + 'Host: ' + host + ':' + str(port) + '\r\n\r\n'
        self.connection.send(REQ.encode('utf-8'))
        RES: str = self.connection.recv(4096)
        
        if port == 443:
            self.connection = load_ssl(self.connection)

        return ExtractResponses(RES)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()