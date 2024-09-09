from ._connections import new_connection
from ._responses import ExtractResponses
from ._build import build
from typing import Optional, Union
from urllib.parse import urlparse, ParseResult
from time import time

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

    def action(self, host:str, request:bytes) -> str:
        self.running = True
        start = time()
        self.hosts[host].sendall(request)
        body : str = ''

        while time() - start < self.time_out:
            try:
                response = self.hosts[host].recv(4096)
                body += response.decode('utf-8')
            except:
                if body and len(body.split('\r\n\r\n')) == 2:
                    break
        else:
            body = 'HTTP/1.1 408 TIMEOUT\r\nHOST: ' + host + '\r\n\r\nTIMEOUT' 

        self.running = False
        return body

    def delete(self, url:str, headers:dict={}):
        return self.get(url, headers, 'DELETE')
    
    def put(self, url:str, headers:dict={}, data=Optional[Union[str, dict]]):
        return self.post(url, headers, data, 'PUT')
    
    def patch(self, url:str, headers:dict={}, data=Optional[Union[str, dict]]):
        return self.post(url, headers, data, 'PATCH')

    def post(self, url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='POST'):
        parsed_url : ParseResult = urlparse(url)
        host : str = parsed_url.hostname

        if self.running:
            return 'create a new client for each thread\nexample: https://github.com/xsxo/fiberhttp/benchmarks'

        elif host not in self.hosts:
            self.hosts[host] = new_connection(host, parsed_url.port or (80 if parsed_url.scheme == 'http' else 443))

        return ExtractResponses(self.action(host, build(method, host, url.split(host)[1:][0] or '/', headers, data)))

    def get(self, url:str, headers:dict={}, method:str='GET'):
        parsed_url : ParseResult = urlparse(url)
        host : str = parsed_url.hostname

        if self.running:
            return 'create a new client for each thread\nexample: https://github.com/xsxo/fiberhttp/benchmarks'

        elif host not in self.hosts:
            self.hosts[host] = new_connection(host, parsed_url.port or (80 if parsed_url.scheme == 'http' else 443))        

        return ExtractResponses(self.action(host, build(method, host, url.split(host)[1:][0] or '/', headers, '')))
    
    def connect(self, host:str, ssl_verify:bool=True):
        if host not in self.hosts:
            self.hosts[host] = new_connection(host, (443 if ssl_verify else 80))

    def send(self, host:str, build:bytes, ssl_verify:bool=True):
        if self.running:
            return 'create a new client for each thread\nexample: https://github.com/xsxo/fiberhttp/benchmarks'
        elif host not in self.hosts:
            self.hosts[host] = new_connection(host, (443 if ssl_verify else 80))

        return ExtractResponses(self.action(host, build))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()