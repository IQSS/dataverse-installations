# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Actionlogrecord(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    actionresult = models.CharField(max_length=255, blank=True, null=True)
    actionsubtype = models.CharField(max_length=255, blank=True, null=True)
    actiontype = models.CharField(max_length=255, blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
    info = models.CharField(max_length=1024, blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    useridentifier = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actionlogrecord'


class Apitoken(models.Model):
    createtime = models.DateTimeField()
    disabled = models.BooleanField()
    expiretime = models.DateTimeField()
    tokenstring = models.CharField(unique=True, max_length=255)
    authenticateduser = models.ForeignKey('Authenticateduser')

    class Meta:
        managed = False
        db_table = 'apitoken'


class Authenticateduser(models.Model):
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    indextime = models.DateTimeField(blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    modificationtime = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    superuser = models.NullBooleanField()
    useridentifier = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'authenticateduser'


class Authenticateduserlookup(models.Model):
    authenticationproviderid = models.CharField(max_length=255, blank=True, null=True)
    persistentuserid = models.CharField(max_length=255, blank=True, null=True)
    authenticateduser = models.ForeignKey(Authenticateduser, unique=True)

    class Meta:
        managed = False
        db_table = 'authenticateduserlookup'
        unique_together = (('persistentuserid', 'authenticationproviderid'),)


class Authenticationproviderrow(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    enabled = models.NullBooleanField()
    factoryalias = models.CharField(max_length=255, blank=True, null=True)
    factorydata = models.TextField(blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authenticationproviderrow'


class Builtinuser(models.Model):
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    encryptedpassword = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    passwordencryptionversion = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'builtinuser'


class Controlledvocabalternate(models.Model):
    strvalue = models.TextField(blank=True, null=True)
    controlledvocabularyvalue = models.ForeignKey('Controlledvocabularyvalue')
    datasetfieldtype = models.ForeignKey('Datasetfieldtype')

    class Meta:
        managed = False
        db_table = 'controlledvocabalternate'

"""
class Controlledvocabularyvalue(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    strvalue = models.TextField(blank=True, null=True)
    datasetfieldtype = models.ForeignKey('Datasetfieldtype', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'controlledvocabularyvalue'
"""

class Customfieldmap(models.Model):
    sourcedatasetfield = models.CharField(max_length=255, blank=True, null=True)
    sourcetemplate = models.CharField(max_length=255, blank=True, null=True)
    targetdatasetfield = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customfieldmap'


class Customquestion(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    hidden = models.NullBooleanField()
    questionstring = models.CharField(max_length=255)
    questiontype = models.CharField(max_length=255)
    required = models.NullBooleanField()
    guestbook = models.ForeignKey('Guestbook')

    class Meta:
        managed = False
        db_table = 'customquestion'


class Customquestionresponse(models.Model):
    response = models.CharField(max_length=255, blank=True, null=True)
    customquestion = models.ForeignKey(Customquestion)
    guestbookresponse = models.ForeignKey('Guestbookresponse')

    class Meta:
        managed = False
        db_table = 'customquestionresponse'


class Customquestionvalue(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    valuestring = models.CharField(max_length=255)
    customquestion = models.ForeignKey(Customquestion)

    class Meta:
        managed = False
        db_table = 'customquestionvalue'

'''
class Datafile(models.Model):
    id = models.ForeignKey('Dvobject', db_column='id', primary_key=True)
    contenttype = models.CharField(max_length=255)
    filesystemname = models.CharField(max_length=255)
    filesize = models.BigIntegerField(blank=True, null=True)
    ingeststatus = models.CharField(max_length=1, blank=True, null=True)
    md5 = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    restricted = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'datafile'
'''

class Datafilecategory(models.Model):
    name = models.CharField(max_length=255)
    dataset = models.ForeignKey('Dvobject')

    class Meta:
        managed = False
        db_table = 'datafilecategory'


class Datafiletag(models.Model):
    type = models.IntegerField()
    datafile = models.ForeignKey('Dvobject')

    class Meta:
        managed = False
        db_table = 'datafiletag'

"""
class Dataset(models.Model):
    id = models.ForeignKey('Dvobject', db_column='id', primary_key=True)
    authority = models.CharField(max_length=255, blank=True, null=True)
    doiseparator = models.CharField(max_length=255, blank=True, null=True)
    fileaccessrequest = models.NullBooleanField()
    globalidcreatetime = models.DateTimeField(blank=True, null=True)
    identifier = models.CharField(max_length=255)
    protocol = models.CharField(max_length=255, blank=True, null=True)
    guestbook = models.ForeignKey('Guestbook', blank=True, null=True)
    thumbnailfile = models.ForeignKey('Dvobject', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset'
        unique_together = (('authority', 'protocol', 'identifier', 'doiseparator'),)
"""

class Datasetfield(models.Model):
    datasetfieldtype = models.ForeignKey('Datasetfieldtype')
    datasetversion = models.ForeignKey('Datasetversion', blank=True, null=True)
    parentdatasetfieldcompoundvalue = models.ForeignKey('Datasetfieldcompoundvalue', blank=True, null=True)
    template = models.ForeignKey('Template', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasetfield'


class DatasetfieldControlledvocabularyvalue(models.Model):
    datasetfield = models.ForeignKey(Datasetfield)
    controlledvocabularyvalues = models.ForeignKey(Controlledvocabularyvalue)

    class Meta:
        managed = False
        db_table = 'datasetfield_controlledvocabularyvalue'
        unique_together = (('datasetfield_id', 'controlledvocabularyvalues_id'),)


class Datasetfieldcompoundvalue(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    parentdatasetfield = models.ForeignKey(Datasetfield, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasetfieldcompoundvalue'


class Datasetfielddefaultvalue(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    strvalue = models.TextField(blank=True, null=True)
    datasetfield = models.ForeignKey('Datasetfieldtype')
    defaultvalueset = models.ForeignKey('Defaultvalueset')
    parentdatasetfielddefaultvalue = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasetfielddefaultvalue'

"""
class Datasetfieldtype(models.Model):
    advancedsearchfieldtype = models.NullBooleanField()
    allowcontrolledvocabulary = models.NullBooleanField()
    allowmultiples = models.NullBooleanField()
    description = models.TextField(blank=True, null=True)
    displayformat = models.CharField(max_length=255, blank=True, null=True)
    displayoncreate = models.NullBooleanField()
    displayorder = models.IntegerField(blank=True, null=True)
    facetable = models.NullBooleanField()
    fieldtype = models.CharField(max_length=255)
    name = models.TextField(blank=True, null=True)
    required = models.NullBooleanField()
    title = models.TextField(blank=True, null=True)
    watermark = models.CharField(max_length=255, blank=True, null=True)
    metadatablock = models.ForeignKey('Metadatablock', blank=True, null=True)
    parentdatasetfieldtype = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasetfieldtype'

"""
class Datasetfieldvalue(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    datasetfield = models.ForeignKey(Datasetfield)

    class Meta:
        managed = False
        db_table = 'datasetfieldvalue'


class Datasetlinkingdataverse(models.Model):
    linkcreatetime = models.DateTimeField()
    dataset = models.ForeignKey('Dvobject')
    linkingdataverse = models.ForeignKey('Dvobject')

    class Meta:
        managed = False
        db_table = 'datasetlinkingdataverse'


class Datasetlock(models.Model):
    info = models.CharField(max_length=255, blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(Authenticateduser)
    dataset = models.ForeignKey('Dvobject')

    class Meta:
        managed = False
        db_table = 'datasetlock'

'''
class Datasetversion(models.Model):
    unf = models.CharField(max_length=255, blank=True, null=True)
    archivenote = models.CharField(max_length=1000, blank=True, null=True)
    archivetime = models.DateTimeField(blank=True, null=True)
    availabilitystatus = models.TextField(blank=True, null=True)
    citationrequirements = models.TextField(blank=True, null=True)
    conditions = models.TextField(blank=True, null=True)
    confidentialitydeclaration = models.TextField(blank=True, null=True)
    contactforaccess = models.TextField(blank=True, null=True)
    createtime = models.DateTimeField()
    dataaccessplace = models.TextField(blank=True, null=True)
    deaccessionlink = models.CharField(max_length=255, blank=True, null=True)
    depositorrequirements = models.TextField(blank=True, null=True)
    disclaimer = models.TextField(blank=True, null=True)
    fileaccessrequest = models.NullBooleanField()
    inreview = models.NullBooleanField()
    lastupdatetime = models.DateTimeField()
    license = models.CharField(max_length=255, blank=True, null=True)
    minorversionnumber = models.BigIntegerField(blank=True, null=True)
    originalarchive = models.TextField(blank=True, null=True)
    releasetime = models.DateTimeField(blank=True, null=True)
    restrictions = models.TextField(blank=True, null=True)
    sizeofcollection = models.TextField(blank=True, null=True)
    specialpermissions = models.TextField(blank=True, null=True)
    studycompletion = models.TextField(blank=True, null=True)
    termsofaccess = models.TextField(blank=True, null=True)
    termsofuse = models.TextField(blank=True, null=True)
    version = models.BigIntegerField(blank=True, null=True)
    versionnote = models.CharField(max_length=1000, blank=True, null=True)
    versionnumber = models.BigIntegerField(blank=True, null=True)
    versionstate = models.CharField(max_length=255, blank=True, null=True)
    dataset = models.ForeignKey('Dvobject', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasetversion'
'''

class Datasetversionuser(models.Model):
    lastupdatedate = models.DateTimeField()
    authenticateduser = models.ForeignKey(Authenticateduser, blank=True, null=True)
    datasetversion = models.ForeignKey(Datasetversion, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasetversionuser'


class Datatable(models.Model):
    casequantity = models.BigIntegerField(blank=True, null=True)
    originalfileformat = models.CharField(max_length=255, blank=True, null=True)
    originalformatversion = models.CharField(max_length=255, blank=True, null=True)
    recordspercase = models.BigIntegerField(blank=True, null=True)
    unf = models.CharField(max_length=255)
    varquantity = models.BigIntegerField(blank=True, null=True)
    datafile = models.ForeignKey('Dvobject')

    class Meta:
        managed = False
        db_table = 'datatable'


class Datavariable(models.Model):
    fileendposition = models.BigIntegerField(blank=True, null=True)
    fileorder = models.IntegerField(blank=True, null=True)
    filestartposition = models.BigIntegerField(blank=True, null=True)
    format = models.CharField(max_length=255, blank=True, null=True)
    formatcategory = models.CharField(max_length=255, blank=True, null=True)
    interval = models.IntegerField(blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    numberofdecimalpoints = models.BigIntegerField(blank=True, null=True)
    orderedfactor = models.NullBooleanField()
    recordsegmentnumber = models.BigIntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    unf = models.CharField(max_length=255, blank=True, null=True)
    universe = models.CharField(max_length=255, blank=True, null=True)
    weighted = models.NullBooleanField()
    datatable = models.ForeignKey(Datatable)

    class Meta:
        managed = False
        db_table = 'datavariable'


class Dataverse(models.Model):
    id = models.ForeignKey('Dvobject', db_column='id', primary_key=True)
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    alias = models.CharField(max_length=255)
    dataversetype = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    #displaybytype = models.NullBooleanField()
    facetroot = models.NullBooleanField()
    guestbookroot = models.NullBooleanField()
    metadatablockroot = models.NullBooleanField()
    name = models.CharField(max_length=255)
    permissionroot = models.NullBooleanField()
    templateroot = models.NullBooleanField()
    themeroot = models.NullBooleanField()
    defaultcontributorrole = models.ForeignKey('Dataverserole')
    defaulttemplate = models.ForeignKey('Template', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataverse'


class DataverseMetadatablock(models.Model):
    dataverse = models.ForeignKey('Dvobject')
    metadatablocks = models.ForeignKey('Metadatablock')

    class Meta:
        managed = False
        db_table = 'dataverse_metadatablock'
        unique_together = (('dataverse_id', 'metadatablocks_id'),)


class Dataversecontact(models.Model):
    contactemail = models.CharField(max_length=255)
    displayorder = models.IntegerField(blank=True, null=True)
    dataverse = models.ForeignKey('Dvobject', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataversecontact'


class Dataversefacet(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    datasetfieldtype = models.ForeignKey(Datasetfieldtype, blank=True, null=True)
    dataverse = models.ForeignKey('Dvobject', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataversefacet'


class Dataversefeatureddataverse(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    dataverse = models.ForeignKey('Dvobject', blank=True, null=True)
    featureddataverse = models.ForeignKey('Dvobject', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataversefeatureddataverse'


class Dataversefieldtypeinputlevel(models.Model):
    include = models.NullBooleanField()
    required = models.NullBooleanField()
    datasetfieldtype = models.ForeignKey(Datasetfieldtype, blank=True, null=True)
    dataverse = models.ForeignKey('Dvobject', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataversefieldtypeinputlevel'


class Dataverselinkingdataverse(models.Model):
    linkcreatetime = models.DateTimeField(blank=True, null=True)
    dataverse = models.ForeignKey('Dvobject')
    linkingdataverse = models.ForeignKey('Dvobject')

    class Meta:
        managed = False
        db_table = 'dataverselinkingdataverse'


class Dataverserole(models.Model):
    alias = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    permissionbits = models.BigIntegerField(blank=True, null=True)
    owner = models.ForeignKey('Dvobject', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataverserole'


class Dataversesubjects(models.Model):
    dataverse = models.ForeignKey('Dvobject')
    controlledvocabularyvalue = models.ForeignKey(Controlledvocabularyvalue)

    class Meta:
        managed = False
        db_table = 'dataversesubjects'
        unique_together = (('dataverse_id', 'controlledvocabularyvalue_id'),)


class Dataversetheme(models.Model):
    backgroundcolor = models.CharField(max_length=255, blank=True, null=True)
    linkcolor = models.CharField(max_length=255, blank=True, null=True)
    linkurl = models.CharField(max_length=255, blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)
    logoalignment = models.CharField(max_length=255, blank=True, null=True)
    logobackgroundcolor = models.CharField(max_length=255, blank=True, null=True)
    logoformat = models.CharField(max_length=255, blank=True, null=True)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    textcolor = models.CharField(max_length=255, blank=True, null=True)
    dataverse = models.ForeignKey('Dvobject', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataversetheme'


class Defaultvalueset(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'defaultvalueset'

'''
class Dvobject(models.Model):
    dtype = models.CharField(max_length=31, blank=True, null=True)
    createdate = models.DateTimeField()
    indextime = models.DateTimeField(blank=True, null=True)
    modificationtime = models.DateTimeField()
    permissionindextime = models.DateTimeField(blank=True, null=True)
    permissionmodificationtime = models.DateTimeField(blank=True, null=True)
    publicationdate = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(Authenticateduser, blank=True, null=True)
    owner = models.ForeignKey('self', blank=True, null=True)
    releaseuser = models.ForeignKey(Authenticateduser, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvobject'
'''

class Explicitgroup(models.Model):
    description = models.CharField(max_length=1024, blank=True, null=True)
    displayname = models.CharField(max_length=255, blank=True, null=True)
    groupalias = models.CharField(unique=True, max_length=255, blank=True, null=True)
    groupaliasinowner = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(Dvobject, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'explicitgroup'


class ExplicitgroupAuthenticateduser(models.Model):
    explicitgroup = models.ForeignKey(Explicitgroup)
    containedauthenticatedusers = models.ForeignKey(Authenticateduser)

    class Meta:
        managed = False
        db_table = 'explicitgroup_authenticateduser'
        unique_together = (('explicitgroup_id', 'containedauthenticatedusers_id'),)


class ExplicitgroupContainedroleassignees(models.Model):
    explicitgroup = models.ForeignKey(Explicitgroup, blank=True, null=True)
    containedroleassignees = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'explicitgroup_containedroleassignees'


class ExplicitgroupExplicitgroup(models.Model):
    explicitgroup = models.ForeignKey(Explicitgroup)
    containedexplicitgroups = models.ForeignKey(Explicitgroup)

    class Meta:
        managed = False
        db_table = 'explicitgroup_explicitgroup'
        unique_together = (('explicitgroup_id', 'containedexplicitgroups_id'),)


class Fileaccessrequests(models.Model):
    datafile = models.ForeignKey(Dvobject)
    authenticated_user = models.ForeignKey(Authenticateduser)

    class Meta:
        managed = False
        db_table = 'fileaccessrequests'
        unique_together = (('datafile_id', 'authenticated_user_id'),)


class Filemetadata(models.Model):
    category = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=255)
    restricted = models.NullBooleanField()
    version = models.BigIntegerField(blank=True, null=True)
    datafile = models.ForeignKey(Dvobject)
    datasetversion = models.ForeignKey(Datasetversion)

    class Meta:
        managed = False
        db_table = 'filemetadata'


class FilemetadataDatafilecategory(models.Model):
    filecategories = models.ForeignKey(Datafilecategory)
    filemetadatas = models.ForeignKey(Filemetadata)

    class Meta:
        managed = False
        db_table = 'filemetadata_datafilecategory'
        unique_together = (('filecategories_id', 'filemetadatas_id'),)


class Foreignmetadatafieldmapping(models.Model):
    datasetfieldname = models.TextField(blank=True, null=True)
    foreignfieldxpath = models.TextField(blank=True, null=True)
    isattribute = models.NullBooleanField()
    foreignmetadataformatmapping = models.ForeignKey('Foreignmetadataformatmapping', blank=True, null=True)
    parentfieldmapping = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'foreignmetadatafieldmapping'
        unique_together = (('foreignmetadataformatmapping_id', 'foreignfieldxpath'),)


class Foreignmetadataformatmapping(models.Model):
    displayname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    schemalocation = models.CharField(max_length=255, blank=True, null=True)
    startelement = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'foreignmetadataformatmapping'


class Guestbook(models.Model):
    createtime = models.DateTimeField()
    emailrequired = models.NullBooleanField()
    enabled = models.NullBooleanField()
    institutionrequired = models.NullBooleanField()
    name = models.CharField(max_length=255, blank=True, null=True)
    namerequired = models.NullBooleanField()
    positionrequired = models.NullBooleanField()
    dataverse = models.ForeignKey(Dvobject, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guestbook'


class Guestbookresponse(models.Model):
    downloadtype = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    institution = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    responsetime = models.DateTimeField(blank=True, null=True)
    sessionid = models.CharField(max_length=255, blank=True, null=True)
    authenticateduser = models.ForeignKey(Authenticateduser, blank=True, null=True)
    datafile = models.ForeignKey(Dvobject)
    dataset = models.ForeignKey(Dvobject)
    datasetversion = models.ForeignKey(Datasetversion, blank=True, null=True)
    guestbook = models.ForeignKey(Guestbook)

    class Meta:
        managed = False
        db_table = 'guestbookresponse'


class Harvestingdataverseconfig(models.Model):
    id = models.BigIntegerField(primary_key=True)
    archivedescription = models.TextField(blank=True, null=True)
    archiveurl = models.CharField(max_length=255, blank=True, null=True)
    harveststyle = models.CharField(max_length=255, blank=True, null=True)
    harvesttype = models.CharField(max_length=255, blank=True, null=True)
    harvestingset = models.CharField(max_length=255, blank=True, null=True)
    harvestingurl = models.CharField(max_length=255, blank=True, null=True)
    dataverse = models.ForeignKey(Dvobject, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'harvestingdataverseconfig'


class Ingestreport(models.Model):
    endtime = models.DateTimeField(blank=True, null=True)
    report = models.CharField(max_length=255, blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    datafile = models.ForeignKey(Dvobject)

    class Meta:
        managed = False
        db_table = 'ingestreport'


class Ingestrequest(models.Model):
    controlcard = models.CharField(max_length=255, blank=True, null=True)
    labelsfile = models.CharField(max_length=255, blank=True, null=True)
    textencoding = models.CharField(max_length=255, blank=True, null=True)
    datafile = models.ForeignKey(Dvobject, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingestrequest'


class Ipv4Range(models.Model):
    id = models.BigIntegerField(primary_key=True)
    bottomaslong = models.BigIntegerField(blank=True, null=True)
    topaslong = models.BigIntegerField(blank=True, null=True)
    owner = models.ForeignKey('Persistedglobalgroup', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ipv4range'


class Ipv6Range(models.Model):
    id = models.BigIntegerField(primary_key=True)
    bottoma = models.BigIntegerField(blank=True, null=True)
    bottomb = models.BigIntegerField(blank=True, null=True)
    bottomc = models.BigIntegerField(blank=True, null=True)
    bottomd = models.BigIntegerField(blank=True, null=True)
    topa = models.BigIntegerField(blank=True, null=True)
    topb = models.BigIntegerField(blank=True, null=True)
    topc = models.BigIntegerField(blank=True, null=True)
    topd = models.BigIntegerField(blank=True, null=True)
    owner = models.ForeignKey('Persistedglobalgroup', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ipv6range'


class Maplayermetadata(models.Model):
    embedmaplink = models.CharField(max_length=255)
    layerlink = models.CharField(max_length=255)
    layername = models.CharField(max_length=255)
    mapimagelink = models.CharField(max_length=255, blank=True, null=True)
    worldmapusername = models.CharField(max_length=255)
    dataset = models.ForeignKey(Dvobject)
    datafile = models.ForeignKey(Dvobject, unique=True)

    class Meta:
        managed = False
        db_table = 'maplayermetadata'

"""
class Metadatablock(models.Model):
    displayname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Dvobject, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metadatablock'
"""

class Passwordresetdata(models.Model):
    created = models.DateTimeField()
    expires = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    builtinuser = models.ForeignKey(Builtinuser)

    class Meta:
        managed = False
        db_table = 'passwordresetdata'


class Persistedglobalgroup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    dtype = models.CharField(max_length=31, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    displayname = models.CharField(max_length=255, blank=True, null=True)
    persistedgroupalias = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'persistedglobalgroup'


class Roleassignment(models.Model):
    assigneeidentifier = models.CharField(max_length=255)
    definitionpoint = models.ForeignKey(Dvobject)
    role = models.ForeignKey(Dataverserole)

    class Meta:
        managed = False
        db_table = 'roleassignment'
        unique_together = (('assigneeidentifier', 'role_id', 'definitionpoint_id'),)


class Savedsearch(models.Model):
    query = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(Authenticateduser)
    definitionpoint = models.ForeignKey(Dvobject)

    class Meta:
        managed = False
        db_table = 'savedsearch'


class Savedsearchfilterquery(models.Model):
    filterquery = models.TextField(blank=True, null=True)
    savedsearch = models.ForeignKey(Savedsearch)

    class Meta:
        managed = False
        db_table = 'savedsearchfilterquery'


class Sequence(models.Model):
    seq_name = models.CharField(primary_key=True, max_length=50)
    seq_count = models.DecimalField(max_digits=38, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sequence'


class Setting(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'setting'


class Shibgroup(models.Model):
    attribute = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    pattern = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'shibgroup'


class Summarystatistic(models.Model):
    type = models.IntegerField(blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    datavariable = models.ForeignKey(Datavariable)

    class Meta:
        managed = False
        db_table = 'summarystatistic'

'''
class Template(models.Model):
    createtime = models.DateTimeField()
    name = models.CharField(max_length=255)
    usagecount = models.BigIntegerField(blank=True, null=True)
    dataverse = models.ForeignKey(Dvobject, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'template'
'''

class Usernotification(models.Model):
    emailed = models.NullBooleanField()
    objectid = models.BigIntegerField(blank=True, null=True)
    readnotification = models.NullBooleanField()
    senddate = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField()
    user = models.ForeignKey(Authenticateduser)

    class Meta:
        managed = False
        db_table = 'usernotification'


class Variablecategory(models.Model):
    catorder = models.IntegerField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    missing = models.NullBooleanField()
    value = models.CharField(max_length=255, blank=True, null=True)
    datavariable = models.ForeignKey(Datavariable)

    class Meta:
        managed = False
        db_table = 'variablecategory'


class Variablerange(models.Model):
    beginvalue = models.CharField(max_length=255, blank=True, null=True)
    beginvaluetype = models.IntegerField(blank=True, null=True)
    endvalue = models.CharField(max_length=255, blank=True, null=True)
    endvaluetype = models.IntegerField(blank=True, null=True)
    datavariable = models.ForeignKey(Datavariable)

    class Meta:
        managed = False
        db_table = 'variablerange'


class Variablerangeitem(models.Model):
    value = models.DecimalField(max_digits=38, decimal_places=0, blank=True, null=True)
    datavariable = models.ForeignKey(Datavariable)

    class Meta:
        managed = False
        db_table = 'variablerangeitem'


class WorldmapauthToken(models.Model):
    created = models.DateTimeField()
    hasexpired = models.BooleanField()
    lastrefreshtime = models.DateTimeField()
    modified = models.DateTimeField()
    token = models.CharField(unique=True, max_length=255, blank=True, null=True)
    application = models.ForeignKey('WorldmapauthTokentype')
    datafile = models.ForeignKey(Dvobject)
    dataverseuser = models.ForeignKey(Authenticateduser)

    class Meta:
        managed = False
        db_table = 'worldmapauth_token'


class WorldmapauthTokentype(models.Model):
    contactemail = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField()
    hostname = models.CharField(max_length=255, blank=True, null=True)
    ipaddress = models.CharField(max_length=255, blank=True, null=True)
    mapitlink = models.CharField(max_length=255)
    md5 = models.CharField(max_length=255)
    modified = models.DateTimeField()
    name = models.CharField(unique=True, max_length=255)
    timelimitminutes = models.IntegerField(blank=True, null=True)
    timelimitseconds = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'worldmapauth_tokentype'
