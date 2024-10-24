from ._exceptions import InvalidScheme
from urllib.parse import urlencode, urlparse
from typing import Optional, Union
from json import dumps

class Request:
    def __init__(self, method: str = None, url: str = None, headers: dict = {}, data: Optional[Union[str, dict]] = '', json: dict = None, auth_proxy: str = ''):
        self.parse = None
        self.api: str = ''
        self.BytesHeaders: str = ''
        self.setJson: bool = False
        
        self.method = method
        self._url: str = url
        self.auth_proxy: str = auth_proxy
        # self._headers = headers if headers is not None else {}
        self._headers = headers
        self._json = json
        self._data = data

        if self._url:
            self.url = self._url

        if self._headers:
            self.headers = headers

        if self._data:
            self.data = data

        if self._json:
            self.json = json

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, value: str) -> None:
        self._url = value 
        self.parse = urlparse(self._url)

        if self._url and not self.parse.scheme:
            raise InvalidScheme()

        self.api = (self.parse.path or '/') + ('?' + self.parse.query if self.parse.query else '')
        self._set_default_headers()

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value: dict) -> None:
        self._headers = value
        self._set_default_headers()

    def _set_default_headers(self) -> None:
        self.BytesHeaders = ''
        lower = [key.lower() for key in self._headers.keys()]

        if 'host' not in lower and self.parse:      
            self.BytesHeaders += f'Host: {self.parse.hostname}\r\n'

        if 'connection' not in lower:
            self.BytesHeaders += 'Connection: Keep-Alive\r\n'

        if 'user-agent' not in lower:
            self.BytesHeaders += 'User-Agent: Mozilla/5.0 Firefox/132.0\r\n'

        if self.setJson and 'content-type' not in lower:
            self.BytesHeaders += 'Content-Type: application/json\r\n'

        if 'content-length' not in lower:
            self.BytesHeaders += f'Content-Length: {str(len(self.data))}\r\n'

        for key, value in self.headers.items():
            self.BytesHeaders += f'{key}: {value}\r\n'

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: Optional[Union[str, dict]]) -> None:
        if isinstance(data, dict):
            self.setJson = False
            self._data = urlencode(data)
        else:
            self._data = data

        self._set_default_headers()
        
    @property
    def json(self):
        return self._json
    
    @json.setter
    def json(self, json: dict) -> None:
        self.setJson = True
        self.data = dumps(json)

    def __bytes__(self) -> bytes:
        return f'{self.method} {self.api} HTTP/1.1\r\n{self.auth_proxy}{self.BytesHeaders}\r\n{self.data}'.encode('utf-8')
    
