import time
from datetime import datetime
import asyncio

import aiohttp
from tqdm import tqdm

# from .config import *

TEST_URL = 'http://127.0.0.1:8000/'
VERIFICATION_NUMBER = 5
TIMEOUT = 4
USER_AGENT = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}


class ProxyNotResponding(Exception):
    def __init__(self, proxy):
        super().__init__(f'{proxy} is not responding')


class ProxyVerifier:
    def __init__(self, proxies_to_check):
        self.proxies_to_check = proxies_to_check
        self._verified_proxies = []

    @staticmethod
    def to_proxy(socket):
        return f'http://{socket}'

    def run(self):
        asyncio.run(self.session_creator())
        return self

    async def session_creator(self):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as client:
            to_verify_proxies_generator = (self.check_proxy(client, socket) for socket in tqdm(self.proxies_to_check))
            await asyncio.gather(*to_verify_proxies_generator)

    async def check_proxy(self, client, socket):
        responses_speed = await self.make_request(client, url=TEST_URL, proxy=self.to_proxy(socket))

        verified_proxy = {
            "socket": socket,
            "success": 1 if responses_speed is not False else 0,
            "speed": round(responses_speed, 3)
        }
        self._verified_proxies.append(verified_proxy)

    @staticmethod
    async def make_request(client, *, proxy, url):
        timer_begin = datetime.now()
        try:
            await client.get(url, proxy=proxy, timeout=TIMEOUT)
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return False
        else:
            return (datetime.now() - timer_begin).total_seconds()

    def get_proxies(self):
        return self._verified_proxies


# asyncio.run same as loop.run_until_complete
if __name__ == '__main__':
    list = ["167.71.5.83:3128"]
    start = time.perf_counter()
    v = ProxyVerifier(list * 100)
    v.run()
    print(v.get_proxies())
    print(time.perf_counter() - start)
