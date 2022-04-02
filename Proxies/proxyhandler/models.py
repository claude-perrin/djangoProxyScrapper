from datetime import datetime

from django.db import models

#
# {"IPAddress": proxy['ip'], "Port": proxy['port'], "Country": proxy['country'],
#                  "Anonymity": proxy['anonymityLevel'], "CratedAt": created_at})
from django.utils import timezone


class Proxies(models.Model):
    socket = models.TextField(blank=False, unique=True, default=None)
    country = models.TextField(default=None)
    anonymity = models.TextField(default=None)
    success = models.IntegerField(default=0)
    speed = models.IntegerField("Speed in ms", default=0)
    latency = models.IntegerField("Latency in ms", default=0)
    created_at = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return self.socket
