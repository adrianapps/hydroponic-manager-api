from django.contrib.auth.models import User
from rest_framework import serializers

from .models import HydroponicSystem, Measurement


class HydroponicSystemSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='systems:hydroponic-system-detail',
        lookup_field = 'slug'
    )
    class Meta:
        model = HydroponicSystem
        fields = ['url', 'id', 'name', 'description', 'owner', 'slug']



class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'system', 'temperature', 'ph', 'tds', 'description', 'timestamp']

    def validate_system(self, value):
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError('You can only create measurements for your own hydroponic systems')
        return value

