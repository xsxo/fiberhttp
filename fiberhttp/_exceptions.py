class JsonDecodeException(Exception):
    def __str__(self):
        return 'Couldnt decode the text into json'

class TextDecodeException(Exception):
    def __str__(self):
        return 'Couldnt decode the bytes to text'

class HeadersReadingException(Exception):
    def __str__(self):
        return 'somthing worng when try read the response headers'

class TimeoutException(Exception):
    def __str__(self):
        return 'timeout'

class TimeoutReadingException(Exception):
    def __str__(self):
        return 'timeout when reading response'

class ConnectionErrorException(Exception):
    def __str__(self):
        return 'error when try create new connection'

class CreateClientEachThreadException(Exception):
    def __str__(self):
        return 'create a new client for each thread\nexample: https://github.com/xsxo/fiberhttp/blob/main/examples/mulit%20threads.py'
    
class MissingSchemaException(Exception):
    def __str__(self):
        return 'create a new client for each thread\nexample: https://github.com/xsxo/fiberhttp/blob/main/examples/mulit%20threads.py'

class InvalidScheme(Exception):
    def __str__(self):
        return "invalid URL scheme (http:// or https://)"
    

class ProxyConnectionException(Exception):
    def __str__(self):
        return "the proxy connection has been disconnected"
    
class ClientConnectionException(Exception):
    def __str__(self):
        return "the client connection has been disconnected"