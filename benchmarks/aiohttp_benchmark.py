from aiohttp import ClientSession, TCPConnector
from asyncio import sleep, gather, new_event_loop
from time import time

class counting:
    def __init__(self) -> None:
        self.ok = 0
        self.error = 0

counter = counting()
NUMBER = 1000000
THREADS = 100

async def count():
    while counter.ok <= NUMBER:
        print(f'\rOK = {counter.ok}; ERR = {counter.error}', end=' ')
        await sleep(0.1)
    print(f'\rOK = {counter.ok}; ERR = {counter.error}')
    print(f'aiohttp Sent {NUMBER} HTTP Requests in {int(time() - start)} Seconds With {THREADS} Threads')

async def test(AIOHTTP_CN):
    while counter.ok <= NUMBER:
        try:
            REQ = await AIOHTTP_CN.get('http://localhost/')
            RES = await REQ.text()
            if RES.__contains__('random'):
                counter.ok += 1
            else:
                counter.error += 1
        except:
            counter.error += 1

async def main():
    CONNECTOR = TCPConnector(ssl=False)
    AIOHTTP_CN = ClientSession(connector=CONNECTOR)

    tasks = []
    tasks.append(count())
    for _ in range(THREADS):
        tasks.append(test(AIOHTTP_CN))
    await gather(*tasks)

start = time()
loop = new_event_loop()
loop.run_until_complete(main())
loop.close()