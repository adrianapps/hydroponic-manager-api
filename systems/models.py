from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.fields import AutoSlugField

class HydroponicSystem(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='name', overwrite=True, unique=True)

    def __str__(self):
        return self.name

class Measurement(models.Model):
    system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE)
    temperature = models.FloatField()
    ph = models.FloatField()
    tds = models.FloatField()
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.system.name} measurement at {self.timestamp}"
