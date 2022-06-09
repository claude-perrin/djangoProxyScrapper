import requests

from .AbstractProxyAdapter import ProxyInterfaceAdapter
import re


class GeonodeProxyScrapper(ProxyInterfaceAdapter):
    URL = 'https://proxylist.geonode.com/api/proxy-list?limit=200&page=1&sort_by=lastChecked&sort_type=desc'

    def scrap(self):
        response = self.request()
        proxies = response.json()
        self.make_proxies(proxies)
        return self._proxies

    def request(self):
        try:
            return requests.get(self.URL)
        except requests.exceptions.ConnectionError:
            return None

    def get_proper_date_format(self, data):
        print(data)
        date = re.compile(r".+?(?=T)+").search(data).group()
        time = re.compile(r"[^T]+?(?=Z)").search(data).group()
        return date + ' ' + time

    # 2022-02-16 16:54:12.928472
    # .+?(?=T)+ date
    # [^T]+?(?=Z) time
    def make_proxies(self, raw_proxies):
        for proxy in raw_proxies['data']:
            created_at = self.get_proper_date_format(proxy['created_at'])
            protocol = ''.join(proxy['protocols'])
            self._proxies.append(
                {"socket": f"{proxy['ip']}:{proxy['port']}", "country": proxy['country'],
                 "anonymity": proxy['anonymityLevel'], "protocol": protocol, "createdAt": created_at, "scraper_name": type(self).__name__})
