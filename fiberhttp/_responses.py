from re import search
from json import loads
from typing import Union

class ExtractResponses:
    def __init__(self, response):
        self.response:str = response

    def __str__(self) -> str:
        reason = search(r'HTTP/1.1 (\d{3} .*)', self.response).group(1)
        return f"satus_code; reason: {reason}"
    
    def __repr__(self) -> str:
        return self.__str__() 

    def text(self):
        return str(self.response.split('\r\n\r\n', 1)[1])
    
    def status_code(self):
        return int(search(r'HTTP/1.1 (\d{3})', self.response).group(1))

    def json(self) -> dict:
        return loads(self.text())
    
    def headers(self) -> dict:
        for_return : dict = {}
        for_nothing : list = self.response.splitlines()[1:]

        for res in for_nothing:
            if not res.__contains__(': '):
                break
            for_split = res.split(': ')
            for_return[for_split[0]] = res.removeprefix(for_split[0] + ': ')

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
