from ._client_file import Client
from typing import Optional, Union

def get(url:str, headers:dict={}):
    with Client(timeout=10) as cn:
        for_return = cn.get(url, headers, 'GET')
        return for_return

def post(url:str, headers:dict={}, data: Optional[Union[str, dict]]='', json:dict=None):
    with Client(timeout=10) as cn:
        for_return = cn.post(url, headers, data, json, 'POST')
        return for_return

def delete(url:str, headers:dict={}):
    with Client(timeout=10) as cn:
        for_return = cn.get(url, headers, 'DELETE')
        return for_return

def patch(url:str, headers:dict={}, data: Optional[Union[str, dict]]='', json:dict=None):
    with Client(timeout=10) as cn:
        for_return = cn.post(url, headers, data, json, 'PATCH')
        return for_return

def put(url:str, headers:dict={}, data: Optional[Union[str, dict]]='', json:dict=None):
    with Client(timeout=10) as cn:
        for_return = cn.post(url, headers, data, json, 'PUT')
        return for_return