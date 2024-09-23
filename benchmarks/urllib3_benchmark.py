from urllib3 import PoolManager, request
from threading import Thread
from time import sleep, time

class counting:
    def __init__(self) -> None:
        self.ok = 0
        self.error = 0

counter = counting()
CN_URLLIB3 : PoolManager = PoolManager()
NUMBER = 1000000
THREADS = 100

def count():
    while counter.ok <= NUMBER:
        print(f'\rOK = {counter.ok}; ERR = {counter.error}', end=' ')
        sleep(0.1)
    print(f'\rOK = {counter.ok}; ERR = {counter.error}')
    print(f'urllib3 Sent {NUMBER} HTTP Requests in {str(time() - start).split('.')[0]} Second With {THREADS} Threads')

def test():
    
    while counter.ok <= NUMBER:
        try:
            RES = CN_URLLIB3.request('GET', 'http://localhost')
            if RES.data.decode('utf-8').__contains__('random'):
                counter.ok += 1
            else:
                counter.error += 1
        except:
            counter.error += 1

Thread(target=count).start()

start = time()
for _ in range(THREADS):
    Thread(target=test).start()
