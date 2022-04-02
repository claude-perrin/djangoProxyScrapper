from django.http import HttpResponse
from .ProxyVerifier.ProxyVerify import verify_proxies
from .scrappers import freeproxy_scrapper as fp
from .models import Proxies


#
# {"IPAddress": proxy['ip'], "Port": proxy['port'], "Country": proxy['country'],
#                  "Anonymity": proxy['anonymityLevel'], "CratedAt": created_at})


# Ip = models.CharField(max_length=15)
# Port = models.IntegerField()
# Success = models.IntegerField()
# Speed = models.IntegerField("Speed in ms")
# Latency = models.IntegerField("Latency in ms")

def scrap(request):
    fp_proxies = fp.FreeProxyScrapper().scrap()
    for proxy in fp_proxies:
        Proxies(socket=proxy["socket"], country=proxy["country"],
                anonymity=proxy["anonymity"]).save()
    return HttpResponse(f"{fp_proxies}")


# {"Socket": self.socket,
# "Success": self.successful_connection_counter,
# "Speed": self.speed,
# "Latency": self.latency,
# "Updated": self.updated}

def verify(request):
    unverified_proxies = [i.__str__() for i in Proxies.objects.all()]  # TODO last updated 1h ago
    verified_proxies = [
        Proxies.objects.filter(socket=proxy['socket']).update(success=proxy['success'],
                                                              speed=proxy['speed'],
                                                              latency=proxy['latency'])
        for proxy in verify_proxies(unverified_proxies)
    ]

    return HttpResponse(f"{verified_proxies}")
