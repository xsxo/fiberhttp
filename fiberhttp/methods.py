from .client_file import client
from typing import Optional, Union

def get(url:str, headers:dict={}, method:str='GET'):
    cn = client(timeout=10)
    for_return = cn.get(url, headers, method)
    cn.close()
    return for_return

def post(url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='POST'):
    cn = client(timeout=10)
    for_return = cn.post(url, headers, data, method)
    cn.close()
    return for_return

def delete(url:str, headers:dict={}, method:str='DELETE'):
    cn = client(timeout=10)
    for_return = cn.get(url, headers, method)
    cn.close()
    return for_return

def patch(url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='PATCH'):
    cn = client(timeout=10)
    for_return = cn.post(url, headers, data, method)
    cn.close()
    return for_return

def put(url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='PUT'):
    cn = client(timeout=10)
    for_return = cn.post(url, headers, data, method)
    cn.close()
    return for_return