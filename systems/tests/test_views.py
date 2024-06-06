from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .factories import HydroponicSystemFactory, UserFactory, MeasurementFactory
from systems.models import HydroponicSystem, Measurement


class APIRootTests(APITestCase):
    def test_api_root(self):
        url = reverse('systems:api-root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('register', response.data)
        self.assertIn('hydroponic-systems', response.data)
        self.assertIn('measurements', response.data)
        self.assertIn('swagger', response.data)
        self.assertIn('redoc', response.data)


class UserCreateTests(APITestCase):
    def test_post(self):
        url = reverse('systems:user-create')
        data = {
            'email': 'test@test.com',
            'username': 'testuser',
            'password': 'testing321'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')


class HydroponicSystemListTests(APITestCase):
    def setUp(self):
        self.url = reverse('systems:hydroponic-system-list')
        self.user = UserFactory()
        self.system = HydroponicSystemFactory(owner=self.user)
        self.client.force_authenticate(user=self.user)
        self.data = {
            'name': 'Test System',
            'description': 'This is my Test System',
            'owner': self.user.pk,
        }

    def test_get(self):
        response = self.client.get(self.url)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_authorized(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HydroponicSystem.objects.count(), 2)

    def test_post_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class HydroponicSystemDetailTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.system = HydroponicSystemFactory(owner=self.user)
        self.url = reverse('systems:hydroponic-system-detail', kwargs={'slug': self.system.slug})
        self.client.force_authenticate(user=self.user)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {
            'name': 'Updated Name',
            'description': 'Updated Description',
            'owner': self.user.pk
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HydroponicSystem.objects.get(pk=self.system.pk).name, 'Updated Name')

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(HydroponicSystem.objects.filter(pk=self.system.pk).exists())


class MeasurementListTests(APITestCase):
    def setUp(self):
        self.url = reverse('systems:measurement-list')
        self.user = UserFactory()
        self.system = HydroponicSystemFactory(owner=self.user)
        self.measurement = MeasurementFactory(system=self.system)
        self.client.force_authenticate(user=self.user)
        self.data = {
            'system': reverse('systems:hydroponic-system-detail', kwargs={'slug': self.system.slug}),
            'temperature': 25.5,
            'ph': 6.0,
            'tds': 500,
            'description': 'This is my test measurement'
        }

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_authorized(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Measurement.objects.count(), 2)

    def test_post_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MeasurementDetailTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.system = HydroponicSystemFactory(owner=self.user)
        self.measurement = MeasurementFactory(system=self.system)
        self.url = reverse('systems:measurement-detail', kwargs={'pk': self.measurement.pk})
        self.client.force_authenticate(user=self.user)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {
            'system': reverse('systems:hydroponic-system-detail', kwargs={'slug': self.system.slug}),
            'temperature': 25.5,
            'ph': 6.0,
            'tds': 500,
            'description': 'This is my updated test measurement'
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Measurement.objects.get(pk=self.measurement.pk).description,
                         "This is my updated test measurement")

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Measurement.objects.filter(pk=self.measurement.pk).exists())
