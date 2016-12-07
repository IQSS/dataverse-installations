from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.
class IngestFormat(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, max_length=200)
