import csv
import datetime

from django.db import IntegrityError
from django.http import HttpResponse

from django.utils import timezone
from django.views import View

from .ProxyVerifier.ProxyVerify import ProxyVerifier
from .scrappers import freeproxy_scrapper as fp
from .models import Proxies
from .FileManager import FileManager

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
            pass  # TODO handle error

    context = {
        'main_page': "Scrapped proxies",
        'proxies': fp_proxies,
    }
    return render(request, 'proxyhandler/show.html', context)


# TODO load bar during verification
def verify(request):
    unverified_proxies = [i.socket for i in Proxies.objects.filter(
        updated__lte=timezone.now() - timezone.timedelta(0.010))]  # 0.010 = 15 min

    verified_proxies = ProxyVerifier(unverified_proxies).run().verified_proxies

    for proxy in verified_proxies:
        proxy_object = Proxies.objects.filter(socket=proxy['socket'])
        proxy_object.update(success=proxy['success'], speed=proxy['speed'], updated=timezone.now())

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


class Downloader(View):

    def get(self, request, method):
        file_manager = {"txt": self.download_txt,
                        "csv": self.download_csv}
        return file_manager[method]()

    @staticmethod
    def download_csv():
        data = [{i.socket} for i in Proxies.objects.filter(success__gt=0)]
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="working_proxies.csv"'},
        )
        writer = csv.writer(response)
        writer.writerows(data)

        return response

    @staticmethod
    def download_txt():  # TODO class view
        data = {i.socket + '\n' for i in Proxies.objects.filter(success__gt=0)}
        response = HttpResponse(data, content_type='application/text charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="working_proxies.txt"'
        return response


def test(request):
    proxies = [i for i in Proxies.objects.all().delete()]
    return HttpResponse("done")
