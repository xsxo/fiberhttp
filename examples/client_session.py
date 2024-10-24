import fiberhttp

cn = fiberhttp.Client()

for _ in range(10):
    data = 'number=' + str(_)
    RES = cn.post('https://httpbin.org/post', data=data)
    
    if RES.text().__contains__(data):
        print('OK')
    else:
        print('ERR0R')

cn.close()