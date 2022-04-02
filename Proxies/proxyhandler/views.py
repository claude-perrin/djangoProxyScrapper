from django.db import IntegrityError
from django.http import HttpResponse
from .ProxyVerifier.ProxyVerify import verify_proxies
from .scrappers import freeproxy_scrapper as fp
from .models import Proxies


def scrap(request):
    fp_proxies = fp.FreeProxyScrapper().scrap()
    for proxy in fp_proxies:
        try:
            Proxies(socket=proxy["socket"], country=proxy["country"],
                    anonymity=proxy["anonymity"]).save()
        except IntegrityError:
            pass
    return HttpResponse(f"{fp_proxies}")


def verify(request):
    unverified_proxies = [i.__str__() for i in Proxies.objects.all()]  # TODO choose which are last updated 1h ago
    [Proxies.objects.filter
        (socket=proxy['socket']).update(success=proxy['success'], speed=proxy['speed'], latency=proxy['latency'])
        for proxy in verify_proxies(unverified_proxies)gi
    ]

    return HttpResponse(f"{Proxies.objects.filter(success__gt=0)}")


def working_proxies(request):
    z = [i.__str__() for i in Proxies.objects.filter(success__gt=0)]
    return HttpResponse(f"{z}")
