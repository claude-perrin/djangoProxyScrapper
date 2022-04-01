from django.db import models


class Proxies(models.Model):
    Ip = models.CharField(max_length=15)
    Port = models.IntegerField()
    Success = models.IntegerField()
    Speed = models.IntegerField("Speed in ms")
    Latency = models.IntegerField("Latency in ms")
    # pub_date = models.DateTimeField('date published')
    # Updated = models.DateTimeField("Updated")



