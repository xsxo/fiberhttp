from urllib.parse import urlencode
from typing import Optional, Union

def build(method:str, host:str, api:str, headers:dict={}, data:Optional[Union[str, dict]] = '') -> bytes:
    
    lower = [key.lower() for key in headers.keys()]
    if not headers or not lower.__contains__('host'):
        headers['Host'] = host
    if not headers or not lower.__contains__('connection'):
        headers['Connection'] = 'Keep-Alive'
    if not headers or not lower.__contains__('user-agent'):
        headers['User-Agent'] = 'Mozilla/5.0 Firefox/132.0'

    my_headers = ''
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

    lower = [key.lower() for key in headers.keys()]
    if not headers or not lower.__contains__('host'):
        headers['Host'] = host
    if not headers or not lower.__contains__('connection'):
        headers['Connection'] = 'Keep-Alive'
    if not headers or not lower.__contains__('user-agent'):
        headers['User-Agent'] = 'Mozilla/5.0 Firefox/132.0'

    my_headers = ''
    for key, value in headers.items():
        my_headers += key + ': ' + value + '\r\n'

    if data:
        if type(data) == dict:
            data : str = urlencode(data)

        if not headers or not lower.__contains__('content-length'):
            my_headers += 'Content-Length: ' + str(len(data)) + '\r\n'

    my_headers += '\r\n'
    
    return f'{method} {api} HTTP/1.1\r\n{my_headers}{proxy_auth}{data}'.encode('utf-8')
