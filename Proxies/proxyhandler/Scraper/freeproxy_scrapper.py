import re
import datetime

import lxml.html
import requests
from requests.exceptions import Timeout

from .AbstractProxyAdapter import ProxyInterfaceAdapter


class FreeProxyScrapper(ProxyInterfaceAdapter):
    URL = 'https://free-proxy-list.net/'

    def scrap(self):
        html = self.request()
        if html:
            doc = lxml.html.fromstring(html.content)
            proxies_table = doc.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr')
            self.make_proxies(proxies_table)
        return self._proxies

    def request(self):
        try:
            return requests.get(self.URL, timeout=self._TIMEOUT)
        except (requests.exceptions.ConnectionError, Timeout):
            return None

    @staticmethod
    def grouped(iterable, n):
        "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
        return zip(*[iter(iterable)] * n)

    def get_proper_date_format(self, data):
        passed_time = re.compile("\w.+(?= ago)").search(data).group().split()
        created_at = datetime.datetime.now()
        for time, unit in self.grouped(passed_time, 2):
            if 'hour' in unit:
                created_at = created_at - datetime.timedelta(hours=int(time))
            if 'min' in unit:
                created_at = created_at - datetime.timedelta(minutes=int(time))
            if 'sec' in unit:
                created_at = created_at - datetime.timedelta(seconds=int(time))
        return f'{created_at.year}-{created_at.month}-{created_at.day} {created_at.hour}:{created_at.minute}:{created_at.second}.{round(created_at.microsecond, 2)}'

    def make_proxies(self, raw_proxies):
        for proxy in raw_proxies:
            proxy = proxy.getchildren()
            protocol = 'http' if proxy[6].text == 'no' else 'https'
            created_at = self.get_proper_date_format(proxy[7].text)
            self._proxies.append(
                {"socket": f"{proxy[0].text}:{proxy[1].text}", "country": proxy[2].text,
                 "anonymity": proxy[4].text, "createdAt": created_at, "protocol": protocol, "scraper_name": type(self).__name__})
