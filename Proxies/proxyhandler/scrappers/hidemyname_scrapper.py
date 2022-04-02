
import lxml.html
import requests
from .AbstractProxyAdapter import ProxyInterfaceAdapter


class FreeProxyScrapper(ProxyInterfaceAdapter):
    URL = 'https://hidemy.name/en/proxy-list/#list'
    Proxies = list()

    def scrap(self):
        html = requests.get(self.URL)
        doc = lxml.html.fromstring(html.content)
        proxies_table = doc.xpath('//div[@class="table_block"]/tbody/tr')
        self.make_proxies(proxies_table)

    def get_proper_date_format(self, data):
        """

        :param data:
        :return:
        """

    #     time_unit = re.compile(r"(sec)").search(data).group()
    #     passed_time = int(re.compile(r"\d").search(data).group())
    #     f = datetime.now().time() - passed_time
    #     print(f)

    def make_proxies(self, raw_proxies):
        for proxy in raw_proxies:
            proxy = proxy.getchildren()
            # self.get_proper_date_format(proxy[7].text)
            self.Proxies.append(
                {"IPAddress": proxy[0].text, "Port": proxy[1].text, "Country": proxy[2].text,
                 "Anonymity": proxy[4].text})

if __name__ == '__main__':
    x = FreeProxyScrapper()
    x.scrap()