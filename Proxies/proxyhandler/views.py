from django.http import HttpResponse
from .ProxyVerifier.ProxyVerify import verify_proxies
from .scrappers import freeproxy_scrapper as fp
from .models import Proxies, VerifiedProxies


#
# {"IPAddress": proxy['ip'], "Port": proxy['port'], "Country": proxy['country'],
#                  "Anonymity": proxy['anonymityLevel'], "CratedAt": created_at})


# Ip = models.CharField(max_length=15)
# Port = models.IntegerField()
# Success = models.IntegerField()
# Speed = models.IntegerField("Speed in ms")
# Latency = models.IntegerField("Latency in ms")

def verify(request):
    unverified_proxies = Proxies.objects.all()
    return HttpResponse(f"{[i.__str__() for i in unverified_proxies]}")


def scrap(request):
    fp_proxies = fp.FreeProxyScrapper().scrap()
    for proxy in fp_proxies:
        Proxies(ip=proxy["IPAddress"], port=proxy["Port"], country=proxy["Country"],
                anonymity=proxy["Anonymity"]).save()
    return HttpResponse(f"{fp_proxies}")
