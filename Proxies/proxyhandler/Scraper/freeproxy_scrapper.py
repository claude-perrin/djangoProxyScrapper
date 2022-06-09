import lxml.html
import requests
from .AbstractProxyAdapter import ProxyInterfaceAdapter


class FreeProxyScrapper(ProxyInterfaceAdapter):
    URL = 'https://free-proxy-list.net/'

    def scrap(self):
        html = self.request()
        if html is not None:
            doc = lxml.html.fromstring(html.content)
            proxies_table = doc.xpath('//table[@class="table table-striped table-bordered"]/tbody/tr')
            self.make_proxies(proxies_table)
        return self._proxies

    def request(self):
        try:
            return requests.get(self.URL)
        except requests.exceptions.ConnectionError:
            return None

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
            protocol = 'http' if proxy[6].text == 'no' else 'https'
            # self.get_proper_date_format(proxy[7].text)
            self._proxies.append(
                {"socket": f"{proxy[0].text}:{proxy[1].text}", "country": proxy[2].text,
                 "anonymity": proxy[4].text, "protocol": protocol, "scraper_name": type(self).__name__})
