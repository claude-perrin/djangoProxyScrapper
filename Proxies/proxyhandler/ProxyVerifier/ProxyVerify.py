import time
from datetime import datetime
import asyncio
from statistics import mean

import aiofiles
import aiohttp
from lxml.html import fromstring
from tqdm import tqdm

# from config import *

TEST_URL = 'http://127.0.0.1:8000/'
VERIFICATION_NUMBER = 5
TIMEOUT = 4
USER_AGENT = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}


class ProxyNotResponding(Exception):
    def __init__(self, proxy):
        super().__init__(f'{proxy} is not responding')


# timeit decorator async
def timeit(func):
    async def process(func, *args, **params):
        try:
            await func(*args, **params)
        except Exception as exc:
            raise RuntimeError

    async def helper(*args, **params):
        start = datetime.now()
        try:
            await process(func, *args, **params)
        except RuntimeError as exc:
            return 0
        return (datetime.now() - start).total_seconds()

    return helper


class ProxyVerifier:
    _verified_proxies = []

    def __init__(self, sockets):
        self.sockets = sockets

    @staticmethod
    def to_proxy(socket):
        return f'http://{socket}'

    def run(self):
        asyncio.run(self.session_creator())
        return self

    async def session_creator(self):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as client:
            await asyncio.gather(
                *[self.check_proxy(client, socket) for socket in tqdm(self.sockets)])

    async def check_proxy(self, client, socket):
        responses_speed = await asyncio.gather(
            *[self.make_request(client, url=TEST_URL, proxy=self.to_proxy(socket)) for _ in range(VERIFICATION_NUMBER)])
        print(responses_speed)

        verified_proxy = {
            "socket": socket,
            "success": len({successful_connect for successful_connect in responses_speed if successful_connect != 0}),
            "speed": round(mean(responses_speed), 3)
        }
        self._verified_proxies.append(verified_proxy)

    @timeit
    async def make_request(self, client, *, proxy, url, method="GET", **kwargs):
        try:
            async with client.request(method, url, proxy=proxy, **kwargs) as response:
                return response
        except Exception as exc:
            raise ProxyNotResponding(proxy)

    def get_proxies(self):
        return self._verified_proxies


# 17.185218759 s   -    synch way 100
# asyncio.run same as loop.run_until_complete
# TODO successful_connection counter
if __name__ == '__main__':
    # print(TEST_URL)
    list = ["172.67.181.8:80"]
    start = time.perf_counter()
    # loop.run_until_complete(v.verify_proxy_connection())
    # print(verify_proxies(list * 1000))
    v = ProxyVerifier(list * 100)
    v.run()
    print(v.get_proxies())
    print(time.perf_counter() - start)
