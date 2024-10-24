import fiberhttp

cn = fiberhttp.Client_Proxy('http://20.111.54.16:8123', proxy_ssl=False)

for _ in range(10):
    data = 'number=' + str(_)
    RES = cn.post('http://httpbin.org/post', data=data)
    
    if RES.text().__contains__(data):
        print('OK')
    else:
        print('ERR0R')

cn.close()