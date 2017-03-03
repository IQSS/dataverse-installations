from django.db import models
from dv_apps.dvobjects.models import DvObject
from dv_apps.harvesting.models import HarvestingClient

PROTOCOL_DOI = "doi"
PROTOCOL_DOI_URL_BASE = 'http://dx.doi.org'

PROTOCOL_HDL = 'hdl'
PROTOCOL_HDL_URL_BASE = 'http://hdl.handle.net'

VERSION_STATE_RELEASED = 'RELEASED'
VERSION_STATE_DRAFT = 'DRAFT'
VERSION_STATE_DEACCESSIONED = 'DEACCESSIONED'
VERSION_STATE_ARCHIVED = 'ARCHIVED'

VERSION_STATES = (VERSION_STATE_RELEASED, VERSION_STATE_DRAFT, VERSION_STATE_DEACCESSIONED)
VERSION_STATE_CHOICES = [ (x, x) for x in VERSION_STATES]

# First, define the Manager subclass.
class DatasetManager(models.Manager):
    def get_queryset(self):
        return super(DatasetManager, self).get_queryset().select_related('dvobject')


class Dataset(models.Model):
    dvobject = models.OneToOneField(DvObject, db_column='id', primary_key=True)

    authority = models.CharField(max_length=255, blank=True, null=True)
    doiseparator = models.CharField(max_length=255, blank=True, null=True)

    fileaccessrequest = models.BooleanField()

    globalidcreatetime = models.DateTimeField(blank=True, null=True)

    identifier = models.CharField(max_length=255)

    protocol = models.CharField(max_length=255, blank=True, null=True)

    #guestbook = models.ForeignKey('Guestbook', blank=True, null=True)

    thumbnailfile = models.ForeignKey(DvObject, blank=True, null=True, related_name="thumbfile")

    harvestingclient = models.ForeignKey(HarvestingClient,
                                         models.DO_NOTHING,
                                         blank=True,
                                         null=True)

    objects = DatasetManager()

    def identifier_string(self):
        return self.__str__()

    @property
    def id(self):
        if self.dvobject is None:
            return None
        return self.dvobject.id


    def __str__(self):
        if self.dvobject:
            return '%s:%s%s%s' % (
                    self.protocol,
                    self.authority,
                    self.doiseparator,
                    self.identifier)
        return 'n/a'

    class Meta:
        managed = False
        db_table = 'dataset'
        unique_together = (('authority', 'protocol', 'identifier', 'doiseparator'),)

    @staticmethod
    def get_dataset_by_persistent_id(persistent_id):
        """quick/dirty method to parse a persistent_id -- is probably incorrect
            Based on these examples:
            doi:10.5072/FK2/BYM3IW => (doi) (10.5072/FK2) (BYM3IW)
            hdl:1902.1/xxxxx => (hdl) (1902.1) (xxxx)
        """
        if persistent_id is None:
            return None

        doi_sep = '/'

        split1 = persistent_id.split(':', 1)
        if len(split1) < 2:
            return None

        protocol = split1[0]
        remaining_parts = ':'.join(split1[1:])
        if protocol == PROTOCOL_DOI:
            # example: doi:10.5072/FK2/BYM3IW => (doi) (10.5072/FK2/BYM3IW)
            authority = doi_sep.join(remaining_parts.split(doi_sep)[:-1])
            identifier = remaining_parts.split(doi_sep)[-1]

        elif protocol == PROTOCOL_HDL:
            # example: hdl:1902.1/111012
            authority = remaining_parts.split(doi_sep)[0]
            identifier = remaining_parts.split(doi_sep)[-1]
        else:
            return None

        lookup_params = dict(protocol=protocol,
                            authority=authority,
                            identifier=identifier)

        return Dataset.objects.filter(**lookup_params).first()  # at most 1

        #//
        #//  or this one: (hdl) (1902.1/xxxxx)

    def get_persistent_url(self):

        if self.protocol == PROTOCOL_DOI:
            url = '%s/%s/%s' % (PROTOCOL_DOI_URL_BASE, self.authority, self.identifier)
        elif self.protocol == PROTOCOL_HDL:
            url = '%s/%s/%s' % (PROTOCOL_HDL_URL_BASE, self.authority, self.identifier)
        else:
            raise Exception('unknown protocol: %s for dataset id: %s' % (self.protocol, self.id))

        return url



class DatasetVersion(models.Model):

    dataset = models.ForeignKey(Dataset)

    # ----------------------------------
    # Version info
    # ----------------------------------
    version = models.BigIntegerField(blank=True, null=True)

    versionnote = models.CharField(max_length=1000, blank=True, null=True)

    versionstate = models.CharField(max_length=255, choices=VERSION_STATE_CHOICES)

    versionnumber = models.BigIntegerField(blank=True, null=True)
    minorversionnumber = models.BigIntegerField(blank=True, null=True)

    lastupdatetime = models.DateTimeField()

    unf = models.CharField(max_length=255, blank=True, null=True)

    archivenote = models.CharField(max_length=1000, blank=True, null=True)

    archivetime = models.DateTimeField(blank=True, null=True)

    #availabilitystatus = models.TextField(blank=True, null=True)

    #citationrequirements = models.TextField(blank=True, null=True)

    #conditions = models.TextField(blank=True, null=True)

    #confidentialitydeclaration = models.TextField(blank=True, null=True)

    #contactforaccess = models.TextField(blank=True, null=True)

    createtime = models.DateTimeField()

    #dataaccessplace = models.TextField(blank=True, null=True)

    deaccessionlink = models.CharField(max_length=255, blank=True, null=True)

    #depositorrequirements = models.TextField(blank=True, null=True)

    #disclaimer = models.TextField(blank=True, null=True)

    #fileaccessrequest = models.NullBooleanField()

    inreview = models.NullBooleanField()


    #license = models.CharField(max_length=255, blank=True, null=True)


    #originalarchive = models.TextField(blank=True, null=True)

    releasetime = models.DateTimeField(blank=True, null=True)

    #restrictions = models.TextField(blank=True, null=True)

    #sizeofcollection = models.TextField(blank=True, null=True)

    #specialpermissions = models.TextField(blank=True, null=True)

    #studycompletion = models.TextField(blank=True, null=True)

    # ----------------------------------
    # Terms of Use / Terms of Access
    # ----------------------------------
    #termsofaccess = models.TextField(blank=True, null=True)

    #termsofuse = models.TextField(blank=True, null=True)


    def get_semantic_version(self):
        if not self.id:
            return None

        if self.versionstate == VERSION_STATE_RELEASED:
            return '%s.%s' % (self.versionnumber, self.minorversionnumber)
        elif self.versionstate == VERSION_STATE_DRAFT:
            return VERSION_STATE_DRAFT
        else:
            return '%s.%s' % (self.versionnumber, self.minorversionnumber)

    def __str__(self):
        if not self.dataset:
            return 'n/a'
        version_text = self.get_semantic_version()
        if version_text is None:
            return self.dataset.__str__()

        return '%s %s' % (self.dataset, version_text)

    class Meta:
        ordering = ('-id',)
        managed = False
        db_table = 'datasetversion'


class DatasetLinkingDataverse(models.Model):
    linkcreatetime = models.DateTimeField()
    dataset = models.ForeignKey(DvObject, related_name='dataset_link')
    linkingdataverse = models.ForeignKey(DvObject, related_name='linkingdataverse')

    def __str__(self):
        return '%s %s' % (self.dataset, self.linkingdataverse)

    class Meta:
        managed = False
        db_table = 'datasetlinkingdataverse'
