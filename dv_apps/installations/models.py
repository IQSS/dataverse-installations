from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from decimal import Decimal

# Create your models here.
@python_2_unicode_compatible
class Installation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0.0000'))
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0.0000'))
    logo = models.ImageField(upload_to='uploads/', null=True, blank=True)
    marker = models.ImageField(upload_to='uploads/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    version = models.CharField(max_length=6, unique=False, null=True, blank=True)
    def __str__(self):
        return self.name
    pass

@python_2_unicode_compatible
class Institution(models.Model):
    name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=False, default=Decimal('0.0000'))
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=False, default=Decimal('0.0000'))
    host = models.ForeignKey(
        Installation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name
