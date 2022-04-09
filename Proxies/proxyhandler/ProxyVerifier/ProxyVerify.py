import statistics
import timeit
from datetime import datetime
from threading import Thread

from tqdm import tqdm

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class Configuration:
    test_url = 'https://httpbin.org/ip'
    VERIFICATION_NUMBER = 5
    timeout = 1
    retries = Retry(total=3,
                    backoff_factor=0.1,
                    status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    to_repeat = 1
    sample_num = 3


class ProxyNotResponding(Exception):
    pass


# checked_at, success, latency, speed, etc.
class Verification:
    config = Configuration()
    successful_connection_counter = 0
    latency = 0
    speed = 0
    updated = datetime.now().time()

    def __init__(self, socket):
        self.socket = socket
        self.proxy = self.make_proxy()

    def make_proxy(self):
        proxy = {'http': f'http://{self.socket}'}
        proxy['https'] = proxy['http']
        return proxy

    def check(self):
        with requests.Session() as session:
            session.mount('http://', self.config.adapter)
            try:
                start_time = datetime.now()
                session.get(self.config.test_url, proxies=self.proxy, timeout=self.config.timeout)
                self.speed = int((datetime.now() - start_time).microseconds)
            except Exception as ex:
                raise ProxyNotResponding

    def evalproxy(self):
        samples = timeit.repeat(lambda: self.check(), number=self.config.to_repeat, repeat=self.config.sample_num)
        return (100.0 * statistics.mean(samples),
                100.0 * statistics.stdev(samples))

    def verify_proxy_connection(self):
        try:
            result = self.evalproxy()
        except ProxyNotResponding:
            print(f'{self.proxy["http"]} is not responding')
        else:
            self.latency = result[0]
            self.successful_connection_counter += 1
            print(
                f'{self.socket}  has a latency of {result[0]} ms (±{result[1]} ms) / '
                f'speed {self.speed} / connections{self.successful_connection_counter}')

    def return_proxies(self):  # make satisfiable return dict
        return {"socket": self.socket,
                "success": self.successful_connection_counter,
                "speed": self.speed,
                "latency": self.latency,
                "updated": self.updated}


def verify_proxies(proxies):
    verified_proxies = []
    threads = []
    for proxy in tqdm(proxies):
        verification_obj = Verification(proxy)
        verified_proxies.append(verification_obj)
        for _ in range(Verification.config.VERIFICATION_NUMBER):
            thread = Thread(target=verification_obj.verify_proxy_connection)
            thread.start()
            threads.append(thread)
    for x in threads:
        x.join()
    return [p.return_proxies() for p in verified_proxies]


# TODO  separate by functions, make tri block cleaner
# 134.119.206.110:1080
# {"IPAddress": "98.12.195.129", "Port": 443}
if __name__ == '__main__':
    list = ["134.119.206.110:1080"]
    start = datetime.now()

    verify_proxies(list * 20)

    print(datetime.now() - start)
# TODO CONCURRENT.FUTURES
