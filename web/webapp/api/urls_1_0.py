from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from api.handlers import BeersHandler
from api.handlers import BeerHandler

beers_handler = Resource(handler=BeersHandler)
beer_handler = Resource(handler=BeerHandler)

urlpatterns = patterns('',
    url(r'^beers/?$', beers_handler),
    url(r'^beer/(?P<slug>[^/]+)', beer_handler),
)
