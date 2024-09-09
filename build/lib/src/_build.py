from urllib.parse import urlencode
from typing import Optional, Union

def build(method:str, host:str, api:str, headers={}, data:Optional[Union[str, dict]] = '') -> bytes:
    if not headers:
        my_headers = 'Host: ' + host + '\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 Firefox/132.0\r\n'
    elif 'User-Agent' not in headers and 'user-agnet' not in headers:
        my_headers = 'Host: ' + host + '\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 Firefox/132.0\r\n'
    else:
        my_headers = 'Host: ' + host + '\r\nConnection: keep-alive\r\n'

        for key, value in headers.items():
            my_headers += key + ': ' + value + '\r\n'

    if data:
        if type(data) == dict:
            data : str = urlencode(data)

        if 'Content-Length' not in headers and 'content-length' not in headers:
            my_headers += 'Content-Length: ' + str(len(data)) + '\r\n'

    my_headers += '\r\n'
    
    return f'{method} {api} HTTP/1.1\r\n{my_headers}{data}'.encode('utf-8')

def build_proxy(method:str, host:str, api:str, headers={}, data:Optional[Union[str, dict]] = '', proxy_auth:str='') -> bytes:
    if not headers:
        my_headers = 'Host: ' + host + '\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 Firefox/132.0\r\n'
    elif 'User-Agent' not in headers and 'user-agnet' not in headers:
        my_headers = 'Host: ' + host + '\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 Firefox/132.0\r\n'
    else:
        my_headers = 'Host: ' + host + '\r\nConnection: keep-alive\r\n'

        for key, value in headers.items():
            my_headers += key + ': ' + value + '\r\n'

    if data:
        if type(data) == dict:
            data : str = urlencode(data)

        if 'Content-Length' not in headers and 'content-length' not in headers:
            my_headers += 'Content-Length: ' + str(len(data)) + '\r\n'

    my_headers += '\r\n'
    
    return f'{method} {api} HTTP/1.1\r\n{my_headers}{proxy_auth}{data}'.encode('utf-8')
