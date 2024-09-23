from http.client import HTTPSConnection
from threading import Thread, Event
from time import time

class counter:
    def __init__(self) -> None:
        self.good, self.bad, self.error = 0, 0, 0
        self.created = 0

event = Event()
count = counter()
threads = 10
seconds = 10

headers = {'Content-Type': 'application/x-www-form-urlencoded'}
body = 'username=ndoshy'

def counter_function():
    while time() - start < seconds:
        print(f'\rgood = {count.good}; bad = {count.bad}; error = {count.bad}', end=' ')
    print(f'\rgood = {count.good}; bad = {count.bad}; error = {count.bad}, finished', end=' ')

def benchmark():
    cn = HTTPSConnection('httpbin.org', timeout=10)
    count.created += 1
    event.wait()
    while time() - start < seconds:
        try:
            cn.request('POST', '/post', body=body, headers=headers)
            response = cn.getresponse()
            if response.read().decode().__contains__('username'):
                count.good += 1
            else:
                count.bad += 1
        except:
            count.error += 1

for _ in range(threads):
    Thread(target=benchmark).start()

while count.created != threads:
    pass

start = time()
Thread(target=counter_function).start()
event.set()