from django.test import TestCase
from django.contrib.auth.models import User
from systems.models import HydroponicSystem, Measurement
from .factories import UserFactory, HydroponicSystemFactory, MeasurementFactory


class HydroponicSystemModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.system = HydroponicSystemFactory(owner=self.user)

    def test_hydroponic_system_creation(self):
        self.assertEqual(self.system.owner, self.user)
        self.assertTrue(isinstance(self.system, HydroponicSystem))
        self.assertEqual(str(self.system), self.system.name)


class MeasurementModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.system = HydroponicSystemFactory(owner=self.user)
        self.measurement = MeasurementFactory(system=self.system)

    def test_measurement_creation(self):
        self.assertEqual(self.measurement.system, self.system)
        self.assertTrue(isinstance(self.measurement, Measurement))
        self.assertEqual(str(self.measurement), f"{self.system.name} measurement at {self.measurement.timestamp}")
