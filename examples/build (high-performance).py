import fiberhttp

cn = fiberhttp.Client()
build = fiberhttp.Request('POST', 'httpbin.org', '/post', headers={}, data='number=10')

for _ in range(10):
    data = 'number=10'
    RES = cn.send(build)
    
    if RES.text().__contains__(data):
        print('OK')
    else:
        print('ERR0R')

cn.close()