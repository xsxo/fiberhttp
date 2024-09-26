from urllib.parse import urlencode, urlparse
from typing import Optional, Union

class request:
    def __init__(self, method: str = None, url: str = None, headers: dict = None, data: Optional[Union[str, dict]] = '', auth_proxy: str = ''):
        self.parse = None
        self.api: str = ''
        self.lower: list = []
        self.BytesHeaders: str = ''
        
        self.method = method
        self._url: str = url
        self.auth_proxy: str = auth_proxy
        self._headers = headers if headers is not None else {}
        self.data = data

        if self._url:
            self.url = self._url

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, value: str) -> None:
        self._url = value 
        self.parse = urlparse(self._url)
        self.api: str = (self.parse.path or '/') + ('?' + self.parse.query if self.parse.query else '')
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
        self.lower = [key.lower() for key in self._headers.keys()]

        if 'host' not in self.lower and self.parse:
            self._headers['Host'] = self.parse.hostname        
        
        if 'connection' not in self.lower:
            self._headers['Connection'] = 'Keep-Alive'
        if 'user-agent' not in self.lower:
            self._headers['User-Agent'] = 'Mozilla/5.0 Firefox/132.0'

        self._headers['Content-Length'] = str(len(self.data))

        for key, value in self.headers.items():
            self.BytesHeaders += f'{key}: {value}\r\n'

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: Optional[Union[str, dict]]) -> None:
        if isinstance(data, dict):
            self._data = urlencode(data)
        else:
            self._data = data

        self._set_default_headers()

    def __bytes__(self) -> bytes:
        return f'{self.method} {self.api} HTTP/1.1\r\n{self.auth_proxy}{self.BytesHeaders}\r\n{self.data}'.encode('utf-8')