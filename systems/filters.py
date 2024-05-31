from django_filters import rest_framework as django_filters
from django_filters.widgets import RangeWidget

from .models import Measurement, HydroponicSystem


class HydroponicSystemFilter(django_filters.FilterSet):
    class Meta:
        model = HydroponicSystem
        fields = {
            'name': ['icontains'],
            'owner__username': ['iexact'],
            'slug': ['iexact'],
        }


class MeasurementFilter(django_filters.FilterSet):
    timestamp = django_filters.DateTimeFromToRangeFilter(
        widget=RangeWidget(attrs={'type': 'date'}))
    temperature = django_filters.RangeFilter()
    ph = django_filters.RangeFilter()
    tds = django_filters.RangeFilter()

    class Meta:
        model = Measurement
        fields = {
            'system__name': ['icontains']
        }
