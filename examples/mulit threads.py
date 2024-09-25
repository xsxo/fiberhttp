import fiberhttp
import threading

# new client for each thread
def start_thread():
    cn = fiberhttp.client()
    data = 'number=' + str(_)
    RES = cn.post('https://httpbin.org/post', data=data)
    
    if RES.text().__contains__(data):
        print('OK')
    else:
        print('ERR0R')
    cn.close()

for _ in range(10):
    threading.Thread(target=start_thread).start()
