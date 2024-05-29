from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import HydroponicSystem, Measurement
from .serializers import HydroponicSystemSerializer, MeasurementSerializer


class HydroponicSystemList(generics.ListCreateAPIView):
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HydroponicSystemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HydroponicSystem
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'


class MeasurementList(generics.ListCreateAPIView):
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Measurement.objects.filter(system__owner=self.request.user)
