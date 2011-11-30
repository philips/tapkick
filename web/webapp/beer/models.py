import datetime

from django.core.mail import send_mail
from django.db import models

from beer_types import BEER_TYPE_CHOICES, KEG_SIZE_CHOICES

TAP_NUMBER_CHOICES = (
    (1, 'Tap number 1'),
    (2, 'Tap number 2'),
)


class Beer(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    beer_type = models.CharField(max_length=3, default='def', choices=BEER_TYPE_CHOICES)
    tap_number = models.IntegerField(choices=TAP_NUMBER_CHOICES)
    active = models.BooleanField(default=True)

    start_date = models.DateTimeField(default=datetime.datetime.now(), blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    size = models.FloatField("Size (in liters)", default=29.33, choices=KEG_SIZE_CHOICES)
    amount_left = models.FloatField("Amount left (in liters)", blank=True, null=True)
    ibu = models.PositiveIntegerField(default=0, help_text="International Bitterness Units (IBU)")
    abv = models.FloatField(default=0.0, help_text="Alcohol by Volume")

    class Meta:
        ordering = ('-active', '-start_date')

    def __unicode__(self):
        name = u'%s, %s' % (self.name, self.beer_type)
        if self.active:
            name += u' (#%s active)' % (self.tap_number)
        else:
            name += u' (#%s)' % (self.tap_number)
        return name

    def save(self, *args, **kwargs):
        """
        Tap cannot be active if it has ended,
        Tap with no amount must be full,
        Tap cannot have negative amount,
        Only one active tap per tap number
        """
        if self.end_date:
            self.active = False

        if self.amount_left != 0.0 and self.amount_left == None:
            self.amount_left = self.size
        elif self.amount_left < 0.0:
            self.amount_left = 0.0

        if self.active:
            for beer in Beer.objects.filter(tap_number=self.tap_number).exclude(id=self.id):
                beer.active = False
                beer.save()
        super(Beer, self).save(*args, **kwargs)

    def cups_left(self, oz_per_cup=12):
        """
        Return approximate number of cups left in this keg of beer.
        Converts amount_left to ounces, and divides that by 12 to get amount of
        12 ounce cups left.
        """
        liters_to_fl_ounces = 33.8140227
        return int(round((self.amount_left * liters_to_fl_ounces) / oz_per_cup))

    def percent_left(self):
        percent = self.amount_left / self.size
        if percent < 0.0:
            return 0.0
        elif percent > 1.0:
            return 1.0
        else:
            return percent


class User(models.Model):
    rfid = models.CharField("RFID", max_length=20)
    name = models.CharField(max_length=255, default='Beer Lover')
    email = models.EmailField(default="", blank=True, null=True)
    receive_alerts = models.BooleanField(default=True)
    private = models.BooleanField(default=False, help_text="Indicate a user does not want to appear on site")

    def __unicode__(self):
        return u'%s, %s' % (self.name, self.rfid)

    @classmethod
    def email_all_users(cls):
        """
        @TODO: A classmethod that emails all users
        to alert when beer is low
        """
        user_email_list = cls.objects.filter(
                receive_alerts=True, email__isnull=False).values_list('email', flat=True)
        subject = 'Beer is almost empty'
        message = 'Get more beer!'
        from_email = 'tapkick@rackspace.com'  # @TODO: Put this in settings
        send_mail(subject, message, from_email, user_email_list, fail_silently=True)


class Access(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    user = models.ForeignKey(User)
    beer = models.ForeignKey(Beer)
    temperature = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ["-time"]
        verbose_name_plural = "Accesses"

    def __unicode__(self):
        return u'%s, %s, %s, %s' % (self.time, self.user, self.beer, self.amount)

    def save(self):
        b = self.beer
        b.amount_left -= self.amount
        b.save()
        super(Access, self).save()
