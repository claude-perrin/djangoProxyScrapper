import datetime

from django.db import IntegrityError
from django.http import HttpResponse

from .ProxyVerifier.ProxyVerify import verify_proxies
from .scrappers import freeproxy_scrapper as fp
from .models import Proxies

from django.shortcuts import render


def scrap(request):
    fp_proxies = fp.FreeProxyScrapper().scrap()
    for proxy in fp_proxies:
        try:
            Proxies(socket=proxy["socket"], country=proxy["country"], anonymity=proxy["anonymity"]).save()
        except IntegrityError:
            pass

    context = {
        'main_page': "Scrapped proxies",
        'proxies': fp_proxies,
    }
    return render(request, 'proxyhandler/index.html', context)


# TODO load bar during verification
# TODO take only not updated
def verify(request):
    unverified_proxies = [i.__str__() for i in Proxies.objects.filter(created_at__lte=datetime.date.today())]  # TODO choose which are last updated 1h ago
    [Proxies.objects.filter
     (socket=proxy['socket']).update(success=proxy['success'], speed=proxy['speed'], latency=proxy['latency'])
     for proxy in verify_proxies(unverified_proxies)
     ]

    context = {
        'main_page': "Proxies which passed verification",
        'proxies': Proxies.objects.filter(success__gt=0),
    }

    return render(request, 'proxyhandler/index.html', context)


def show(request):
    working_proxies = [i.get_info() for i in Proxies.objects.filter(success__gt=0)]
    context = {
        'main_page': "Proxies which are working",
        'proxies': working_proxies,
    }
    return render(request, 'proxyhandler/index.html', context)
