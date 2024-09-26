import fiberhttp

cn = fiberhttp.client()

# not required but preferred for high performance
cn.connect('httpbin.org')

# preparing the request before send it
req = fiberhttp.request()
req.method = 'POST'
req.url = 'https://httpbin.org/post'
req.headers = {'Accept-Language': 'en-US,en;q=0.5'}
req.data = 'number=10'

for _ in range(10):
    RES = cn.send(req)
    if RES.text().__contains__('number=10'):
        print('OK')
    else:
        print('ERR0R')

cn.close()