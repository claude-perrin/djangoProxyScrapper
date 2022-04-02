from datetime import datetime

from django.db import models

#
# {"IPAddress": proxy['ip'], "Port": proxy['port'], "Country": proxy['country'],
#                  "Anonymity": proxy['anonymityLevel'], "CratedAt": created_at})
from django.utils import timezone


class Proxies(models.Model):
    ip = models.CharField(max_length=15)
    port = models.IntegerField()
    country = models.CharField(max_length=4, default="")
    anonymity = models.CharField(max_length=12, default="transparent")
    created_at = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.ip+":"+str(self.port)


class VerifiedProxies(models.Model):
    Proxy = models.ForeignKey(Proxies, on_delete=models.CASCADE)
    Success = models.IntegerField()
    Speed = models.IntegerField("Speed in ms")
    Latency = models.IntegerField("Latency in ms")
    # Updated = models.DateTimeField("Updated")
