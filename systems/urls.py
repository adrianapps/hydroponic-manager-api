from django.urls import path

from .views import HydroponicSystemList, HydroponicSystemDetail, MeasurementList, MeasurementDetail, api_root, UserCreate

app_name = 'systems'

urlpatterns = [
    path('', api_root, name='api-root'),
    path('register/', UserCreate.as_view(), name='user-create'),
    path('hydroponic-systems/', HydroponicSystemList.as_view(), name='hydroponic-system-list'),
    path('hydroponic-systems/<slug:slug>/', HydroponicSystemDetail.as_view(), name='hydroponic-system-detail'),
    path('measurements/', MeasurementList.as_view(), name='measurement-list'),
    path('measurements/<int:pk>/', MeasurementDetail.as_view(), name='measurement-detail'),
]