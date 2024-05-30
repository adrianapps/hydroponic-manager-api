from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import HydroponicSystem, Measurement
from .serializers import HydroponicSystemSerializer, MeasurementSerializer
from .permissions import IsOwner, IsSystemOwner

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'hydroponic-systems': reverse('systems:hydroponic-system-list', request=request, format=format),
        'measurements': reverse('systems:measurement-list', request=request, format=format)
    })

class HydroponicSystemList(generics.ListCreateAPIView):
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        else:
            print(serializer.errors)


class HydroponicSystemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HydroponicSystem
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = 'slug'


class MeasurementList(generics.ListCreateAPIView):
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Measurement.objects.filter(system__owner=self.request.user)


class MeasurementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Measurement
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated, IsSystemOwner]
