from __future__ import unicode_literals

from django.db import models
from django.utils.html import format_html, mark_safe

from dv_apps.dvobjects.models import DvObject
from dv_apps.dataverses.models import Dataverse


class HarvestingDataverseConfig(models.Model):
    archivedescription = models.TextField(blank=True, null=True)
    archiveurl = models.CharField(max_length=255, blank=True, null=True)
    harveststyle = models.CharField(max_length=255, blank=True, null=True)
    harvesttype = models.CharField(max_length=255, blank=True, null=True)
    harvestingset = models.CharField(max_length=255, blank=True, null=True)
    harvestingurl = models.CharField(max_length=255, blank=True, null=True)
    dataverse = models.ForeignKey(DvObject, blank=True, null=True)

    def __str__(self):
        return self.archiveurl

    class Meta:
        managed = False
        db_table = 'harvestingdataverseconfig'

    def get_dataverse_name(self):
        """The orig model connects to DvObject, not Dataverse directly"""
        if not self.dataverse:
            return 'n/a'

        try:
            actual_dataverse = Dataverse.objects.get(pk=self.dataverse.id)
        except Dataverse.DoesNotExist:
            return 'not found'

        return str(actual_dataverse)
    dataverse_name = property(get_dataverse_name)



class HarvestingClient(models.Model):
    """From inspectdb"""    
    name = models.CharField(unique=True, max_length=255)

    archivedescription = models.TextField(blank=True, null=True)
    archiveurl = models.CharField(max_length=255, blank=True, null=True)

    deleted = models.NullBooleanField()

    harveststyle = models.CharField(max_length=255, blank=True, null=True)
    harvesttype = models.CharField(max_length=255, blank=True, null=True)

    harvestingnow = models.NullBooleanField()
    harvestingset = models.CharField(max_length=255, blank=True, null=True)
    harvestingurl = models.CharField(max_length=255, blank=True, null=True)

    metadataprefix = models.CharField(max_length=255, blank=True, null=True)

    scheduledayofweek = models.IntegerField(blank=True, null=True)
    schedulehourofday = models.IntegerField(blank=True, null=True)
    scheduleperiod = models.CharField(max_length=255, blank=True, null=True)
    scheduled = models.NullBooleanField()

    dataverse = models.ForeignKey(DvObject, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'harvestingclient'
