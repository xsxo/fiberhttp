from ._exceptions import JsonDecodeException, TextDecodeException
from re import search
from json import loads
from typing import Union

class ExtractResponses:
    def __init__(self, response):
        self.response:bytes = response

    def __str__(self) -> str:
        reason = search(rb'HTTP/1.1 (\d{3} .*)', self.response).group(1)
        return f"Reason: {reason.decode('utf-8')}"
    
    def __repr__(self) -> str:
        return self.__str__() 

    def content(self) -> bytes:
        return self.response.split(b'\r\n\r\n', 1)[1]

    def text(self) -> str:
        try:
            return self.response.split(b'\r\n\r\n', 1)[1].decode('utf-8')
        except:
            raise TextDecodeException()
    
    def status_code(self) -> int:
        return int(search(rb'HTTP/1.1 (\d{3})', self.response).group(1))

    def json(self) -> dict:
        try:
            return loads(self.text())
        except:
            raise JsonDecodeException()
    
    def headers(self) -> dict:
        for_return : dict = {}
        for_nothing : list = self.response.splitlines()[1:]

        for res in for_nothing:
            if not res.__contains__(b': '):
                break
            for_split = res.split(b': ')
            for_return[for_split[0].decode('utf-8')] = res.removeprefix(for_split[0] + b': ').decode('utf-8')

        return for_return

    
    def cookie(self) -> Union[dict, None]:
        components = [component.strip() for component in self.headers().get('Set-Cookie', '').split(';')]
        cookie_dict = {}
        
        for component in components:
            if '=' in component:
                key, value = component.split('=', 1)
                cookie_dict[key.strip()] = value.strip()
            else:
                key = component.strip()
                if key not in cookie_dict:
                    None

        return cookie_dict