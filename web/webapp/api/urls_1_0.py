from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from api.handlers import KegsHandler
from api.handlers import KegHandler

kegs_handler = Resource(handler=KegsHandler)
keg_handler = Resource(handler=KegHandler)

urlpatterns = patterns('',
    url(r'^kegs/?$', kegs_handler),
    url(r'^keg/(?P<tap_number>[^/]+)', keg_handler),
)
