import datetime

from django.db import IntegrityError
from django.http import HttpResponse

from django.utils import timezone

from .ProxyVerifier.ProxyVerify import ProxyVerifier
from .scrappers import freeproxy_scrapper as fp
from .models import Proxies

from django.shortcuts import render


def main_page(request):
    return render(request, 'proxyhandler/index.html')


def scrap(request):
    fp_proxies = fp.FreeProxyScrapper().scrap()
    for proxy in fp_proxies:
        try:
            Proxies(socket=proxy["socket"], country=proxy["country"], anonymity=proxy["anonymity"],
                    protocol=proxy["protocol"]).save()
        except IntegrityError:
            pass

    context = {
        'main_page': "Scrapped proxies",
        'proxies': fp_proxies,
    }
    return render(request, 'proxyhandler/show.html', context)


# TODO load bar during verification
def verify(request):
    unverified_proxies = [i.__str__() for i in Proxies.objects.filter(
        updated__lte=timezone.now() - timezone.timedelta(0.010))]  # 0.010 = 15 min

    verified_proxies = ProxyVerifier(unverified_proxies).run().get_proxies()
    print(verified_proxies)

    [Proxies.objects.filter
     (socket=proxy['socket']).update(success=proxy['success'], speed=proxy['speed'], updated=timezone.now()) for proxy in verified_proxies
     ]
    context = {
        'main_page': "Proxies which passed verification",
        'proxies': [i.get_info() for i in Proxies.objects.filter(success__gt=0)],
    }

    return render(request, 'proxyhandler/show.html', context)


def show(request):
    working_proxies = [i.get_info() for i in Proxies.objects.filter(success__gt=0)]
    context = {
        'main_page': "Proxies which are working",
        'proxies': working_proxies,
    }
    return render(request, 'proxyhandler/show.html', context)


def download(request):
    working_proxies = Proxies.objects.filter(success__gt=0)


def test(request):
    proxies = [i for i in Proxies.objects.all().delete()]
    return HttpResponse("done")
