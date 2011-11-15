from beer.models import Beer
from beer.models import Access
from beer.models import User
from django.contrib import admin

def amount_in_liters(obj):
    if type(obj) == Beer:
        return "%s liters" % obj.amount_left
    else:
        return "%s liters" % obj.amount

class BeerAdmin(admin.ModelAdmin):
    list_display = ('name', amount_in_liters, 'cups_left', 'start_date', 'end_date', 'tap_number', 'active')
    list_filter = ('name',)

class AccessAdmin(admin.ModelAdmin):
    list_display = ('user', amount_in_liters, 'beer', 'time')

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'rfid')

admin.site.register(Beer, BeerAdmin)
admin.site.register(Access, AccessAdmin)
admin.site.register(User, UserAdmin)
