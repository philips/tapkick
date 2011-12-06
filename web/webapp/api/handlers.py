from piston.handler import BaseHandler

from beer.models import Beer

class BeersHandler(BaseHandler):
    allowed_methods = ('GET')
    fields = ('name', 'slug', 'beer_type', 'tap_number', 'active', 'size',
              'amount_left', 'abv')
    model = Beer

    def read(self, request):
        beers = Beer.objects.filter(active=True)
        return beers


class BeerHandler(BaseHandler):
    allowed_methods = ('GET')
    fields = ('name', 'slug', 'beer_type', 'tap_number', 'active', 'size',
              'amount_left', 'abv')
    model = Beer

    def read(self, request, tap_number):
        beer = Beer.objects.get(tap_number=tap_number, active=True)
        return beer
