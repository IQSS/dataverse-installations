from django.db import models
from django.utils.encoding import python_2_unicode_compatible

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

    rootdatafileid = models.BigIntegerField(default=-1)
    previousdatafileid = models.BigIntegerField(blank=True, null=True)

    checksumvalue = models.CharField(max_length=255)
    checksumtype = models.CharField(max_length=255)
    #md5 = models.CharField(max_length=255)
    restricted = models.BooleanField()

    def __str__(self):
        return '%s' % self.dvobject

    @property
    def id(self):
        if self.dvobject is None:
            return None
        return self.dvobject.id

    class Meta:
        ordering = ('dvobject',)
        managed = False
        db_table = 'datafile'

@python_2_unicode_compatible
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


@python_2_unicode_compatible
class DatafileCategory(models.Model):
    name = models.CharField(max_length=255)
    dataset = models.ForeignKey(DvObject)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        verbose_name_plural = 'Datafile categories'
        db_table = 'datafilecategory'

@python_2_unicode_compatible
class DatafileTag(models.Model):
    dtype = models.IntegerField(db_column='type')
    datafile = models.ForeignKey(DvObject)

    def __str__(self):
        return '%s' % self.dtype

    class Meta:
        managed = False
        db_table = 'datafiletag'


class FilemetadataDatafileCategory(models.Model):
    filecategories = models.ForeignKey(DatafileCategory, db_column='filecategories_id')
    filemetadatas = models.ForeignKey(FileMetadata, db_column='filemetadatas_id', primary_key=True)

    def __str__(self):
        return '%s' % self.filecategories

    class Meta:
        managed = False
        verbose_name = 'File metadata datafile category'
        verbose_name_plural = 'File metadata datafile categories'
        db_table = 'filemetadata_datafilecategory'
        #unique_together = (('filecategories_id', 'filemetadatas_id'),)
        unique_together = (('filecategories', 'filemetadatas'),)
