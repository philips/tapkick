from django.db import models
from beer_types import BEER_TYPE_CHOICES

TAP_NUMBER_CHOICES = (
    (1, 'Tap number 1'),
    (2, 'Tap number 2'),
)


class Beer(models.Model):
    beer_type = models.CharField(max_length=3, choices=BEER_TYPE_CHOICES)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    size = models.FloatField("Size (in liters)", default=29.33)
    amount_left = models.FloatField("Amount left (in liters)", default=29.33)
    tap_number = models.IntegerField(choices=TAP_NUMBER_CHOICES)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s, %s liters left, %s, %s' % (self.name, self.amount_left, self.start_date, self.get_tap_number_display())

    """
    Return approximate number of cups left in this keg of beer.
    Converts amount_left to ounces, and divides that by 12 to get amount of
    12 ounce cups left.
    """
    def cups_left(self):
        return round((self.amount_left * 33.8140227) / 12)


class User(models.Model):
    rfid = models.CharField("RFID", max_length=20)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s, %s' % (self.name, self.rfid)


class Access(models.Model):
    time = models.DateTimeField()
    amount = models.FloatField()
    user = models.ForeignKey(User)
    beer = models.ForeignKey(Beer)

    class Meta:
        ordering = ["time"]
        verbose_name_plural = "Accesses"

    def __unicode__(self):
        return u'%s, %s, %s, %s' % (self.user, self.time, self.beer, self.amount)
