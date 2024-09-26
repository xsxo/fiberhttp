from ._client_file import client
from ._client_proxy import client_proxy
from ._methods import get, post, put, delete, patch
from ._build import request

__all__ = ['client', 'client_proxy', 'request', 'get', 'post', 'put', 'delete', 'patch']