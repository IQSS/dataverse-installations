from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from dv_apps.dvobjects.models import DvObject
from dv_apps.terms_of_use.models import TermsOfUseAndAccess

DATAVERSE_TYPE_UNCATEGORIZED = 'UNCATEGORIZED'

@python_2_unicode_compatible
class Dataverse(models.Model):

    dvobject = models.OneToOneField(DvObject, db_column='id', primary_key=True)

    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    affiliation = models.CharField(max_length=255, blank=True, null=True)
    dataversetype = models.CharField(max_length=255)

    #displaybytype = models.NullBooleanField()

    facetroot = models.BooleanField()
    guestbookroot = models.BooleanField()

    metadatablockroot = models.BooleanField()

    permissionroot = models.BooleanField(default=True)
    templateroot = models.BooleanField()
    themeroot = models.BooleanField()

    defaultcontributorrole = models.ForeignKey('Dataverserole')
    defaulttemplate = models.ForeignKey('Template', blank=True, null=True, related_name='dv_default_template')
    #citation_redirect_url = models.CharField(db_column='citationredirecturl', max_length=255, blank=True, null=True)

    """
        defaultcontributorrole = models.ForeignKey('Dataverserole')
        defaulttemplate = models.ForeignKey('Template', blank=True, null=True)
        citationredirecturl = models.CharField(max_length=255, blank=True, null=True)
    """

    def __str__(self):
        return self.name
    #defaultcontributorrole = models.ForeignKey('Dataverserole')
    #defaulttemplate = models.ForeignKey('Template', blank=True, null=True)

    @property
    def id(self):
        if self.dvobject is None:
            return None
        return self.dvobject.id

    class Meta:
        managed = False
        db_table = 'dataverse'


class Dataverserole(models.Model):
    alias = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    permissionbits = models.BigIntegerField(blank=True, null=True)
    owner = models.ForeignKey(DvObject, blank=True, null=True)

    def __str__(self):
        return self.alias

    class Meta:
        managed = False
        db_table = 'dataverserole'

@python_2_unicode_compatible
class DataverseTheme(models.Model):
    """
    No id, created, modified
    """
    backgroundcolor = models.CharField(max_length=255, blank=True, null=True)
    linkcolor = models.CharField(max_length=255, blank=True, null=True)
    linkurl = models.CharField(max_length=255, blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    logoalignment = models.CharField(max_length=255, blank=True, null=True)
    logobackgroundcolor = models.CharField(max_length=255, blank=True, null=True)
    logoformat = models.CharField(max_length=255, blank=True, null=True)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    textcolor = models.CharField(max_length=255, blank=True, null=True)
    dataverse = models.ForeignKey(Dataverse, blank=True, null=True)

    def __str__(self):
        return '%s' % self.dataverse.name

    class Meta:
        managed = False
        db_table = 'dataversetheme'


@python_2_unicode_compatible
class DataverseContact(models.Model):
    """
    Bleh. Why isn't the FK a Dataverse?
    How can the attribute "dataverse" be null?
    """
    contactemail = models.CharField(max_length=255)
    displayorder = models.IntegerField(blank=True, null=True)
    dataverse = models.ForeignKey(DvObject, blank=True, null=True)


    def __str__(self):
        if self.dataverse:
            return self.contactemail

    class Meta:
        # real ordering is 'dataverse' first but don't want to incur cost
        ordering = ('displayorder', 'contactemail',)
        managed = False
        db_table = 'dataversecontact'


class Template(models.Model):
    name = models.CharField(max_length=255)
    dataverse = models.ForeignKey(DvObject, blank=True, null=True)

    usagecount = models.BigIntegerField(blank=True, null=True)

    createtime = models.DateTimeField()

    def __str__(self):
        return '%s (%s)' % (self.dataverse, self.dataverse)

    class Meta:
        managed = False
        db_table = 'template'



class DataverseLinkingDataverse(models.Model):
    linkcreatetime = models.DateTimeField(blank=True, null=True)
    dataverse = models.ForeignKey(DvObject, related_name='the_dataverse')
    linkingdataverse = models.ForeignKey(DvObject, related_name='the_linkingdataverse')

    def __str__(self):
        return '%s' % (self.dataverse)

    class Meta:
        managed = False
        db_table = 'dataverselinkingdataverse'

"""
class CitationPageCheck(models.Model):
    dataverse = models.ForeignKey(Dataverse)
    citation_url = models.URLField()
    widget_link = models.TextField(blank=True)
    citation_found = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.dataverse

    class Meta:
        ordering = ('-created', 'dataverse')
"""
