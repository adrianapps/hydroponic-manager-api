from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import HydroponicSystem, Measurement
from .serializers import (
    HydroponicSystemSerializer,
    MeasurementSerializer,
    UserSerializer,
    HydroponicSystemDetailSerializer
)
from .permissions import IsOwner, IsSystemOwner
from .filters import MeasurementFilter, HydroponicSystemFilter


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint providing links to other endpoints.

    Returns:
       Response: A response containing links to different endpoints.
    """
    return Response({
        'register': reverse('systems:user-create', request=request, format=format),
        'hydroponic-systems': reverse('systems:hydroponic-system-list', request=request, format=format),
        'measurements': reverse('systems:measurement-list', request=request, format=format)
    })


class UserCreate(generics.CreateAPIView):
    """
    View for creating new user instances.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class HydroponicSystemList(generics.ListCreateAPIView):
    """
    View for listing and creating hydroponic systems owned by the authenticated user.
    """
    serializer_class = HydroponicSystemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = HydroponicSystemFilter
    ordering_fields = ['name', 'owner', 'slug']

    def get_queryset(self):
        """
        Retrieve all hydroponic systems owned by the authenticated user.

        :return: QuerySet of HydroponicSystem objects
        """
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Perform creation of a new hydroponic system owned by the authenticated user.

        :param serializer: Serializer instance
        """
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        else:
            print(serializer.errors)


class HydroponicSystemDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting specific hydroponic systems.
    """
    queryset = HydroponicSystem
    serializer_class = HydroponicSystemDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = 'slug'


class MeasurementList(generics.ListCreateAPIView):
    """
    View for listing and creating measurements associated with hydroponic systems owned by the authenticated user.
    """
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MeasurementFilter
    ordering_fields = ['timestamp', 'temperature', 'ph', 'tds']

    def get_queryset(self):
        """
        Retrieve all measurements associated with hydroponic systems owned by the authenticated user.

        :return: QuerySet of Measurement objects
        """
        return Measurement.objects.filter(system__owner=self.request.user)


class MeasurementDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting specific measurements.
    """
    queryset = Measurement
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated, IsSystemOwner]
