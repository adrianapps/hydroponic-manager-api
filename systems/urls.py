from django.urls import path

from .views import HydroponicSystemList, HydroponicSystemDetail, MeasurementList

urlpatterns = [
    path('hydroponic_systems/', HydroponicSystemList.as_view(), name='hydroponicsystems-list'),
    path('hydroponic_systems/<slug:slug>/', HydroponicSystemDetail.as_view(), name='hydroponicsystem-detail'),
    path('measurements/', MeasurementList.as_view(), name='measurement-list'),
]