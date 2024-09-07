from re import search
from json import loads

class ExtractResponses:
    def __init__(self, response):
        self.response:str = response

    def __str__(self) -> str:
        return f"status_code: {search(r'HTTP/1.1 (\d{3} .*)', self.response).group(1)}"

    def status_code(self):
        self.__str__()

    def json(self) -> dict:
        return loads(self.body())

    def text(self) -> str:
        return self.body()

    def body(self) -> str:
        return str(self.response.split('\r\n\r\n')[1])
    
    def headers(self) -> dict:
        for_return : dict = {}
        for_nothing : list = self.response.splitlines()[1:]

        for res in for_nothing:
            if not res.__contains__(': '):
                break
            for_split = res.split(': ')
            for_return[for_split[0]] = res.removeprefix(for_split[0] + ': ')

        return for_return