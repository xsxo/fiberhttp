from http.client import HTTPConnection
from threading import Thread
from time import sleep, time

class counting:
    def __init__(self) -> None:
        self.ok = 0
        self.error = 0

counter = counting()
NUMBER = 1000000
THREADS = 100

def count():
    while counter.ok <= NUMBER:
        print(f'\rOK = {counter.ok}; ERR = {counter.error}', end=' ')
        sleep(0.1)
    print(f'\rOK = {counter.ok}; ERR = {counter.error}')
    print(f'http.client Sent {NUMBER} HTTP Requests in {str(time() - start).split('.')[0]} Second With {THREADS} Threads')

def test():
    CN_HTTPCLIENT : HTTPConnection = HTTPConnection('localhost', timeout=1)
    while counter.ok <= NUMBER:
        try:
            CN_HTTPCLIENT.request('GET', '/')
            RES = CN_HTTPCLIENT.getresponse()
            if RES.read().decode('utf-8').__contains__('random'):
                counter.ok += 1
            else:
                counter.error += 1
        except:
            counter.error += 1

Thread(target=count).start()

start = time()
for _ in range(THREADS):
    Thread(target=test).start()
