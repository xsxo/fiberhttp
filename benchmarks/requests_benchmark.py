from requests import session
from threading import Thread, Event
from time import time

class counter:
    def __init__(self) -> None:
        self.good, self.bad, self.error = 0, 0, 0
        self.created = 0

cn = session()
event = Event()
count = counter()
threads = 10
seconds = 10

def counter_function():
    while time() - start < seconds:
        print(f'\rgood = {count.good}; bad = {count.bad}; error = {count.bad}', end=' ')
    print(f'\rgood = {count.good}; bad = {count.bad}; error = {count.bad}, finished', end=' ')

def benchmark():
    count.created += 1
    event.wait()
    while time() - start < seconds:
        try:
            response = cn.post('https://httpbin.org/post', data={'username':'ndoshy'}, timeout=10).text
            if response.__contains__('username'):
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