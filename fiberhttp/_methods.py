from ._client_file import client
from typing import Optional, Union

def get(url:str, headers:dict={}, method:str='GET'):
    with client(timeout=10) as cn:
        for_return = cn.get(url, headers, method)
        return for_return

def post(url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='POST'):
    with client(timeout=10) as cn:
        for_return = cn.post(url, headers, data, method)
        return for_return

def delete(url:str, headers:dict={}, method:str='DELETE'):
    with client(timeout=10) as cn:
        for_return = cn.get(url, headers, method)
        return for_return

def patch(url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='PATCH'):
    with client(timeout=10) as cn:
        for_return = cn.post(url, headers, data, method)
        return for_return

def put(url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='PUT'):
    with client(timeout=10) as cn:
        for_return = cn.post(url, headers, data, method)
        return for_return