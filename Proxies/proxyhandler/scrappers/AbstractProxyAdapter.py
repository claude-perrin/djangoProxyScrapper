import abc


class ProxyInterfaceAdapter(abc.ABC):
    Proxies = list()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ProxyInterfaceAdapter, cls).__new__(cls)
        return cls.instance

    @abc.abstractmethod
    def scrap(self):
        """
        Using url gets proxies
        :return: list of raw proxies
        """

    @abc.abstractmethod
    def make_proxies(self, raw_proxies):
        """
        Makes namedtuple from the scrapped proxy
        :return: namedtuple()
        """

    @abc.abstractmethod
    def get_proper_date_format(self, data):
        """
        Using Regex, fit scrapped data in proper format
        :return: Satisfiable date format
                """
