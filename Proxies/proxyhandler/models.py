import datetime

from django.db import models

from django.utils import timezone


class Proxy(models.Model):
    socket = models.TextField(blank=False, unique=True, default=None)
    country = models.TextField(default=None)
    anonymity = models.TextField(default=None)
    success = models.IntegerField(default=0)
    protocol = models.TextField(default='')
    speed = models.FloatField("Speed in seconds", default=0.0)
    updated = models.DateTimeField('Updated', default=datetime.datetime.min)
    created_at = models.DateTimeField('date published', default=timezone.now)
    scraper_name = models.TextField(default=None)

    def __str__(self):
        return self.socket

    def get_info(self):
        return {"socket": self.socket, "success": self.success, "speed": self.speed, 'protocol': self.protocol,
                "updated": self.updated, "scraper_name": self.scraper_name}

    def get_socket(self):
        return self.socket

