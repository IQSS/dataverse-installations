from django.db import models

from dv_apps.dvobjects.models import DvObject
from dv_apps.datasets.models import DatasetVersion

INGEST_STATUS_NONE = 'A' # ASCII 65
INGEST_STATUS_SCHEDULED = 'B' # ASCII 66
INGEST_STATUS_INPROGRESS = 'C' # ASCII 67
INGEST_STATUS_ERROR = 'D' # ASCII 68

class Datafile(models.Model):
    dvobject = models.OneToOneField(DvObject, db_column='id', primary_key=True)

    name = models.CharField(max_length=255, blank=True, null=True)

    contenttype = models.CharField(max_length=255)

    filesystemname = models.CharField(max_length=255)

    filesize = models.BigIntegerField(blank=True, null=True)

    ingeststatus = models.CharField(max_length=1, blank=True, null=True)

    md5 = models.CharField(max_length=255)

    restricted = models.BooleanField()

    def __str__(self):
        return '%s' % self.dvobject

    class Meta:
        ordering = ('dvobject',)
        managed = False
        db_table = 'datafile'

class FileMetadata(models.Model):
    description = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=255)
    restricted = models.NullBooleanField()
    version = models.BigIntegerField(blank=True, null=True)
    datafile = models.ForeignKey(DvObject)
    datasetversion = models.ForeignKey(DatasetVersion)

    def __str__(self):
        return self.label

    class Meta:
        #ordering = ('datafile',)
        managed = False

    class Meta:
        managed = False
        db_table = 'filemetadata'
