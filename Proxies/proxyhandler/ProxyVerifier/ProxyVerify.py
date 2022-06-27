from datetime import datetime
import asyncio

import aiohttp
from tqdm import tqdm

from .config import *


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
