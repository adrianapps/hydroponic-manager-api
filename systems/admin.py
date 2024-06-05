from django.contrib import admin

from .models import HydroponicSystem, Measurement


class MeasurementInLine(admin.TabularInline):
    model = Measurement
    extra = 3


class HydroponicSystemAdmin(admin.ModelAdmin):
    inlines = [MeasurementInLine]
    list_display = ['name', 'owner', 'slug']
    list_filter = ['owner']
    search_fields = ['name', 'owner__username', 'slug']

class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['system', 'timestamp']
    list_filter = ['system', 'timestamp']
    search_fields = ['system__name', 'timestamp', 'temperature', 'ph', 'tds']


admin.site.register(HydroponicSystem, HydroponicSystemAdmin)
admin.site.register(Measurement, MeasurementAdmin)
