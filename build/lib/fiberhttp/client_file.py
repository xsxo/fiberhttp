from .other_functions import new_connection, extract_port, new_raw_request
from .responses import ExtractResponses
from typing import Optional, Union
from urllib.parse import urlencode, urlparse

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

    def action(self, request:str, host:str) -> str:
        self.running = True
        self.hosts[host].sendall(request.encode('utf-8'))
        body : str = ''
        loop : bool = False

        while True:
            try:
                response = self.hosts[host].recv(4096)
                body += response.decode('utf-8')
                loop = True
            except:
                if loop:
                    break
        
        self.running = False
        return body

    def delete(self, url:str, headers:dict={}):
        return self.get(url, headers, 'DELETE')
    
    def put(self, url:str, headers:dict={}, data=Optional[Union[str, dict]]):
        return self.post(url, headers, data, 'PUT')
    
    def patch(self, url:str, headers:dict={}, data=Optional[Union[str, dict]]):
        return self.post(url, headers, data, 'PATCH')

    def post(self, url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='POST'):
        host : str = urlparse(url).hostname

        if type(data) == dict:
            data = urlencode(data)
        else:
            data = data

        if host not in self.hosts:
            self.hosts[host] = new_connection(host, extract_port(url), time_out=self.time_out)

        my_headers = f'Host: {host}\r\nConnection: keep-alive\r\n'
        if 'user-agent' not in headers and 'User-Agent' not in headers:
            my_headers += 'User-Agent: Mozilla/5.0 Firefox/132.0\r\n'

        for key, value in headers.items():
            my_headers += key + ': ' + value + '\r\n'
        my_headers += 'Content-Length: ' + str(len(data)) + '\r'

        if self.running:
            return 'this client under used, create new client in same host'

        return ExtractResponses(self.action(new_raw_request(method, url.split(host)[1:][0] or '/', my_headers, data), host))

    def get(self, url:str, headers:dict={}, method:str='GET'):
        host : str = urlparse(url).hostname

        if host not in self.hosts:
            self.hosts[host] = new_connection(host, extract_port(url), time_out=self.time_out)

        my_headers = f'Host: {host}\r\nConnection: keep-alive\r\n'
        if 'user-agent' not in headers and 'User-Agent' not in headers:
            my_headers += 'User-Agent: Mozilla/5.0 Firefox/132.0\r\n'
        
        for key, value in headers.items():
            my_headers += key + ': ' + value + '\r\n'

        if self.running:
            return 'this client under used, create new client in same host'
        
        return ExtractResponses(self.action(new_raw_request(method, url.split(host)[1:][0] or '/', my_headers, ''), host))
