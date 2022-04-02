import requests

from AbstractProxyAdapter import ProxyInterfaceAdapter
import re


class GeonodeProxyScrapper(ProxyInterfaceAdapter):
    URL = 'https://proxylist.geonode.com/api/proxy-list?limit=200&page=1&sort_by=lastChecked&sort_type=desc'
    Proxies = list()

    def scrap(self):
        response = requests.get(self.URL)
        proxies = response.json()
        self.make_proxies(proxies)
        return self.Proxies

    def get_proper_date_format(self, data):
        print(data)
        date = re.compile(r".+?(?=T)+").search(data).group()
        time = re.compile(r"[^T]+?(?=Z)").search(data).group()
        return date + ' ' + time

    # 2022-02-16 16:54:12.928472
    # .+?(?=T)+ date
    # [^T]+?(?=Z) time
    def make_proxies(self, raw_proxies):
        for proxy in raw_proxies['data'][:5]:  #-------------------------------------------------------[:5]
            created_at = self.get_proper_date_format(proxy['created_at'])
            self.Proxies.append(
                {"IPAddress": proxy['ip'], "Port": proxy['port'], "Country": proxy['country'],
                 "Anonymity": proxy['anonymityLevel'], "CratedAt": created_at})

if __name__ == '__main__':
    x = GeonodeProxyScrapper().scrap()
    print(x)