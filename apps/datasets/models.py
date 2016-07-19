from django.db import models
from apps.dvobjects.models import DvObject


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

    objects = DatasetManager()

    def identifier_string(self):
        return self.__str__()

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
