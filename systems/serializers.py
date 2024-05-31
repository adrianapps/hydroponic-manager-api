from django.contrib.auth.models import User
from rest_framework import serializers

from .models import HydroponicSystem, Measurement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(f"A user with {value} email already exists")
        return value


class HydroponicSystemSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='systems:hydroponic-system-detail',
        lookup_field='slug'
    )

    class Meta:
        model = HydroponicSystem
        fields = ['url', 'id', 'name', 'description', 'owner', 'slug']


class HydroponicSystemDetailSerializer(serializers.ModelSerializer):
    last_measurements = serializers.SerializerMethodField()

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'description', 'owner', 'slug', 'last_measurements']

    def get_last_measurements(self, obj):
        measurements = Measurement.objects.filter(system=obj).order_by('-timestamp')[:10]
        request = self.context.get('request')
        return LastMeasurementsSerializer(measurements, many=True, context={'request': request}).data


class LastMeasurementsSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='systems:measurement-detail',
    )

    class Meta:
        model = Measurement
        fields = ['url', 'id', 'temperature', 'ph', 'tds', 'description', 'timestamp']


class MeasurementSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='systems:measurement-detail',
    )
    system = serializers.HyperlinkedRelatedField(
        view_name='systems:hydroponic-system-detail',
        lookup_field='slug',
        queryset=HydroponicSystem.objects.all()
    )

    class Meta:
        model = Measurement
        fields = ['url', 'id', 'system', 'temperature', 'ph', 'tds', 'description', 'timestamp']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['system'].queryset = HydroponicSystem.objects.filter(owner=request.user)

    def validate_system(self, value):
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError('You can only create measurements for your own hydroponic systems')
        return value
