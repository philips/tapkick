from django.db import models
from beer_types import BEER_TYPE_CHOICES

TAP_NUMBER_CHOICES = (
    (1, 'Tap number 1'),
    (2, 'Tap number 2'),
)

class Beer(models.Model):
    beer_type = models.CharField(max_length=3, choices=BEER_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    size = models.FloatField("Size (in liters)", default=29.33)
    amount_left = models.FloatField("Amount left (in liters)", default=29.33)
    tap_number = models.IntegerField(choices=TAP_NUMBER_CHOICES)
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

