from django.db import models

from apps.dvobjects.models import DvObject
from apps.datasets.models import DatasetVersion
from apps.dataverses.models import Template


class MetadataBlock(models.Model):
    displayname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(DvObject, blank=True, null=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.displayname)

    class Meta:
        managed = False
        db_table = 'metadatablock'



class DatasetFieldType(models.Model):
    name = models.TextField(blank=True, null=True)
    required = models.BooleanField()
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    fieldtype = models.CharField(max_length=255)

    advancedsearchfieldtype = models.BooleanField()
    allowcontrolledvocabulary = models.BooleanField()
    allowmultiples = models.BooleanField()

    displayformat = models.CharField(max_length=255, blank=True, null=True)
    displayoncreate = models.BooleanField()
    displayorder = models.IntegerField(blank=True, null=True)
    facetable = models.BooleanField()

    watermark = models.CharField(max_length=255, blank=True, null=True)

    metadatablock = models.ForeignKey(MetadataBlock, blank=True, null=True)
    parentdatasetfieldtype = models.ForeignKey('self', blank=True, null=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.fieldtype)

    class Meta:
        managed = False
        db_table = 'datasetfieldtype'



class ControlledVocabularyValue(models.Model):
    strvalue = models.TextField()
    datasetfieldtype = models.ForeignKey(DatasetFieldType)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    displayorder = models.IntegerField()

    def __str__(self):
        return self.strvalue

    class Meta:
        ordering = ('displayorder',)
        managed = False
        db_table = 'controlledvocabularyvalue'



class DatasetField(models.Model):
    #id = models.IntegerField(primary_key=True)
    datasetfieldtype = models.ForeignKey(DatasetFieldType)
    datasetversion = models.ForeignKey(DatasetVersion, blank=True, null=True)
    parentdatasetfieldcompoundvalue = models.ForeignKey('DatasetFieldCompoundValue', blank=True, null=True)
    template = models.ForeignKey(Template, blank=True, null=True)

    def allow_multiples(self):
        """
        Retrieve the "allowmultiples" from the DatasetFieldType
        """
        return self.datasetfieldtype.allowmultiples

    def __str__(self):
        if not self.id:
            return '(not saved)'
        return '%d' % (self.id)
        #return '%s v%s' % (self.datasetfieldtype, self.datasetversion)

    class Meta:
        managed = False
        db_table = 'datasetfield'



class DatasetFieldControlledVocabularyValue(models.Model):
    datasetfield = models.ForeignKey(DatasetField, primary_key=True)
    controlledvocabularyvalues = models.ForeignKey(ControlledVocabularyValue)

    class Meta:
        managed = False
        db_table = 'datasetfield_controlledvocabularyvalue'
        unique_together = (('datasetfield', 'controlledvocabularyvalues'),)
        #unique_together = (('datasetfield_id', 'controlledvocabularyvalues_id'),)

'''
class DatasetFieldControlledVocabularyValue(models.Model):
    """
    Change name of
    """
    datasetfield = models.ForeignKey(DatasetField)
    controlledvocabularyvalues = models.ForeignKey(ControlledVocabularyValue)

    def __str__(self):
        return '%s - %s' % (self.datasetfield.id, self.controlledvocabularyvalues)

    class Meta:
        managed = False
        ordering = ('datasetfield', 'controlledvocabularyvalues')
        db_table = 'datasetfield_controlledvocabularyvalue'
        unique_together = (('datasetfield', 'controlledvocabularyvalues'),)
'''

class DatasetFieldCompoundValue(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    parentdatasetfield = models.ForeignKey(DatasetField, blank=True, null=True)

    def __str__(self):
        if not self.id:
            return '(not saved)'
        return '%s' % self.id
        #return '%s (%s) ' % (self.parentdatasetfield, self.displayorder, )

    class Meta:
        managed = False
        db_table = 'datasetfieldcompoundvalue'


class DatasetFieldValue(models.Model):
    displayorder = models.IntegerField(blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    datasetfield = models.ForeignKey(DatasetField)

    def __str__(self):
        return '%s' % (self.value)

    class Meta:
        managed = False
        db_table = 'datasetfieldvalue'
