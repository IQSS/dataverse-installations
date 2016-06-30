from django.db import models
"""
# Create your models here.
class DataFilePreview(models.Model):

    doi = models.FileField()
    version = models.BigIntegerField(blank=True, null=True)

    versionnote = models.CharField(max_length=1000, blank=True, null=True)

    versionstate = models.CharField(max_length=255, choices=VERSION_STATE_CHOICES)

    versionnumber = models.BigIntegerField(blank=True, null=True)
    minorversionnumber = models.BigIntegerField(blank=True, null=True)

    dataset = models.ForeignKey(Dataset, blank=True, null=True)
    lastupdatetime = models.DateTimeField()

    unf = models.CharField(max_length=255, blank=True, null=True)

    archivenote = models.CharField(max_length=1000, blank=True, null=True)

    archivetime = models.DateTimeField(blank=True, null=True)

    availabilitystatus = models.TextField(blank=True, null=True)

    citationrequirements = models.TextField(blank=True, null=True)

    conditions = models.TextField(blank=True, null=True)
"""