from django.db import models


class LastPostTimeStamp(models.Model):
    time_stamp = models.IntegerField()
