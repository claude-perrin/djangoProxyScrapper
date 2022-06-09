"""
Statistic:
	1) procent of working proxies, e.g. from 300 scraped sockets only 20 are working
		division on http and https
	2) average speed
	3) optional: the fastest situation, e.g. UK, ROM, FR
	4) the best proxy list provider, name of website, e.g. free-proxy-list

"""
# TODO do something else during verification
# TODO normal statistic
# TODO put on the server
# TODO prometheus

import time
from datetime import datetime
import asyncio

import aiohttp
from tqdm import tqdm

TEST_URL = 'http://127.0.0.1:8000/'
VERIFICATION_NUMBER = 5
TIMEOUT = 4
USER_AGENT = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}


class ProxyVerifier:
    ProxyNotResponding = (asyncio.TimeoutError, aiohttp.ClientError)

    def __init__(self, proxies_to_check):
        self.proxies_to_check = proxies_to_check
        self._verified_proxies = []

    @staticmethod
    def to_proxy(socket):
        return f'http://{socket}'

    def run(self):
        asyncio.run(self.start_verification())
        return self

    async def start_verification(self):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as client:
            to_verify_proxies_generator = (self.check_proxy(client, socket) for socket in tqdm(self.proxies_to_check))
            await asyncio.gather(*to_verify_proxies_generator)

    async def check_proxy(self, client, socket):
        response_speed_tracker_start = datetime.now()

        response = await self.make_request(client, url=TEST_URL, proxy=self.to_proxy(socket))

        response_speed = (datetime.now() - response_speed_tracker_start).total_seconds()

        verified_proxy = {
            "socket": socket,
            "success": 1 if response else 0,
            "speed": round(response_speed, 3) if response else 0,
        }
        self._verified_proxies.append(verified_proxy)

    async def make_request(self, client, *, proxy, url):
        try:
            return await client.get(url, proxy=proxy, timeout=TIMEOUT)
        except self.ProxyNotResponding:
            return False

    @property
    def failed_proxies(self):
        return {i for i in self.verified_proxies if i['success'] == 0}

    @property
    def succeeded_proxies(self):
        return {i for i in self.verified_proxies if i['success'] > 0}

    @property
    def verified_proxies(self):
        return self._verified_proxies


# asyncio.run same as loop.run_until_complete
if __name__ == '__main__':
    list = ["167.71.5.83:3128"]
    start = time.perf_counter()
    v = ProxyVerifier(list * 10)
    v.run()
    print(v.succeeded_proxies)
    print(time.perf_counter() - start)
