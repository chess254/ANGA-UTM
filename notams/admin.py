from django.contrib import admin

# Register your models here.
from .models import NotamAirspace

from leaflet.admin import LeafletGeoAdmin

# Register your models here.

class NotamAirspaceAdmin(LeafletGeoAdmin):
    list_display = ( 'notam_number','created_by')


admin.site.register(NotamAirspace, NotamAirspaceAdmin)