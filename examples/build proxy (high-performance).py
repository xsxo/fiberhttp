import fiberhttp

cn = fiberhttp.client_proxy('http://Heisenberg:505152@20.111.54.16:8123', proxy_ssl=False)
build = fiberhttp.build_proxy('POST', 'httpbin.org', '/post', headers={}, data='number=10', proxy_auth=cn.proxy_auth)

for _ in range(10):
    data = 'number=' + str(_)
    RES = cn.post('https://httpbin.org/post', data=data)
    
    if RES.text().__contains__(data):
        print('OK')
    else:
        print('ERR0R')

cn.close()