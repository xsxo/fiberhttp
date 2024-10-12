from fiberhttp import client, request
from threading import Thread
from time import sleep, time

class counting:
    def __init__(self) -> None:
        self.ok = 0
        self.error = 0

counter = counting()
BUILD = request('GET', 'http://localhost/')
NUMBER = 1000000
THREADS = 100

def count():
    while counter.ok <= NUMBER:
        print(f'\rOK = {counter.ok}; ERR = {counter.error}', end=' ')
        sleep(0.1)
    print(f'\rOK = {counter.ok}; ERR = {counter.error}')
    print(f'FiberHTTP Sent {NUMBER} HTTP Requests in {str(time() - start).split('.')[0]} Second With {THREADS} Threads')

def test():
    CN_FIBERHTTP : client = client(timeout=0.4)
    while counter.ok <= NUMBER:
        try:
            if CN_FIBERHTTP.send(BUILD).text().__contains__('random'):
                counter.ok += 1
            else:
                counter.error += 1
        except:
            counter.error += 1

Thread(target=count).start()

start = time()
for _ in range(THREADS):
    Thread(target=test).start()
