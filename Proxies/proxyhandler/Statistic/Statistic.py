class Statistic:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Statistic, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def success_percentage(proxies):
        success_list = [i["success"] for i in proxies]
        return round(sum(success_list) / len(success_list), 3)

    @staticmethod
    def average_speed(proxies):
        speed = [i["speed"] for i in proxies if i["speed"] != 0]
        if speed:
            return round(sum(speed) / len(speed), 3)
        return None

    @staticmethod
    def count_providers(providers):
        return [{i: providers.count(i)} for i in set(providers)]
