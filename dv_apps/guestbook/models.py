from __future__ import unicode_literals
from django.db import models
#from dv_apps.dataverses.models import Dataverse
from dv_apps.dvobjects.models import DvObject
from dv_apps.datasets.models import DatasetVersion

RESPONSE_TYPE_DOWNLOAD = 'Download'
RESPONSE_TYPE_EXPLORE = 'Explore'
RESPONSE_TYPE_SUBSET = 'Subset'

class GuestBook(models.Model):
    createtime = models.DateTimeField()
    emailrequired = models.NullBooleanField()
    enabled = models.NullBooleanField()
    institutionrequired = models.NullBooleanField()
    name = models.CharField(max_length=255, blank=True, null=True)
    namerequired = models.NullBooleanField()
    positionrequired = models.NullBooleanField()
    dataverse = models.ForeignKey(DvObject, blank=True, null=True)

    def __str__(self):
        if self.dataverse:
            return '%s' % self.dataverse
        return '%s' % self.id

    class Meta:
        managed = False
        db_table = 'guestbook'


class GuestBookResponse(models.Model):
    downloadtype = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    institution = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    responsetime = models.DateTimeField(blank=True, null=True)
    sessionid = models.CharField(max_length=255, blank=True, null=True)
    #authenticateduser = models.ForeignKey(Authenticateduser, blank=True, null=True)
    datafile = models.ForeignKey(DvObject, related_name='guestbook_datafile')
    dataset = models.ForeignKey(DvObject, related_name='guestbook_dataset')
    #datasetversion = models.ForeignKey(DatasetVersion, blank=True, null=True)
    guestbook = models.ForeignKey(GuestBook)

    def __str__(self):
        return self.downloadtype
        #return '%s - %s' % (self.id, self.responsetime)

    class Meta:
        managed = False
        db_table = 'guestbookresponse'
