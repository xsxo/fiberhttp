import fiberhttp

cn = fiberhttp.client()
build = fiberhttp.build('POST', 'httpbin.org', '/post', headers={}, data='number=10')

for _ in range(10):
    data = 'number=10'
    RES = cn.send('httpbin.org', build)
    
    if RES.text().__contains__(data):
        print('OK')
    else:
        print('ERR0R')

cn.close()