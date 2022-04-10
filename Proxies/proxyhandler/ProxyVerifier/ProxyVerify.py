import time
from datetime import datetime
from threading import Thread

from tqdm import tqdm

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class Configuration:
    test_url = 'http://127.0.0.1:8000/'
    VERIFICATION_NUMBER = 5
    timeout = 1.6
    user_agent = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}


class ProxyNotResponding(Exception):
    pass


class Verification:
    config = Configuration()
    successful_connection_counter = 0
    speed = 0

    def __init__(self, socket):
        self.socket = socket
        self.proxy = self.make_proxy()

    def make_proxy(self):
        proxy = {'http': f'http://{self.socket}'}
        proxy['https'] = proxy['http']
        return proxy

    def verify_proxy_connection(self):
        try:
            self.check()
        except ProxyNotResponding:
            print(f'{self.proxy["http"]} is not responding')
        else:
            self.successful_connection_counter += 1
            print(f'{self.socket} has speed {self.speed} / connections{self.successful_connection_counter}')

    # TODO custom speed check
    def check(self):
        with requests.Session() as session:
            start_time = time.perf_counter()
            try:
                session.get(self.config.test_url, proxies=self.proxy, timeout=self.config.timeout,
                            headers=self.config.user_agent)
            except Exception as ex:
                print(ex)
                raise ProxyNotResponding
            else:
                self.speed = round(float((time.perf_counter() - start_time)), 3)

    def return_proxies(self):  # make satisfiable return dict
        return {"socket": self.socket,
                "success": self.successful_connection_counter,
                "speed": self.speed}


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


if __name__ == '__main__':
    list = ["182.160.121.99:10800"]
    start = time.perf_counter()
    print(verify_proxies(list))
    print(time.perf_counter() - start)
