import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from systems.models import HydroponicSystem, Measurement


class UserFactory(DjangoModelFactory):
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')

    class Meta:
        model = User


class HydroponicSystemFactory(DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    name = factory.Faker('word')
    description = factory.Faker('text')

    class Meta:
        model = HydroponicSystem


class MeasurementFactory(factory.django.DjangoModelFactory):
    system = factory.SubFactory(HydroponicSystemFactory)
    temperature = factory.Faker('pyfloat')
    ph = factory.Faker('pyfloat')
    tds = factory.Faker('pyfloat')
    description = factory.Faker('text')

    class Meta:
        model = Measurement
