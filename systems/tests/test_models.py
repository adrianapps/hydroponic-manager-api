from django.test import TestCase
from django.contrib.auth.models import User
from systems.models import HydroponicSystem, Measurement

class HydroponicSystemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testing321')
        self.system = HydroponicSystem.objects.create(
            name="Test System",
            description="This is my Test Hydroponic System",
            owner=self.user
        )

    def test_hydroponic_system_creation(self):
        self.assertEqual(self.system.name, 'Test System')
        self.assertEqual(self.system.description, 'This is my Test Hydroponic System')
        self.assertEqual(self.system.owner, self.user)
        self.assertEqual(self.system.slug, 'test-system')
        self.assertTrue(isinstance(self.system, HydroponicSystem))
        self.assertEqual(str(self.system), self.system.name)


class MeasurementModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testing321')
        self.system = HydroponicSystem.objects.create(
            name="Test System",
            description="This is my Test Hydroponic System",
            owner=self.user
        )
        self.measurement = Measurement.objects.create(
            system=self.system,
            temperature=25.5,
            ph=7.0,
            tds=500.0,
            description="This is my test measurement"
        )

    def test_measurement_creation(self):
        self.assertEqual(self.measurement.system, self.system)
        self.assertEqual(self.measurement.temperature, 25.5)
        self.assertEqual(self.measurement.ph, 7.0)
        self.assertEqual(self.measurement.tds, 500.0)
        self.assertEqual(self.measurement.description, "This is my test measurement")
        self.assertTrue(isinstance(self.measurement, Measurement))
        self.assertEqual(str(self.measurement), f"{self.system.name} measurement at {self.measurement.timestamp}")
