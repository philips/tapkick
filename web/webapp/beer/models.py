from django.db import models
from beer_types import TYPE_OF_BEER

NUMBER_OF_TAP = (
    (1, 'Tap number 1'),
    (2, 'Tap number 2'),
)

class Beer(models.Model):
    type = models.CharField(max_length=2, choices=TYPE_OF_BEER)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    size = models.FloatField("Size (in liters)", default=29.33)
    tap_number = models.IntegerField(choices=NUMBER_OF_TAP)
    active = models.BooleanField()

class User(models.Model):
    rfid = models.CharField("RFID", max_length=20)
    name = models.CharField(max_length=255)

class Access(models.Model):
    time = models.DateTimeField()
    amount = models.IntegerField()
    user = models.ForeignKey(User)
    beer = models.ForeignKey(Beer)

    class Meta:
        ordering = ["time"]
        verbose_name_plural = "Accesses"

