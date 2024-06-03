from django.contrib.auth.models import User
from rest_framework import serializers

from .models import HydroponicSystem, Measurement


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        """
        Create a new user instance.

        Args:
            validated_data (dict): Validated data for user creation.

        Returns:
            User: Newly created user instance.
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate_email(self, value):
        """
        Validate uniqueness of email.

        Args:
            value (str): Email to validate.

        Returns:
            str: Validated email.
        """
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(f"A user with {value} email already exists")
        return value


class HydroponicSystemSerializer(serializers.ModelSerializer):
    """
    Serializer for the HydroponicSystem model.
    """
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
        """
        Retrieve last measurements for the system.

        Args:
           obj (HydroponicSystem): Hydroponic system object.

        Returns:
           list: Serialized last measurements.
        """
        measurements = obj.last_measurements_prefetched
        request = self.context.get('request')
        return LastMeasurementsSerializer(measurements, many=True, context={'request': request}).data


class LastMeasurementsSerializer(serializers.ModelSerializer):
    """
    Serializer for the last 10 measurements of a HydroponicSystem.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='systems:measurement-detail',
    )

    class Meta:
        model = Measurement
        fields = ['url', 'id', 'temperature', 'ph', 'tds', 'description', 'timestamp']


class MeasurementSerializer(serializers.ModelSerializer):
    """
    Serializer for the Measurement model.
    """
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
        """
        Initialize the MeasurementSerializer instance.

        This method customizes the queryset of the 'system' field based on the requesting user.

        Args:
           *args: Variable length argument list.
           **kwargs: Arbitrary keyword arguments.

        Returns:
           None
        """
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['system'].queryset = HydroponicSystem.objects.filter(owner=request.user)

    def validate_system(self, value):
        """
        Validate if the user owns the system.

        Args:
            value (HydroponicSystem): Hydroponic system object.

        Returns:
            HydroponicSystem: Validated hydroponic system object.
        """
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError('You can only create measurements for your own hydroponic systems')
        return value
