import os, sys

sys.path.append('/home/tapkick/tapkick/web/webapp')
sys.path.append('/home/tapkick/tapkick/web/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

def django_patcher():
  from django.db.backends.mysql import base
  def valid_connection_replacement(self):
    return self.connection is not None
  base.DatabaseWrapper._valid_connection = valid_connection_replacement

application = django.core.handlers.wsgi.WSGIHandler()
