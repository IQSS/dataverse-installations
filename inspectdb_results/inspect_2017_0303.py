# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class EjbTimerTbl(models.Model):
    timerid = models.CharField(db_column='TIMERID', primary_key=True, max_length=255)  # Field name made lowercase.
    applicationid = models.BigIntegerField(db_column='APPLICATIONID', blank=True, null=True)  # Field name made lowercase.
    blob = models.BinaryField(db_column='BLOB', blank=True, null=True)  # Field name made lowercase.
    containerid = models.BigIntegerField(db_column='CONTAINERID', blank=True, null=True)  # Field name made lowercase.
    creationtimeraw = models.BigIntegerField(db_column='CREATIONTIMERAW', blank=True, null=True)  # Field name made lowercase.
    initialexpirationraw = models.BigIntegerField(db_column='INITIALEXPIRATIONRAW', blank=True, null=True)  # Field name made lowercase.
    intervalduration = models.BigIntegerField(db_column='INTERVALDURATION', blank=True, null=True)  # Field name made lowercase.
    lastexpirationraw = models.BigIntegerField(db_column='LASTEXPIRATIONRAW', blank=True, null=True)  # Field name made lowercase.
    ownerid = models.CharField(db_column='OWNERID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pkhashcode = models.IntegerField(db_column='PKHASHCODE', blank=True, null=True)  # Field name made lowercase.
    schedule = models.CharField(db_column='SCHEDULE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='STATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EJB__TIMER__TBL'


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
    authenticateduser = models.ForeignKey('Authenticateduser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'apitoken'


class Authenticateduser(models.Model):
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    emailconfirmed = models.DateTimeField(blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    modificationtime = models.DateTimeField(blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    superuser = models.NullBooleanField()
    useridentifier = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'authenticateduser'


class Authenticateduserlookup(models.Model):
    authenticationproviderid = models.CharField(max_length=255, blank=True, null=True)
    persistentuserid = models.CharField(max_length=255, blank=True, null=True)
    authenticateduser = models.ForeignKey(Authenticateduser, models.DO_NOTHING, unique=True)

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


class Clientharvestrun(models.Model):
    deleteddatasetcount = models.BigIntegerField(blank=True, null=True)
    faileddatasetcount = models.BigIntegerField(blank=True, null=True)
    finishtime = models.DateTimeField(blank=True, null=True)
    harvestresult = models.IntegerField(blank=True, null=True)
    harvesteddatasetcount = models.BigIntegerField(blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    harvestingclient = models.ForeignKey('Harvestingclient', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'clientharvestrun'


class Confirmemaildata(models.Model):
    created = models.DateTimeField()
    expires = models.DateTimeField()
    token = models.CharField(max_length=255, blank=True, null=True)
    authenticateduser = models.ForeignKey(Authenticateduser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'confirmemaildata'


class Controlledvocabalternate(models.Model):
    strvalue = models.TextField(blank=True, null=True)
    controlledvocabularyvalue = models.ForeignKey('Controlledvocabularyvalue', models.DO_NOTHING)
    datasetfieldtype = models.ForeignKey('Datasetfieldtype', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'controlledvocabalternate'


class Controlledvocabularyvalue(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    strvalue = models.TextField(blank=True, null=True)
    datasetfieldtype = models.ForeignKey('Datasetfieldtype', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'controlledvocabularyvalue'


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
    guestbook = models.ForeignKey('Guestbook', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'customquestion'


class Customquestionresponse(models.Model):
    response = models.TextField(blank=True, null=True)
    customquestion = models.ForeignKey(Customquestion, models.DO_NOTHING)
    guestbookresponse = models.ForeignKey('Guestbookresponse', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'customquestionresponse'


class Customquestionvalue(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    valuestring = models.CharField(max_length=255)
    customquestion = models.ForeignKey(Customquestion, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'customquestionvalue'


class Datafile(models.Model):
    id = models.ForeignKey('Dvobject', models.DO_NOTHING, db_column='id', primary_key=True)
    checksumtype = models.CharField(max_length=255)
    checksumvalue = models.CharField(max_length=255)
    contenttype = models.CharField(max_length=255)
    filesystemname = models.CharField(max_length=255)
    filesize = models.BigIntegerField(blank=True, null=True)
    ingeststatus = models.CharField(max_length=1, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    previousdatafileid = models.BigIntegerField(blank=True, null=True)
    restricted = models.NullBooleanField()
    rootdatafileid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datafile'


class Datafilecategory(models.Model):
    name = models.CharField(max_length=255)
    dataset = models.ForeignKey('Dvobject', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'datafilecategory'


class Datafiletag(models.Model):
    type = models.IntegerField()
    datafile = models.ForeignKey('Dvobject', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'datafiletag'


class Dataset(models.Model):
    id = models.ForeignKey('Dvobject', models.DO_NOTHING, db_column='id', primary_key=True)
    authority = models.CharField(max_length=255, blank=True, null=True)
    doiseparator = models.CharField(max_length=255, blank=True, null=True)
    fileaccessrequest = models.NullBooleanField()
    globalidcreatetime = models.DateTimeField(blank=True, null=True)
    harvestidentifier = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(max_length=255)
    lastexporttime = models.DateTimeField(blank=True, null=True)
    protocol = models.CharField(max_length=255, blank=True, null=True)
    citationdatedatasetfieldtype = models.ForeignKey('Datasetfieldtype', models.DO_NOTHING, blank=True, null=True)
    harvestingclient = models.ForeignKey('Harvestingclient', models.DO_NOTHING, blank=True, null=True)
    guestbook = models.ForeignKey('Guestbook', models.DO_NOTHING, blank=True, null=True)
    thumbnailfile = models.ForeignKey('Dvobject', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset'
        unique_together = (('authority', 'protocol', 'identifier', 'doiseparator'),)


class Datasetfield(models.Model):
    datasetfieldtype = models.ForeignKey('Datasetfieldtype', models.DO_NOTHING)
    datasetversion = models.ForeignKey('Datasetversion', models.DO_NOTHING, blank=True, null=True)
    parentdatasetfieldcompoundvalue = models.ForeignKey('Datasetfieldcompoundvalue', models.DO_NOTHING, blank=True, null=True)
    template = models.ForeignKey('Template', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasetfield'


class DatasetfieldControlledvocabularyvalue(models.Model):
    datasetfield = models.ForeignKey(Datasetfield, models.DO_NOTHING)
    controlledvocabularyvalues = models.ForeignKey(Controlledvocabularyvalue, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'datasetfield_controlledvocabularyvalue'
        unique_together = (('datasetfield', 'controlledvocabularyvalues'),)


class Datasetfieldcompoundvalue(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    parentdatasetfield = models.ForeignKey(Datasetfield, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasetfieldcompoundvalue'


class Datasetfielddefaultvalue(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    strvalue = models.TextField(blank=True, null=True)
    datasetfield = models.ForeignKey('Datasetfieldtype', models.DO_NOTHING)
    defaultvalueset = models.ForeignKey('Defaultvalueset', models.DO_NOTHING)
    parentdatasetfielddefaultvalue = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasetfielddefaultvalue'


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
    metadatablock = models.ForeignKey('Metadatablock', models.DO_NOTHING, blank=True, null=True)
    parentdatasetfieldtype = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasetfieldtype'


class Datasetfieldvalue(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    datasetfield = models.ForeignKey(Datasetfield, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'datasetfieldvalue'


class Datasetlinkingdataverse(models.Model):
    linkcreatetime = models.DateTimeField()
    dataset = models.ForeignKey('Dvobject', models.DO_NOTHING)
    linkingdataverse = models.ForeignKey('Dvobject', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'datasetlinkingdataverse'


class Datasetlock(models.Model):
    info = models.CharField(max_length=255, blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(Authenticateduser, models.DO_NOTHING)
    dataset = models.ForeignKey('Dvobject', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'datasetlock'


class Datasetversion(models.Model):
    unf = models.CharField(max_length=255, blank=True, null=True)
    archivenote = models.CharField(max_length=1000, blank=True, null=True)
    archivetime = models.DateTimeField(blank=True, null=True)
    createtime = models.DateTimeField()
    deaccessionlink = models.CharField(max_length=255, blank=True, null=True)
    inreview = models.NullBooleanField()
    lastupdatetime = models.DateTimeField()
    minorversionnumber = models.BigIntegerField(blank=True, null=True)
    releasetime = models.DateTimeField(blank=True, null=True)
    version = models.BigIntegerField(blank=True, null=True)
    versionnote = models.CharField(max_length=1000, blank=True, null=True)
    versionnumber = models.BigIntegerField(blank=True, null=True)
    versionstate = models.CharField(max_length=255, blank=True, null=True)
    dataset = models.ForeignKey('Dvobject', models.DO_NOTHING, unique=True, blank=True, null=True)
    termsofuseandaccess = models.ForeignKey('Termsofuseandaccess', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasetversion'
        unique_together = (('dataset', 'versionnumber', 'minorversionnumber'),)


class Datasetversionuser(models.Model):
    lastupdatedate = models.DateTimeField()
    authenticateduser = models.ForeignKey(Authenticateduser, models.DO_NOTHING, blank=True, null=True)
    datasetversion = models.ForeignKey(Datasetversion, models.DO_NOTHING, blank=True, null=True)

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
    datafile = models.ForeignKey('Dvobject', models.DO_NOTHING)

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
    datatable = models.ForeignKey(Datatable, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'datavariable'


class Dataverse(models.Model):
    id = models.ForeignKey('Dvobject', models.DO_NOTHING, db_column='id', primary_key=True)
    affiliation = models.CharField(max_length=255, blank=True, null=True)
    alias = models.CharField(unique=True, max_length=255)
    dataversetype = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    facetroot = models.NullBooleanField()
    guestbookroot = models.NullBooleanField()
    metadatablockroot = models.NullBooleanField()
    name = models.CharField(max_length=255)
    permissionroot = models.NullBooleanField()
    templateroot = models.NullBooleanField()
    themeroot = models.NullBooleanField()
    defaultcontributorrole = models.ForeignKey('Dataverserole', models.DO_NOTHING)
    defaulttemplate = models.ForeignKey('Template', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataverse'


class DataverseCitationdatasetfieldtypes(models.Model):
    dataverse = models.ForeignKey('Dvobject', models.DO_NOTHING)
    citationdatasetfieldtype = models.ForeignKey(Datasetfieldtype, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dataverse_citationdatasetfieldtypes'
        unique_together = (('dataverse', 'citationdatasetfieldtype'),)


class DataverseMetadatablock(models.Model):
    dataverse = models.ForeignKey('Dvobject', models.DO_NOTHING)
    metadatablocks = models.ForeignKey('Metadatablock', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dataverse_metadatablock'
        unique_together = (('dataverse', 'metadatablocks'),)


class Dataversecontact(models.Model):
    contactemail = models.CharField(max_length=255)
    displayorder = models.IntegerField(blank=True, null=True)
    dataverse = models.ForeignKey('Dvobject', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataversecontact'


class Dataversefacet(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    datasetfieldtype = models.ForeignKey(Datasetfieldtype, models.DO_NOTHING, blank=True, null=True)
    dataverse = models.ForeignKey('Dvobject', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataversefacet'


class Dataversefeatureddataverse(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    dataverse = models.ForeignKey('Dvobject', models.DO_NOTHING, blank=True, null=True)
    featureddataverse = models.ForeignKey('Dvobject', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataversefeatureddataverse'


class Dataversefieldtypeinputlevel(models.Model):
    include = models.NullBooleanField()
    required = models.NullBooleanField()
    datasetfieldtype = models.ForeignKey(Datasetfieldtype, models.DO_NOTHING, blank=True, null=True)
    dataverse = models.ForeignKey('Dvobject', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataversefieldtypeinputlevel'
        unique_together = (('dataverse', 'datasetfieldtype'),)


class Dataverselinkingdataverse(models.Model):
    linkcreatetime = models.DateTimeField(blank=True, null=True)
    dataverse = models.ForeignKey('Dvobject', models.DO_NOTHING)
    linkingdataverse = models.ForeignKey('Dvobject', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dataverselinkingdataverse'


class Dataverserole(models.Model):
    alias = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    permissionbits = models.BigIntegerField(blank=True, null=True)
    owner = models.ForeignKey('Dvobject', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataverserole'


class Dataversesubjects(models.Model):
    dataverse = models.ForeignKey('Dvobject', models.DO_NOTHING)
    controlledvocabularyvalue = models.ForeignKey(Controlledvocabularyvalue, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dataversesubjects'
        unique_together = (('dataverse', 'controlledvocabularyvalue'),)


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
    dataverse = models.ForeignKey('Dvobject', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataversetheme'


class Defaultvalueset(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'defaultvalueset'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Doidataciteregistercache(models.Model):
    doi = models.CharField(unique=True, max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    xml = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doidataciteregistercache'


class Dvobject(models.Model):
    dtype = models.CharField(max_length=31, blank=True, null=True)
    createdate = models.DateTimeField()
    indextime = models.DateTimeField(blank=True, null=True)
    modificationtime = models.DateTimeField()
    permissionindextime = models.DateTimeField(blank=True, null=True)
    permissionmodificationtime = models.DateTimeField(blank=True, null=True)
    previewimageavailable = models.NullBooleanField()
    publicationdate = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(Authenticateduser, models.DO_NOTHING, blank=True, null=True)
    owner = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    releaseuser = models.ForeignKey(Authenticateduser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dvobject'


class Explicitgroup(models.Model):
    description = models.CharField(max_length=1024, blank=True, null=True)
    displayname = models.CharField(max_length=255, blank=True, null=True)
    groupalias = models.CharField(unique=True, max_length=255, blank=True, null=True)
    groupaliasinowner = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(Dvobject, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'explicitgroup'


class ExplicitgroupAuthenticateduser(models.Model):
    explicitgroup = models.ForeignKey(Explicitgroup, models.DO_NOTHING)
    containedauthenticatedusers = models.ForeignKey(Authenticateduser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'explicitgroup_authenticateduser'
        unique_together = (('explicitgroup', 'containedauthenticatedusers'),)


class ExplicitgroupContainedroleassignees(models.Model):
    explicitgroup = models.ForeignKey(Explicitgroup, models.DO_NOTHING, blank=True, null=True)
    containedroleassignees = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'explicitgroup_containedroleassignees'


class ExplicitgroupExplicitgroup(models.Model):
    explicitgroup = models.ForeignKey(Explicitgroup, models.DO_NOTHING)
    containedexplicitgroups = models.ForeignKey(Explicitgroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'explicitgroup_explicitgroup'
        unique_together = (('explicitgroup', 'containedexplicitgroups'),)


class Fileaccessrequests(models.Model):
    datafile = models.ForeignKey(Dvobject, models.DO_NOTHING)
    authenticated_user = models.ForeignKey(Authenticateduser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'fileaccessrequests'
        unique_together = (('datafile', 'authenticated_user'),)


class Filemetadata(models.Model):
    description = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=255)
    restricted = models.NullBooleanField()
    version = models.BigIntegerField(blank=True, null=True)
    datafile = models.ForeignKey(Dvobject, models.DO_NOTHING)
    datasetversion = models.ForeignKey(Datasetversion, models.DO_NOTHING)
    directorylabel = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filemetadata'


class FilemetadataDatafilecategory(models.Model):
    filecategories = models.ForeignKey(Datafilecategory, models.DO_NOTHING)
    filemetadatas = models.ForeignKey(Filemetadata, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'filemetadata_datafilecategory'
        unique_together = (('filecategories', 'filemetadatas'),)


class Foreignmetadatafieldmapping(models.Model):
    datasetfieldname = models.TextField(blank=True, null=True)
    foreignfieldxpath = models.TextField(blank=True, null=True)
    isattribute = models.NullBooleanField()
    foreignmetadataformatmapping = models.ForeignKey('Foreignmetadataformatmapping', models.DO_NOTHING, blank=True, null=True)
    parentfieldmapping = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'foreignmetadatafieldmapping'
        unique_together = (('foreignmetadataformatmapping', 'foreignfieldxpath'),)


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
    dataverse = models.ForeignKey(Dvobject, models.DO_NOTHING, blank=True, null=True)

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
    authenticateduser = models.ForeignKey(Authenticateduser, models.DO_NOTHING, blank=True, null=True)
    datafile = models.ForeignKey(Dvobject, models.DO_NOTHING)
    dataset = models.ForeignKey(Dvobject, models.DO_NOTHING)
    datasetversion = models.ForeignKey(Datasetversion, models.DO_NOTHING, blank=True, null=True)
    guestbook = models.ForeignKey(Guestbook, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'guestbookresponse'


class Harvestingclient(models.Model):
    archivedescription = models.TextField(blank=True, null=True)
    archiveurl = models.CharField(max_length=255, blank=True, null=True)
    deleted = models.NullBooleanField()
    harveststyle = models.CharField(max_length=255, blank=True, null=True)
    harvesttype = models.CharField(max_length=255, blank=True, null=True)
    harvestingnow = models.NullBooleanField()
    harvestingset = models.CharField(max_length=255, blank=True, null=True)
    harvestingurl = models.CharField(max_length=255, blank=True, null=True)
    metadataprefix = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(unique=True, max_length=255)
    scheduledayofweek = models.IntegerField(blank=True, null=True)
    schedulehourofday = models.IntegerField(blank=True, null=True)
    scheduleperiod = models.CharField(max_length=255, blank=True, null=True)
    scheduled = models.NullBooleanField()
    dataverse = models.ForeignKey(Dvobject, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'harvestingclient'


class Harvestingdataverseconfig(models.Model):
    id = models.BigIntegerField(primary_key=True)
    archivedescription = models.TextField(blank=True, null=True)
    archiveurl = models.CharField(max_length=255, blank=True, null=True)
    harveststyle = models.CharField(max_length=255, blank=True, null=True)
    harvesttype = models.CharField(max_length=255, blank=True, null=True)
    harvestingset = models.CharField(max_length=255, blank=True, null=True)
    harvestingurl = models.CharField(max_length=255, blank=True, null=True)
    dataverse = models.ForeignKey(Dvobject, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'harvestingdataverseconfig'


class Ingestreport(models.Model):
    endtime = models.DateTimeField(blank=True, null=True)
    report = models.CharField(max_length=255, blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    datafile = models.ForeignKey(Dvobject, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ingestreport'


class Ingestrequest(models.Model):
    controlcard = models.CharField(max_length=255, blank=True, null=True)
    labelsfile = models.CharField(max_length=255, blank=True, null=True)
    textencoding = models.CharField(max_length=255, blank=True, null=True)
    datafile = models.ForeignKey(Dvobject, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingestrequest'


class Ipv4Range(models.Model):
    id = models.BigIntegerField(primary_key=True)
    bottomaslong = models.BigIntegerField(blank=True, null=True)
    topaslong = models.BigIntegerField(blank=True, null=True)
    owner = models.ForeignKey('Persistedglobalgroup', models.DO_NOTHING, blank=True, null=True)

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
    owner = models.ForeignKey('Persistedglobalgroup', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ipv6range'


class Maplayermetadata(models.Model):
    embedmaplink = models.CharField(max_length=255)
    isjoinlayer = models.NullBooleanField()
    joindescription = models.TextField(blank=True, null=True)
    layerlink = models.CharField(max_length=255)
    layername = models.CharField(max_length=255)
    mapimagelink = models.CharField(max_length=255, blank=True, null=True)
    maplayerlinks = models.TextField(blank=True, null=True)
    worldmapusername = models.CharField(max_length=255)
    dataset = models.ForeignKey(Dvobject, models.DO_NOTHING)
    datafile = models.ForeignKey(Dvobject, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'maplayermetadata'


class Metadatablock(models.Model):
    displayname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Dvobject, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metadatablock'


class Oairecord(models.Model):
    globalid = models.CharField(max_length=255, blank=True, null=True)
    lastupdatetime = models.DateTimeField(blank=True, null=True)
    removed = models.NullBooleanField()
    setname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oairecord'


class Oaiset(models.Model):
    definition = models.TextField(blank=True, null=True)
    deleted = models.NullBooleanField()
    description = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    spec = models.TextField(blank=True, null=True)
    updateinprogress = models.NullBooleanField()
    version = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oaiset'


class Passwordresetdata(models.Model):
    created = models.DateTimeField()
    expires = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    builtinuser = models.ForeignKey(Builtinuser, models.DO_NOTHING)

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
    privateurltoken = models.CharField(max_length=255, blank=True, null=True)
    definitionpoint = models.ForeignKey(Dvobject, models.DO_NOTHING)
    role = models.ForeignKey(Dataverserole, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'roleassignment'
        unique_together = (('assigneeidentifier', 'role', 'definitionpoint'),)


class Savedsearch(models.Model):
    query = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(Authenticateduser, models.DO_NOTHING)
    definitionpoint = models.ForeignKey(Dvobject, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'savedsearch'


class Savedsearchfilterquery(models.Model):
    filterquery = models.TextField(blank=True, null=True)
    savedsearch = models.ForeignKey(Savedsearch, models.DO_NOTHING)

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
    datavariable = models.ForeignKey(Datavariable, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'summarystatistic'


class Template(models.Model):
    createtime = models.DateTimeField()
    name = models.CharField(max_length=255)
    usagecount = models.BigIntegerField(blank=True, null=True)
    dataverse = models.ForeignKey(Dvobject, models.DO_NOTHING, blank=True, null=True)
    termsofuseandaccess = models.ForeignKey('Termsofuseandaccess', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'template'


class Termsofuseandaccess(models.Model):
    availabilitystatus = models.TextField(blank=True, null=True)
    citationrequirements = models.TextField(blank=True, null=True)
    conditions = models.TextField(blank=True, null=True)
    confidentialitydeclaration = models.TextField(blank=True, null=True)
    contactforaccess = models.TextField(blank=True, null=True)
    dataaccessplace = models.TextField(blank=True, null=True)
    depositorrequirements = models.TextField(blank=True, null=True)
    disclaimer = models.TextField(blank=True, null=True)
    fileaccessrequest = models.NullBooleanField()
    license = models.CharField(max_length=255, blank=True, null=True)
    originalarchive = models.TextField(blank=True, null=True)
    restrictions = models.TextField(blank=True, null=True)
    sizeofcollection = models.TextField(blank=True, null=True)
    specialpermissions = models.TextField(blank=True, null=True)
    studycompletion = models.TextField(blank=True, null=True)
    termsofaccess = models.TextField(blank=True, null=True)
    termsofuse = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'termsofuseandaccess'


class Usernotification(models.Model):
    emailed = models.NullBooleanField()
    objectid = models.BigIntegerField(blank=True, null=True)
    readnotification = models.NullBooleanField()
    senddate = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField()
    user = models.ForeignKey(Authenticateduser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'usernotification'


class Variablecategory(models.Model):
    catorder = models.IntegerField(blank=True, null=True)
    frequency = models.FloatField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    missing = models.NullBooleanField()
    value = models.CharField(max_length=255, blank=True, null=True)
    datavariable = models.ForeignKey(Datavariable, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'variablecategory'


class Variablerange(models.Model):
    beginvalue = models.CharField(max_length=255, blank=True, null=True)
    beginvaluetype = models.IntegerField(blank=True, null=True)
    endvalue = models.CharField(max_length=255, blank=True, null=True)
    endvaluetype = models.IntegerField(blank=True, null=True)
    datavariable = models.ForeignKey(Datavariable, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'variablerange'


class Variablerangeitem(models.Model):
    value = models.DecimalField(max_digits=38, decimal_places=0, blank=True, null=True)
    datavariable = models.ForeignKey(Datavariable, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'variablerangeitem'


class WorldmapauthToken(models.Model):
    created = models.DateTimeField()
    hasexpired = models.BooleanField()
    lastrefreshtime = models.DateTimeField()
    modified = models.DateTimeField()
    token = models.CharField(unique=True, max_length=255, blank=True, null=True)
    application = models.ForeignKey('WorldmapauthTokentype', models.DO_NOTHING)
    datafile = models.ForeignKey(Dvobject, models.DO_NOTHING)
    dataverseuser = models.ForeignKey(Authenticateduser, models.DO_NOTHING)

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
