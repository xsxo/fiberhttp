from ._connections import new_connection_proxy, load_ssl
from ._responses import ExtractResponses
from ._build import build_proxy
from typing import Optional, Union
from urllib.parse import urlparse, ParseResult
from time import time
from base64 import b64encode
from re import search

class client_proxy:
    def __init__(self, proxy:str, proxy_ssl:Union[bool, int]=0, timeout:int=10) -> None:
        self.time_out : int = timeout
        self.running : bool = False
        self.host_connected : str = ''
        proxy : ParseResult = urlparse(proxy)

        if proxy_ssl == 0:
            proxy_ssl =  (False if proxy.scheme == 'http' else True)

        if proxy_ssl:
            self.proxy_port = 443
        else:
            self.proxy_port = 80

        self.connection = new_connection_proxy(proxy.hostname or proxy.hostname, int(proxy.port))
        if proxy.username:
            self.proxy_auth = 'Proxy-Authorization: Basic ' + b64encode(f"{proxy.username}:{proxy.password}".encode()).decode() + '\r\n'  
        else:
            self.proxy_auth = ''
 
    def close(self) -> str:
        self.connection.close()
        return 'closed'

    def action(self, request:bytes) -> str:
        self.running = True
        self.connection.send(request)
        response : bytes = b''
        start = time()

        while time() - start < self.time_out:
            data = self.connection.recv(4096)
            body += data

            if not data:
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
            raise ValueError('timeout')

        self.running = False
        return response.decode('utf-8')

    def delete(self, url:str, headers:dict={}):
        return self.get(url, headers, 'DELETE')
    
    def put(self, url:str, headers:dict={}, data=Optional[Union[str, dict]]):
        return self.post(url, headers, data, 'PUT')
    
    def patch(self, url:str, headers:dict={}, data=Optional[Union[str, dict]]):
        return self.post(url, headers, data, 'PATCH')

    def post(self, url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='POST'):
        parsed_url : ParseResult = urlparse(url)
        host : str = parsed_url.hostname

        if host != self.host_connected:
            self.connect(host)

        if self.running:
            assert  ValueError('create a new client for each thread\nexample: https://github.com/xsxo/fiberhttp/tree/main/benchmarks')

        return ExtractResponses(self.action(build_proxy(method, host, parsed_url.path or '/' + url.split(host)[1].split(':')[0], headers, data, self.proxy_auth)))

    def get(self, url:str, headers:dict={}, method:str='GET'):
        parsed_url : ParseResult = urlparse(url)
        host : str = parsed_url.hostname

        if host != self.host_connected:
            self.connect(host)

        if self.running:
            assert  ValueError('create a new client for each thread\nexample: https://github.com/xsxo/fiberhttp/tree/main/benchmarks')
        
        return ExtractResponses(self.action(build_proxy(method, host, parsed_url.path or '/' + url.split(host)[1].split(':')[0], headers, '', self.proxy_auth)))
    
    def connect(self, host:str):
        self.host_connected = host
        REQ : str = 'CONNECT ' + host + ':' + str(self.proxy_port) + ' HTTP/1.1\r\nHost: ' + host + ':' + str(self.proxy_port) + '\r\n' + self.proxy_auth + '\r\n'
        self.connection.send(REQ.encode('utf-8'))
        RES : str = self.connection.recv(4096).decode('utf-8')
        
        if self.proxy_port == 443:
            self.connection = load_ssl(self.connection, host)
        # else:
            # self.connection.setblocking(0)

        return ExtractResponses(RES)

    def send(self, host:str, build:bytes):
        if self.running:
            return 'create a new client for each thread\nexample: https://github.com/xsxo/fiberhttp/tree/main/benchmarks'
        elif host != self.host_connected:
            self.connect(host)

        return ExtractResponses(self.action(host, build))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()