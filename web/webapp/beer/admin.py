from beer.models import Beer, User, Access
from django.contrib import admin


def amount_in_liters(obj):
    if type(obj) == Beer:
        return "%s liters" % obj.amount_left
    else:
        return "%s liters" % obj.amount


class BeerAdmin(admin.ModelAdmin):
    list_display = ('name', amount_in_liters, 'cups_left',
                    'start_date', 'end_date', 'tap_number', 'active')
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name', )}
    search_fields = ('name',)

admin.site.register(Beer, BeerAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'rfid', 'email', 'receive_alerts', 'private')
    list_editable = ('receive_alerts', 'private')
    list_filter = ('receive_alerts', 'private')
    search_fields = ('name',)

admin.site.register(User, UserAdmin)


class AccessAdmin(admin.ModelAdmin):
    list_display = ('user', amount_in_liters, 'beer', 'time', 'temperature')
    list_filter = ('beer', 'time',)

admin.site.register(Access, AccessAdmin)
