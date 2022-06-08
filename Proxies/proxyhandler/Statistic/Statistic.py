class Statistic:
    @staticmethod
    def success_percentage(proxies):
        success_list = [i["success"] for i in proxies]
        return round(sum(success_list) / len(success_list), 3)

    @staticmethod
    def average_speed(proxies):
        speed = [i["speed"] for i in proxies if i["speed"] is not 0]
        if speed:
            return round(sum(speed) / len(speed), 3)
        return None
