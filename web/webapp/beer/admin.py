from beer.models import Keg, BeerType, User, Access
from django.contrib import admin


def amount_in_liters(obj):
    if type(obj) == Keg:
        return "%s liters" % obj.amount_left
    else:
        return "%s liters" % obj.amount


class KegAdmin(admin.ModelAdmin):
    list_display = ('beer_type', amount_in_liters, 'cups_left',
                    'start_date', 'end_date', 'tap_number', 'active')
    list_filter = ('beer_type',)

admin.site.register(Keg, KegAdmin)


class BeerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'beer_type')
    prepopulated_fields = {'slug': ('name', )}
    search_fields = ('name',)

admin.site.register(BeerType, BeerTypeAdmin) 


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'rfid', 'email', 'receive_alerts', 'private')
    list_editable = ('receive_alerts', 'private')
    list_filter = ('receive_alerts', 'private')
    search_fields = ('name',)

admin.site.register(User, UserAdmin)


class AccessAdmin(admin.ModelAdmin):
    list_display = ('user', amount_in_liters, 'keg', 'time', 'temperature')
    list_filter = ('keg', 'time',)

admin.site.register(Access, AccessAdmin)
