from piston.handler import BaseHandler

from beer.models import Keg, BeerType

class KegsHandler(BaseHandler):
    allowed_methods = ('GET')
    fields = ('beer_type', 'tap_number', 'active', 'size', 'amount_left')
    model = Keg

    def read(self, request):
        kegs = Keg.objects.filter(active=True)
        return kegs


class KegHandler(BaseHandler):
    allowed_methods = ('GET')
    fields = ('beer_type', 'tap_number', 'active', 'size', 'amount_left')
    model = Keg

    def read(self, request, tap_number):
        keg = Keg.objects.get(tap_number=tap_number, active=True)
        return keg
