import abc

REQUEST_TIMEOUT = 5


class ProxyInterfaceAdapter(abc.ABC):
    def __new__(cls):
        cls_instance = super(ProxyInterfaceAdapter, cls).__new__(cls)
        cls_instance._proxies = []
        cls_instance._TIMEOUT = REQUEST_TIMEOUT
        return cls_instance

    @abc.abstractmethod
    def scrap(self):
        """
        Using url gets proxies
        :return: list of raw proxies
        """

    @abc.abstractmethod
    def request(self):
        """
        makes a request and handles exception
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

    @property
    def get_proxies(self):
        return self._proxies
