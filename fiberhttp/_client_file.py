from ._connections import new_connection
from ._responses import ExtractResponses
from ._build import request
from typing import Optional, Union
from time import time
from re import search

class client:
    def __init__(self, timeout:int=10) -> None:
        self.time_out : int = timeout
        self.running : bool = False
        self.hosts : dict = {}

    def close_host(self, host) -> str:
        try:
            self.hosts[host].close()
            return f"'{host}' is closed"
        except:
            f"'{host}' not found"
    
    def close(self) -> str:
        for host in self.hosts.values():
            host.close()
        return 'closed'

    def action(self, REQ:request) -> str:
        self.running = True
        host = REQ.parse.hostname

        self.hosts[host].send(bytes(REQ))
        response : bytes = b''
        start = time()

        while time() - start < self.time_out:
            recv = self.hosts[host].recv(4096)
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
                    if b'\n\r\n0\r\n\r\n' in body:
                        break
        else:
            raise ValueError('timeout')

        self.running = False
        return response

    def delete(self, url:str, headers:dict={}):
        return self.get(url, headers, 'DELETE')
    
    def put(self, url:str, headers:dict={}, data=Optional[Union[str, dict]]):
        return self.post(url, headers, data, 'PUT')
    
    def patch(self, url:str, headers:dict={}, data=Optional[Union[str, dict]]):
        return self.post(url, headers, data, 'PATCH')

    def post(self, url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='POST'):
        REQ = request(method, url, headers, data)
        host : str = REQ.parse.hostname

        if self.running:
            assert  ValueError('create a new client for each thread\nexample: https://github.com/xsxo/fiberhttp/tree/main/benchmarks')

        elif host not in self.hosts:
            self.hosts[host] = new_connection(host, REQ.parse.port or (80 if REQ.parse.scheme == 'http' else 443))

        return ExtractResponses(self.action(REQ))

    def get(self, url:str, headers:dict={}, method:str='GET'):
        REQ = request(method, url, headers)
        host : str = REQ.parse.hostname

        if self.running:
            assert  ValueError('create a new client for each thread\nexample: https://github.com/xsxo/fiberhttp/tree/main/benchmarks')

        elif host not in self.hosts:
            self.hosts[host] = new_connection(host, REQ.parse.port or (80 if REQ.parse.scheme == 'http' else 443))        

        return ExtractResponses(self.action(REQ))
    
    def connect(self, host:str, port:int = 0, ssl:bool = True):
        if port:
            port = port
        elif ssl:
            port = 443
        else:
            port = 80

        if host not in self.hosts:
            self.hosts[host] = new_connection(host, port)

    def send(self, REQ:request):
        if self.running:
            assert  ValueError('create a new client for each thread\nexample: https://github.com/xsxo/fiberhttp/tree/main/benchmarks')
        elif REQ.parse.hostname not in self.hosts:
            self.hosts[REQ.parse.hostname] = new_connection(REQ.parse.hostname, REQ.parse.port or (80 if REQ.parse.scheme == 'http' else 443))

        return ExtractResponses(self.action(REQ))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()