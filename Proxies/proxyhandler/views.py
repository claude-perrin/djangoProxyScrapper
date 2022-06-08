import csv

from django.db import IntegrityError
from django.http import HttpResponse,  FileResponse

from django.utils import timezone

from .ProxyVerifier.ProxyVerify import ProxyVerifier
from .Scraper import freeproxy_scrapper as fp
from .models import Proxy
from .Statistic.Statistic import Statistic
from django.db.models import Max


from django.shortcuts import render


def main_page(request):
    return render(request, 'proxyhandler/index.html')


def scrap(request):
    #TODO Thread to start both scrappers synch
    fp_proxies = fp.FreeProxyScrapper().scrap()
    for proxy in fp_proxies:
        try:
            Proxy(socket=proxy["socket"], country=proxy["country"], anonymity=proxy["anonymity"],
                  protocol=proxy["protocol"]).save()
        except IntegrityError as exc:
            print(exc)

    context = {
        'main_page': "Scrapped proxies",
        'proxies': fp_proxies,
    }
    return render(request, 'proxyhandler/show.html', context)


def verify(request):
    unverified_proxies = [i.socket for i in Proxy.objects.filter(updated__lte=timezone.now() - timezone.timedelta(0.010))]  # 0.010 = 15 min

    verified_proxies = ProxyVerifier(unverified_proxies).run().verified_proxies

    for proxy in verified_proxies:
        proxy_object = Proxy.objects.filter(socket=proxy['socket'])
        proxy_object.update(success=proxy['success'], speed=proxy['speed'], updated=timezone.now())

    context = {
        'main_page': "Proxies which passed verification",
        'proxies': [i.get_info() for i in Proxy.objects.filter(success__gt=0)],
    }

    return render(request, 'proxyhandler/show.html', context)


def statistic(request):
    s = Statistic
    successed_proxies = Proxy.objects.filter(success__gt=0)
    proxy_max_speed = Proxy.objects.aggregate(Max('speed'))

    Statistic.success_percentage(successed_proxies)
    Statistic.average_speed(successed_proxies)


def show(request):
    working_proxies = [i.get_info() for i in Proxy.objects.filter(success__gt=0)]
    context = {
        'main_page': "Proxies which are working",
        'proxies': working_proxies,
    }
    return render(request, 'proxyhandler/show.html', context)


def download_csv(request):
    data = [{i.socket} for i in Proxy.objects.filter(success__gt=0)]
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="working_proxies.csv"'},
    )
    writer = csv.writer(response)
    writer.writerows(data)

    return response


def download_txt(request):
    data = {i.socket + '\n' for i in Proxy.objects.filter(success__gt=0)}
    response = FileResponse(data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="working_proxies.txt"'
    return response


def test(request):
    # obj = Proxies.objects.get(socket="202.162.37.68:8080")
    # x = obj.success + 1
    # Proxies.objects.filter(socket="202.162.37.68:8080").update(success=x)
    proxies = [i for i in Proxy.objects.all().delete()]
    return HttpResponse("done")
