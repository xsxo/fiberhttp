import fiberhttp

cn = fiberhttp.Client_Proxy('http://Heisenberg:505152@20.111.54.16:8123', proxy_ssl=False)
build = fiberhttp.Request('POST', 'httpbin.org', '/post', headers={}, data='number=10')

for _ in range(10):
    data = 'number=' + str(_)
    RES = cn.post('https://httpbin.org/post', data=data)
    
    if RES.text().__contains__(data):
        print('OK')
    else:
        print('ERR0R')

cn.close()